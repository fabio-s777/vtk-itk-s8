# Étude longitudinale de l'évolution d'une tumeur


## Objectif
Ce projet vise à suivre les changements d'une tumeur à partir de deux scans effectués sur un même patient à des dates différentes.

## Étapes

1. **Chargement des scans** : Les scans sont chargés en utilisant ITK.
2. **Recalage d'images** : Les scans sont alignés automatiquement.
3. **Segmentation des tumeurs** : Les tumeurs sont segmentées dans les deux volumes.
4. **Analyse et visualisation des changements** : Les changements entre les tumeurs sont analysés et visualisés.

## utilisation

**debug** permet d'afficher les 2 d'inputs
**main** permet de calculer et d'afficher l'évolution de la tumeur

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
