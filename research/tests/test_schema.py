from crux_lab.graph.extract import ArgumentsOut
from crux_lab.llm.client import _compact_schema


def test_argument_title_is_preserved_in_compact_generation_schema():
    schema = _compact_schema(ArgumentsOut)
    argument = schema['$defs']['XArgument']
    assert 'title' in argument['properties']
    assert 'title' in argument['required']
    assert argument['properties']['title']['type'] == 'string'
    assert 'title' not in argument  # descriptive schema metadata is still compacted


def test_reconstruction_grammar_restricts_ids_and_premise_count():
    import asyncio
    from crux_lab.graph.extract import reconstruct_arguments
    from crux_lab.graph.schema import Claim
    from pydantic import ValidationError
    import pytest
    captured = []
    class InspectClient:
        async def json(self, role, user, schema, *a, **kw):
            captured.append(schema)
            return None, None
    claims = [Claim(id=f'P.c{i}', paper_id='oa:P', kind=k, text='Evidence', quote='Evidence', level='fulltext') for i, k in enumerate(['premise', 'premise', 'conclusion', 'objection'], 1)]
    asyncio.run(reconstruct_arguments(InspectClient(), 'oa:P', 'Source', '', claims))
    schema = captured[0]
    valid = {'arguments': [{'title': 'A sourced inference', 'premise_ids': ['P.c1', 'P.c2'], 'conclusion_id': 'P.c3'}]}
    assert schema.model_validate(valid)
    for ids in [['P.c1', 'P.c3'], ['P.c1', 'invented'], ['P.c1'] * 7]:
        invalid = {'arguments': [{**valid['arguments'][0], 'premise_ids': ids}]}
        with pytest.raises(ValidationError):
            schema.model_validate(invalid)


def test_formalizer_schema_requires_source_ids_and_boolean_syntax():
    import asyncio
    from crux_lab.graph.formalize import formalize
    from crux_lab.graph.schema import Argument, Claim
    captured = []
    class InspectClient:
        async def json(self, role, user, schema, *a, **kw):
            captured.append(schema.model_json_schema())
            return None, None
    claims = {f'P.c{i}': Claim(id=f'P.c{i}', paper_id='oa:P', kind='premise' if i < 3 else 'conclusion', text='Evidence', quote='Evidence', level='fulltext') for i in range(1, 4)}
    arg = Argument(id='P.arg1', paper_id='oa:P', title='Source argument', premise_ids=['P.c1', 'P.c2'], conclusion_id='P.c3')
    asyncio.run(formalize(InspectClient(), arg, claims))
    schema = captured[0]
    formulas = schema['properties']['premise_formulas']
    assert formulas['required'] == arg.premise_ids
    assert set(formulas['properties']) == set(arg.premise_ids)
    assert formulas['additionalProperties'] is False
    import re
    pattern = formulas['properties']['P.c1']['pattern']
    assert re.fullmatch(pattern, '(A -> B) & ~C')
    assert not re.fullmatch(pattern, 'A = B')
