# Ce dinosaure

Trame de design bilingue pour **ce-dinosaure.fr**, dans la continuité de
[ce-requin](https://github.com/rockyluke/ce-requin) et
[cette-baleine](https://github.com/rockyluke/cette-baleine).

## État actuel

Aucune donnée d’espèce, aucun appel réseau, aucune dépendance de compilation.
Trois fiches vierges permettent de travailler la présentation. Le compteur reste
à zéro. La recherche et les filtres affichent un état vide ; la réinitialisation
rétablit les fiches de présentation. Français et anglais sont disponibles, avec
mémorisation de la langue lorsque le stockage local est autorisé.

## Aperçu local

Depuis la racine du dépôt : `python3 -m http.server 8000 --directory docs`.
Ouvrir http://localhost:8000/fr/ (ou /en/).

## Design

`docs/styles.css` contient la palette, la typographie et les mises en page.
`docs/fr/index.html` et `docs/en/index.html` contiennent les trames de fiches.
`docs/app.js` gère uniquement les interactions de présentation.

## Hébergement prévu

Site statique dans `docs/`, compatible GitHub Pages (branche `main`, dossier
`/docs`). `docs/CNAME` réserve la configuration pour `ce-dinosaure.fr`.
L’activation de Pages et les DNS doivent être configurés séparément.
Les pages restent en `noindex` pendant la phase de design.

## À venir

Valider le design avant de définir le format Markdown des fiches, d’ajouter
les données sourcées et de brancher la recherche sur le catalogue.
