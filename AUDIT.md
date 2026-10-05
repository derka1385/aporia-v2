# APORIA — audit du challenge 3

Audit du 5 octobre 2026. Périmètre : moteur de recherche, reproductibilité et laboratoire `/app`. L’accueil `/` conserve le concept APORIA approuvé. Les constats ci-dessous sont tirés du code et des essais ; aucun score ne certifie la validité scientifique des conclusions.

## Verdict sur l’intégrité

La base est cohérente : profils indépendants, contrôleur à état explicite, graphes persistés et visualisation issue des variables du moteur. Le point faible était la frontière entre une proposition et une vérification, puis la maîtrise des conditions de comparaison. Les correctifs de ce lot traitent ces deux points avant la décoration.

## Constats prioritaires et traitement

| Priorité | Constat vérifié | Effet | Traitement |
|---|---|---|---|
| P1 | La couverture d’un test pouvait appartenir à une hypothèse antérieure à sa révision (`server/engine.mjs`). | Une nouvelle conclusion paraissait déjà testée. | Couverture liée à l’identifiant de l’hypothèse courante ; registre des tests et des hypothèses encore sans test. |
| P1 | Une formalisation mal formée pouvait conserver un lien `supports`. Une conclusion copiée dans les prémisses obtenait un crédit logique. | Soutien trompeur dans le graphe. | Aucun crédit ni lien de soutien pour une erreur ou une circularité directe ; contradictions et contre-modèles restent visibles. |
| P1 | Toute objection rappelée de mémoire pouvait réduire la confiance, y compris une objection déjà résolue. | Réintroduction d’un échec passé comme preuve. | Statut d’origine conservé ; une objection résolue devient un rappel conceptuel. |
| P1 | Comparaisons calculées sur les profils survivants sans dénominateur suffisamment visible. | Biais de sélection masqué. | Positions terminées seulement, nombre total, échecs et profils incomplets explicitement enregistrés. |
| P1 | Mémoire et utilité apprises changeaient entre deux conditions. | Comparaison non contrôlée. | État neuf par défaut, apprentissage antérieur explicite, instantané initial immuable et empreintes exportées. |
| P1 | Les études n’écrivaient le JSON récapitulatif qu’à la fin. | Travail et contexte difficilement récupérables après interruption. | Sauvegarde atomique à chaque étape, reprise bornée, cas terminés et erreurs conservés, refus de mélanger des versions de modèle/code. |
| P2 | La politique contient désormais des chaînes (`memoryScope`) mais le panneau les convertissait en nombres. | `NaN` dans une configuration censée être inspectable. | Formatage selon le type de la valeur. |
| P2 | Le contrôle Δ restait désactivé pour la condition à différenciation par prompt. | Impossible de contrôler l’intensité de ce témoin depuis l’interface. | Contrôle réactivé ; la condition de base reste commune. |
| P2 | Le laboratoire affichait encore le nom et le symbole provisoires Aproria. | Rupture avec l’identité APORIA approuvée. | Symbole d’origine et nom APORIA repris dans `/app`. |
| P2 | Le rendu WebGL continuait hors écran et durant une pause. | Coût GPU inutile pendant la lecture. | Arrêt hors champ/onglet masqué ; rendu à la demande pendant la pause et avec mouvement réduit. |
| P2 | La provenance, les limites et les questions ouvertes étaient dispersées. | Interprétation scientifique difficile. | Onglet Research dossier : couverture, objections, frontières de preuve, protocole et calcul consommé. |

## Qualité technique — avant ce lot

Échelle 0–4, appréciation technique limitée au périmètre inspecté ; pas une certification WCAG.

| Dimension | Score | Observation |
|---|---:|---|
| Accessibilité | 3 | Sémantique et focus présents ; actions tactiles trop petites dans le laboratoire. |
| Performance | 2 | Chargement des routes séparé ; rendu GPU encore continu hors écran. |
| Responsive | 3 | Graphes à défilement local ; long contenu corrigé par une divulgation explicite. |
| Thèmes | 2 | Identité APORIA approuvée sur l’accueil, ancien nom et nombreuses couleurs locales dans le laboratoire. |
| Intégrité de l’implémentation | 2 | Bon état explicite, mais frontière de preuve et contrôle expérimental insuffisants. |
| Total | 12/20 | Des corrections fonctionnelles étaient nécessaires avant une simple finition visuelle. |

## Ce qui fonctionne et doit rester

Le contrôleur et la mémoire modifient réellement les trajectoires. Δ n’est pas une couleur ni une consigne de rôle dans la condition architecturale. L’archive conserve les erreurs. Le vérificateur propositionnel n’exécute aucun code produit par le modèle. La sculpture WebGL possède une géométrie propre et des états lisibles ; l’accueil différencie correctement la simulation des recherches réelles. Les routes et ressources lourdes sont chargées séparément.

## Limites scientifiques persistantes

Le même petit modèle propose et juge les objections. Les corpus ne sont pas récupérés ni cités passage par passage. Les confiances et gains sont des heuristiques. La validité propositionnelle ne prouve pas la qualité d’une traduction philosophique. Les différences sémantiques ne mesurent pas l’utilité scientifique. Le prototype permet maintenant de documenter et d’examiner ces limites ; une validation indépendante reste nécessaire.

## Validation de ce lot

Voir EXPERIMENTS.md pour les résultats réels et les échecs, et RESEARCH_ROADMAP.md pour le point de reprise. 23 tests automatisés réussis ; build de production réussi. Quatre essais réels conservés, dont un échec de format et sa reprise ciblée réussie. Export de l’état initial vérifié par empreinte. Revue statique indépendante sur ordinateur et mobile : navigation active du dossier mobile corrigée par retour à la ligne ; verdict final consigné dans RESEARCH_ROADMAP.md. Un blocage signalé par l’utilisateur provenait d’un essai réellement pausé, masqué lorsqu’un ancien résultat était consulté ; un accès explicite à cet essai permet maintenant de retrouver les commandes de reprise et d’arrêt sans effacer son historique. Les contrôles de mouvement ont été vérifiés dans le code ; cette revue ne certifie ni la fluidité temporelle ni une conformité WCAG complète.
