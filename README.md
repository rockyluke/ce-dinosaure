# Ce dinosaure

Catalogue bilingue pour **ce-dinosaure.fr**, dans la continuité de
[ce-requin](https://github.com/rockyluke/ce-requin) et
[cette-baleine](https://github.com/rockyluke/cette-baleine).

19 fiches de genres réels : 18 dinosaures (dont Archaeopteryx, dinosaure avien)
et Pteranodon, explicitement identifié comme ptérosaure. Spinosaurus est présent
une seule fois. Apatosaure et Brontosaure sont des alias recherchables de deux
genres distincts : Apatosaurus et Brontosaurus.

## Contenu et sources

Les fiches Markdown de `content/real/` sont la source de vérité. Leur en-tête
entre `---` contient du JSON (sous-ensemble de YAML), avec noms, alias bilingues,
période, régime, lieux de découverte, mesures et liens de sources.
Les dimensions sont des estimations représentatives issues des résumés des
musées cités, pas des valeurs fixes pour toutes les espèces ou tous les individus
d'un genre. Les lieux sont ceux indiqués par les sources, sans prétention
à l'exhaustivité. Un champ vide est affiché « À compléter ».
Le régime d'Archaeopteryx reste incertain selon la synthèse de 2026 citée.

## Modifier et prévisualiser

1. Modifier ou ajouter une fiche dans `content/real/`.
2. Exécuter `python3 scripts/build.py` depuis la racine du dépôt.
3. Exécuter `python3 -m http.server 8000 --directory docs`.
4. Ouvrir http://localhost:8000/fr/ ou http://localhost:8000/en/.

Le générateur utilise uniquement la bibliothèque standard Python.
Les pages HTML générées sont versionnées et lisibles sans JavaScript.
`docs/app.js` filtre les fiches localement par nom/alias, période, régime et
catégorie. Aucun téléchargement des fiches n'est nécessaire à l'ouverture.
Le compteur indique le nombre de fiches visibles, ptérosaure compris.
Les filtres se combinent ; « Réinitialiser » efface tous les critères.

## Design et hébergement

`docs/styles.css` définit le design. Les pages `docs/fr/index.html` et
`docs/en/index.html` contiennent la structure ; leurs blocs balisés CATALOG et
COUNT sont remplacés par le générateur.

Site statique compatible GitHub Pages (branche `main`, dossier `/docs`).
`docs/CNAME` contient `ce-dinosaure.fr`. L'activation de Pages et les DNS sont
configurés séparément. Les pages restent en `noindex` pendant le travail de design.
