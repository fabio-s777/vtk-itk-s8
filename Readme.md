# Étude longitudinale de l'évolution d'une tumeur

## Algorithmes Utilisés

- **Recalage** : Initialisation du transformateur rigide centré suivie d'un recalage par gradient de descente.
- **Segmentation** : Seuil d'Otsu pour déterminer le seuil de segmentation, suivi d'un seuillage binaire.
- **Visualisation** : Utilisation de VTK pour visualiser les différences entre les tumeurs.

## Difficultés Rencontrées

- Choix des paramètres de recalage.
- Segmentation précise des tumeurs.
- Visualisation claire des changements.

## Résultats

Les résultats montrent les différences de volume et d'intensité des voxels entre les deux tumeurs.
