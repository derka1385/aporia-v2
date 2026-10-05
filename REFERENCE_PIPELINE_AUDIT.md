# APORIA / Crux Lab: paper-grounded research discovery

Source audit requested by the user, 5 October 2026. This records executable behavior, rather than treating repository descriptions as proof of a working scientific result. No new experiment or model inference was launched for this audit.

## Repositories and inspection

- [Crux Lab](https://github.com/univerdread/crux-lab/tree/22299f7f31178cdd357a410cac8d0808f5dcd179), revision `22299f7f31178cdd357a410cac8d0808f5dcd179`.
- [APORIA](https://github.com/derka1385/APORIA/tree/d45ef58f19a2dd3ae0a8195b1b01763348b2084a), revision `d45ef58f19a2dd3ae0a8195b1b01763348b2084a`.

Compared both Git trees: all **78 files** under APORIA's `directions/crux_lab/` have the same Git blob IDs as the corresponding `crux_lab/` files in Crux Lab. The research backend is the same implementation at these revisions. Read the retrieval, extraction, formalization, indexing, generation, debate, adjudication, adaptive selection, brief writing, assessment, revision and export paths, their relevant prompts and selected tests. Also inspected APORIA's policy definitions, integration script, CLI workflow and recorded divine-simplicity brief summaries. External code was inspected without executing it.

APORIA's [site integration script](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions/scripts/build_aporia_site.py#L56) makes research directions the front door and moves the earlier divergence dashboard to its own page. This is a product distinction: cognitive diversity supports the finder; it is not the student's final deliverable.

## Actual pipeline

### 1. Build a topic-specific literature corpus

Topic configuration supplies several searches, area, relevance criteria, recent-publication boundary and philosophical traditions. OpenAlex provides real work records: titles, authors, dates, DOI/URLs, abstracts, venues and open-access PDF locations. Abstracts are reconstructed from the inverted index. Records are merged by OpenAlex ID; a separate normalized-title/first-author key identifies likely duplicate versions for search exclusions and display.

PDFs are downloaded from their open-access locations, extracted with PyMuPDF and cached. A corpus can contain abstract-only records; it does not imply that every work was read in full. The default full-text acquisition limit is 50, and usable text must reach 8,000 characters. Target selection requires available English full text, a thesis and LLM screening for topic relevance and argument clarity. The default target set is three recent papers plus two classics, with classic fallback when there are too few recent papers.

Sources: [OpenAlex adapter](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/corpus/openalex.py#L31), [corpus builder](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/corpus/build.py#L52), [PDF extraction](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/corpus/pdf.py#L55), [target selection](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/corpus/targets.py#L111).

### 2. Reconstruct a published argument with source evidence

An extractor proposes typed claims, including premises, conclusions, assumptions, objections and replies. Each extracted claim needs a short source quotation. The code checks quotation presence using normalization and fuzzy matching, rejects unverified proposals and deduplicates claims. Source levels distinguish full text, abstract and generated content.

The reconstruction stage connects known claim IDs into arguments with two to six premises. A formalizer maps those premises and conclusion to Boolean formulas. Code checks entailment with a truth table. A proposed missing premise is retained only if it repairs validity without making the premises inconsistent; it is explicitly generated, not attributed to the paper's author. A mapped paper can have multiple arguments, but `run_target` currently tests the first one.

Sources: [claim extraction and reconstruction](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/graph/extract.py#L110), [formalization checks](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/graph/formalize.py#L67), [mapping and index construction](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/graph/build.py#L29).

### 3. Generate objections to identified premises

The default first wave uses APORIA's five profiles: explorer, formalist, skeptic, synthesizer and minimalist. Policy interpolation through Δ changes the strongest weighted generation move, premise selection, context cap and requested sampling temperature. Models rotate across families over waves. Additional generators attack the hidden premise, apply two tradition lenses and optionally sharpen a naive question into a concrete objection.

New objections must target an allowed premise ID, explain why it fails and supply a concrete case. The generators receive the target argument's own claims; they do not receive retrieved external literature. This separates new hypothesis generation from prior-art checking. Existing paper objections can be extracted into the corpus, but the trial objections are model-generated proposals, not automatically quotations of an author's objections.

This integration uses the cognitive profiles as generators and learns their yield. It does **not** run APORIA's entire twelve-operation stateful reasoner for each objection.

Sources: [generators and validation](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/generators.py#L153), [cognitive integration](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions/crux_lab/lab/cognition.py#L77), [original policy vectors](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/lab/profiles.py#L102).

### 4. Check prior art for each objection

Before trial selection, the objection is restated in the paper's vocabulary, plain English and a neighboring tradition. The original and these restatements search two local indexes: extracted claims and paper abstracts. Retrieval combines BM25 and dense similarity through reciprocal-rank fusion. A bounded, cached live OpenAlex query adds candidate abstracts. The target work and recognized duplicate versions are excluded.

An LLM reranks up to 14 candidate passages by whether they make the same argumentative move against the same premise: `same_move`, `related` or `different`. Similarity bands are 0.70–1.00, 0.30–0.69 and 0.00–0.29. Matching quotations are checked. The score is `1 − maximum judged similarity`, preferentially using same-move/related candidates; when all candidates differ, it uses the best different candidate. Retrieval/reranking failure or no candidates produces an explicit unassessed result, not perfect novelty.

The output includes search scope and three nearest distinct works. Counts combine indexed claims, indexed abstracts and live abstract results; they are not unique-paper counts. This measures distance from what retrieval found, not academic originality established across all literature.

Sources: [hybrid index](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/graph/index.py#L105), [prior-art check](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/novelty.py#L165), [strict reranker prompt](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/agents/prompts/rerank.md).

### 5. Test objections against two defenders and a referee

A referee first screens for misreading. Each remaining objection faces two separate exchanges, each consisting of a defender reply, attacker rejoinder and defender closing reply, with early concession allowed. Defenders receive retrieved corpus claims and must cite claim IDs. The code verifies cited IDs exist and were available to that defender or belong to the target paper, and records invalid citations as struck. An external verified citation is required for `known_answer`.

The referee labels each exchange and supplies a deciding quotation from the transcript. Outcomes and survival weights are:

| Outcome | Meaning | Survival |
| --- | --- | ---: |
| misreading | The objection attacks a claim the argument does not make. | 0.0 |
| known_answer | Verified external literature already resolves it. | 0.1 |
| rebutted | The defender supplies an adequate reply. | 0.3 |
| revision_required | Saving the argument requires a changed or additional premise. | 0.8 |
| standing | The objection remains unanswered. | 1.0 |

The combined outcome is the one most favorable to the original argument, so an objection must survive both defenders. Missing referee labels make a trial fail. A required premise revision enters the argument and can itself be attacked later in the same run. Citation-ID checks and quotation checks establish traceability; they do not prove the cited passage supports the interpretation.

Sources: [exchange](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/debate.py#L81), [gauntlet and citation checks](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/gauntlet.py#L103), [outcome schema](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/graph/schema.py#L10).

### 6. Adapt which experiment runs next

The Director queue uses `S × N × (0.5 + 0.5 × C) + 0.1 × E`: survival prior, assessed novelty, premise dependence and exploration. Untested objections use `S = 0.5`. Profile learning is the mean realized survival × novelty of completed trials. This influences later exploration and generation. Default limits are 12 objections, six trials, depth two and at most three briefs per target.

This queue score is distinct from final brief ranking. It allocates a limited experiment budget; it is not an academic quality assessment.

Source: [Director](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/director.py#L17), [run orchestration](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/run.py).

### 7. Write, assess, revise and rank research briefs

Complete, novelty-assessed trials yield up to three briefs from standing/revision-required objections; if none survive, the writer can produce one diagnostic brief from the best rebutted objection. A brief contains a research question, the source argument and quotations, challenged premise, objection, strongest replies and their limits, nearest literature, unresolved questions and a concrete paper direction. Bibliographic metadata is attached from records, not invented by the writer. JSON and Markdown are saved.

The separate Assessor pass scores coherence, robustness, significance and specificity from 1 to 5, identifies the strongest objection to the proposal, and explains what a defensible paper needs. Quality is their mean. Coherence or robustness ≤2 yields `not yet defensible`; coherence and robustness ≥4 with mean ≥3.75 yields `promising`; the remainder is `needs work`. A reviser answers or narrows around the strongest objection, then the revised proposal receives a fresh assessment without showing the earlier critique. Both versions and grades are preserved.

Export ranks eligible briefs by `survival × novelty × (latest quality / 5)`. Unassessed novelty or incomplete trials cannot receive a lead score. However, ungraded briefs can still rank with a default quality multiplier of 0.6; a numbered rank is not a quality endorsement. The student can inspect the complete brief, citations, trial and original/revised assessments, and download Markdown or print it.

Sources: [brief writer](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/brief.py#L37), [academic grade rules](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/assess.py#L37), [revision pass](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/lab/assess.py#L140), [final ranking](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/export.py#L165), [brief reader](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions/web/src/pages/Brief.tsx#L170).

## Important implementation limits to preserve or improve

1. **Novelty is checked on the objection before the debate.** Assessment and revision do not rerun prior-art search for the final paper thesis. A revised brief inherits the original objection's novelty score, although its thesis may have changed. A local implementation should check the final research contribution as well.
2. **Assessment is a separate pass.** The live API calls `run_target`, which writes briefs, but does not then call assessment, revision or export. The CLI workflow explicitly includes those stages. Completing the debate alone is not completing the student deliverable. See [Makefile](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions/Makefile#L39) and [API](https://github.com/univerdread/crux-lab/blob/22299f7f31178cdd357a410cac8d0808f5dcd179/crux_lab/api/server.py#L67).
3. **Different-family assessment is preferred, with fallback.** The selector can fall back to the configured referee if another family is unavailable. Multiple roles are not automatically independent validation.
4. **The source corpus has bounded coverage.** Full-text extraction reads at most eight chunks; much of the wider index comes from abstracts. Quote presence does not establish a faithful reconstruction. Human review remains necessary.
5. **Weak directions are retained honestly.** In the pinned APORIA [divine-simplicity export](https://github.com/derka1385/APORIA/blob/d45ef58f19a2dd3ae0a8195b1b01763348b2084a/directions/web/public/data/topics/divine-simplicity/briefs.json), all 15 directions' latest assessments are `not yet defensible`; novelty ranges from 0.40 to 0.65. The top two lead scores are 0.264. These are recorded model evaluations, not independently verified publication judgments.

## Gap at the time of the source audit (before integration)

The current local prototype is an inspectable cognitive experiment. It does not yet implement this literature-based research finder.

| Required student capability | Current local behavior | Required change |
| --- | --- | --- |
| Read actual papers on the question | Five curated SEP reading pointers; their text is not retrieved | Topic search, real records, cached OA text, explicit coverage |
| Debate a published argument | Profiles propose arguments from a question | Extract quoted claims, reconstruct a source argument and attach premise IDs |
| Check academic novelty | Novelty measures lexical distance from nodes in the same profile | Corpus retrieval, prior-art judgments, source exclusions, final-thesis recheck |
| Defend and referee using evidence | Local model adjudicates its own graph | Separate roles, literature-grounded defense, citation verification, complete trial labels |
| Deliver ranked research proposals | Per-profile positions and process dossier | Brief writing, academic assessment, revision, ranking and readable export |
| Explain the score to a student | Protocol coverage/formalization diagnostics | Separate process metrics from academic quality and literature novelty |

Local evidence: [reading pointers](/Users/petrinolann/Documents/ChatGPT/aproria/server/tools.mjs:56), [within-graph novelty](/Users/petrinolann/Documents/ChatGPT/aproria/server/engine.mjs:8), [model adjudication](/Users/petrinolann/Documents/ChatGPT/aproria/server/engine.mjs:219), [process-quality dossier](/Users/petrinolann/Documents/ChatGPT/aproria/server/protocol.mjs:9).

The earlier roadmap's completed delivery describes the cognitive prototype, not completion of this paper-grounded product. Profile divergence and formal test coverage must not be presented as academic novelty or research quality.

## Concrete product acceptance criteria

- A question leads to identifiable, relevant papers and passages, with full-text/abstract provenance visible.
- A trial targets a quoted premise in a reconstructed argument; generated hidden premises are distinguished.
- Prior objections and replies are searched; new objections and resulting paper theses receive traceable prior-art checks.
- Defender/referee failures remain explicit and cannot produce successful briefs or misleading scores.
- The finished run includes assessment, bounded revision and ranked briefs, with explicit ungraded/unassessed states.
- Each brief tells the student what thesis to investigate, which existing debate it advances, what has already been said, the strongest remaining objection and what work is still required.
- Replays expose the exact paper records, extracted passages, model assignments, retrieval results, transcripts and score components.

These are the functional requirements implied by the user's correction. They are not implemented by this source audit. No interface redesign, mobile work, deployment, or new inference was performed.

## Subsequent local integration

The user subsequently authorized implementation. The audited backend now lives in `research/crux_lab/`, with the full integrated worker and student-facing reader. The historical gap table above describes the earlier prototype; see [research/UPSTREAM.md](research/UPSTREAM.md) and [README.md](README.md) for the implemented path and [EXPERIMENTS.md](EXPERIMENTS.md) for its validation boundaries.
