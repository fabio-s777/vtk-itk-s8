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

- **Recalage d'Images** : Initialisation du transformateur rigide centré suivie d'un recalage par gradient de descente.
- **Segmentation des Tumeurs** : Seuil d'Otsu pour déterminer le seuil de segmentation, suivi d'un seuillage binaire.
- **Visualisation** : Utilisation de VTK pour visualiser les différences entre les tumeurs.

### 1. Recalage d'Images

**Objectif :** Aligner les deux scans pour permettre une comparaison précise des tumeurs.

**Algorithme :**

- **Initialisation du transformateur rigide centré :** 
  - Utilisation de `itk.CenteredTransformInitializer` pour aligner approximativement les images.
  - Choix d'une transformation rigide (rotation et translation) car les variations entre les scans sont principalement de ce type.
  
- **Recalage par descente de gradient :**
  - Utilisation de `itk.ImageRegistrationMethodv4` avec un optimiseur de gradient de descente régulier (`itk.RegularStepGradientDescentOptimizerv4`).
  - La métrique utilisée est `itk.MeanSquaresImageToImageMetricv4`, qui mesure les différences en intensité entre les images alignées.

**Paramètres Clés :**
  - **TransformType** : `itk.VersorRigid3DTransform[itk.D]`
  - **OptimizerType** : `itk.RegularStepGradientDescentOptimizerv4[itk.D]`
  - **MetricType** : `itk.MeanSquaresImageToImageMetricv4`

  ### 2. Segmentation des Tumeurs

**Objectif :** Isoler les tumeurs dans chaque scan pour permettre une analyse de leur évolution.

**Algorithme :**

- **Seuil d'Otsu :**
  - Utilisation de `itk.OtsuThresholdImageFilter` pour déterminer automatiquement un seuil de segmentation basé sur l'histogramme des intensités des voxels.
  - Cet algorithme est choisi pour sa capacité à séparer efficacement les régions d'intérêt (tumeur) du reste de l'image en fonction des intensités.

- **Seuillage Binaire :**
  - Application d'un filtre de seuillage binaire (`itk.BinaryThresholdImageFilter`) avec le seuil déterminé par l'Otsu pour créer une image binaire où les voxels de la tumeur sont mis en valeur.

**Paramètres Clés :**
  - **LowerThreshold** : Seuil déterminé par Otsu
  - **UpperThreshold** : Valeur maximale de l'intensité des voxels (typiquement `itk.NumericTraits[itk.F].max()`)
  - **InsideValue** : 1 (valeur des voxels de la tumeur)
  - **OutsideValue** : 0 (valeur des voxels non-tumeur)

### 3. Visualisation

**Objectif :** Visualiser les différences entre les deux tumeurs pour évaluer leur évolution.

**Algorithme :**

- **Filtrage par soustraction et valeur absolue :**
  - Utilisation de `itk.SubtractImageFilter` pour calculer la différence voxel par voxel entre les deux images segmentées.
  - Application de `itk.AbsImageFilter` pour obtenir les valeurs absolues des différences, mettant ainsi en évidence les changements.

- **Conversion ITK à VTK :**
  - Transformation des images ITK en format VTK pour permettre leur visualisation.

- **Application de table de couleurs (Lookup Table) :**
  - Utilisation de `vtkLookupTable` pour mapper les valeurs scalaires des voxels à une gamme de couleurs, facilitant ainsi l'interprétation visuelle des différences.

**Paramètres Clés :**
  - **Range de la Lookup Table** : 0 à 255 (valeurs typiques des intensités des voxels après segmentation)


## Difficultés Rencontrées

- Choix des paramètres de recalage.
- Segmentation précise des tumeurs.
- Visualisation claire des changements.

## Résultats

Les résultats montrent les différences de volume et d'intensité des voxels entre les deux tumeurs.
