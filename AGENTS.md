# Conventions du dépôt

Tous les nouveaux commits suivent Conventional Commits :

`type(scope): description`

- Types usuels : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- Le scope est facultatif ; utiliser par exemple `catalog`, `ui` ou `periods` lorsqu’il clarifie le changement.
- Rédiger une description courte en anglais, à l’impératif, sans point final.
- Réserver `style` aux changements de formatage du code ; une modification visuelle du site relève de `feat` ou `fix` selon son intention.
- Signaler une rupture de compatibilité avec `!` et un pied de message `BREAKING CHANGE:` explicatif.
- Appliquer cette convention aux prochains commits sans réécrire l’historique publié.

Exemples :

- `feat(catalog): add new dinosaur entries`
- `fix(ui): align silhouettes with dinosaur names`
- `docs: explain the catalogue file format`
