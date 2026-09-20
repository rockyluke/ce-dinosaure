# Ce dinosaure

Catalogue bilingue pour **ce-dinosaure.fr**, dans la continuité de
[ce-requin](https://github.com/rockyluke/ce-requin) et
[cette-baleine](https://github.com/rockyluke/cette-baleine).

340 fiches bilingues : 337 animaux réels et 3 hybrides fictifs de l’univers Jurassic World.
Les 326 noms du répertoire A–Z du Natural History Museum sont présents,
avec les autres animaux déjà ajoutés au catalogue.
Les groupes sont identifiés sur chaque fiche. Archaeopteryx est un dinosaure avien.
Spinosaurus est présent
une seule fois. Apatosaure et Brontosaure sont des alias recherchables de deux
genres distincts : Apatosaurus et Brontosaurus.

## Contenu et sources

Les fiches Markdown de `content/real/` et `content/fictional/` sont la source de vérité. Leur en-tête
entre `---` contient du JSON (sous-ensemble de YAML), avec noms, alias bilingues,
période, régime, lieux de découverte, mesures et liens de sources.
Les dimensions sont des estimations représentatives issues des résumés des
musées cités, pas des valeurs fixes pour toutes les espèces ou tous les individus
d'un genre. Les lieux sont ceux indiqués par les sources, sans prétention
à l'exhaustivité. Un champ vide est affiché « À compléter ».
Le régime d'Archaeopteryx reste incertain selon la synthèse de 2026 citée.

Le relevé du répertoire du 20 septembre 2026 est conservé dans
`content/nhm-directory.json` : 295 fiches manquantes ont été ajoutées sans
écraser les 31 fiches déjà présentes. Les données factuelles sont attribuées
à chaque page du musée ; les textes descriptifs ne sont pas reproduits.
Les pays sont traduits en français. Les dimensions absentes restent à compléter
et les régimes inconnus ou ambigus sont signalés comme incertains.
La période de Hagryphus est complétée avec le musée d’histoire naturelle de l’Utah.

## Modifier et prévisualiser

1. Modifier ou ajouter une fiche dans `content/real/`.
2. Exécuter `python3 scripts/build.py` depuis la racine du dépôt.
3. Exécuter `python3 -m http.server 8000 --directory docs`.
4. Ouvrir http://localhost:8000/fr/ ou http://localhost:8000/en/.

Le générateur utilise uniquement la bibliothèque standard Python.
Les pages HTML générées sont versionnées et lisibles sans JavaScript.
`docs/app.js` filtre les fiches localement par nom/alias, période, régime et
catégorie. Aucun téléchargement des fiches n'est nécessaire à l'ouverture.
Le compteur indique le nombre de fiches visibles.
Les filtres se combinent ; « Réinitialiser » efface tous les critères.

## Design et hébergement

`docs/styles.css` définit le design. Les pages `docs/fr/index.html` et
`docs/en/index.html` contiennent la structure ; leurs blocs balisés CATALOG et
COUNT sont remplacés par le générateur.

Site statique compatible GitHub Pages (branche `main`, dossier `/docs`).
`docs/CNAME` contient `ce-dinosaure.fr`. L'activation de Pages et les DNS sont
configurés séparément. Les pages restent en `noindex` pendant le travail de design.

## Périodes géologiques

Chaque période affichée sur une fiche renvoie à la section correspondante de
`docs/fr/periods.html` ou `docs/en/periods.html`. Ces pages expliquent le Permien, le Trias, le Jurassique, le Crétacé et
le Paléogène avec des résumés originaux et une frise chronologique. Chaque
section cite Wikipédia dans la langue de la page (français ou anglais). Un complément sur le Permien situe Dimetrodon avant les dinosaures. Les dates sont des
repères arrondis et la frise n'est pas proportionnelle aux durées.
`docs/periods.js` conserve la section lors d'un changement de langue.
Les filtres de régime suivent l'ordre Carnivore, Herbivore, Omnivore, après Tous.

## Silhouettes de taille

Les vignettes SVG locales de `docs/assets/size-comparisons/` proviennent des
comparaisons schématiques du Natural History Museum : silhouettes génériques
par famille corporelle avec humain, et non portraits anatomiques de chaque genre.
L'objet `image` des fiches indique le fichier, le mode et sa source.
Brontosaurus n'a pas de comparaison NHM disponible ; sa silhouette générique de
sauropode est donc présentée sans humain et sans échelle. Les crédits et détails
d'extraction figurent dans le README du dossier des images et `sources.json`.
Les images se placent à côté du nom et renvoient à leur source au clic.
Les mesures sont affichées sans symbole d'approximation ; la note générale
continue de préciser qu'il s'agit d'estimations.

## Créatures fictives et autres reptiles préhistoriques

Indominus rex, Scorpios rex et Indoraptor ont la catégorie `fictional`, le type
`hybrid`, une période `fictional` (sans lien vers les périodes géologiques), et
un univers bilingue. Les valeurs de fiction viennent des pages Jurassic Park
Wiki françaises citées ; les poids inconnus restent à compléter. Le filtre
Fictifs affiche ces trois fiches, avec une présentation distincte.

Quetzalcoatlus et Pterodactylus sont identifiés comme ptérosaures, Plesiosaurus
et Mosasaurus comme reptiles marins. Ils restent dans la catégorie Réels.
Les mesures d'envergure sont distinguées des longueurs. Les estimations
controversées sont précisées dans les notes.

Ceratosaurus et Deinonychus utilisent les comparaisons NHM génériques locales.
Aucune silhouette NHM n'est attribuée aux sept autres nouvelles fiches en
l'absence de comparaison vérifiée ; leurs titres occupent toute la largeur.
Les filtres géologiques ne sélectionnent que les animaux réels : conserver
« Toutes » pour afficher les hybrides fictifs.

## Drapeaux et illustrations complémentaires

Les drapeaux sont ajoutés par `scripts/build.py` à partir des pays en anglais,
sans modifier les champs Markdown. Les noms français et anglais restent visibles
et accessibles. Les régions sans drapeau national et les lieux fictifs restent
en texte. Les précisions entre parenthèses sont conservées.

Les 30 vignettes manquantes sont des SVG originaux générés par
`python3 scripts/draw_silhouettes.py`, puis intégrés par `python3 scripts/build.py`.
Le manifeste dans `docs/assets/original-silhouettes/` évite toute modification
des fiches. Un humain de 1,75 m apparaît uniquement si la mesure est documentée ;
les autres dessins sont sans échelle. Voir le README de ce dossier pour les
conventions de comparaison et les limites des dessins.
