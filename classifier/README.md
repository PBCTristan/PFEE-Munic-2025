# README - Détection de Crashes avec Random Forest et Isolation Forest

## Description du Projet

Ce projet implémente un pipeline complet pour la détection de crashes à partir de données d'accéléromètre. Deux modèles sont utilisés :
- **RandomForestClassifier** pour la classification supervisée
- **IsolationForest** pour la détection d'anomalies

Les données sont extraites à partir de fichiers JSON contenant des relevés de capteurs et une étiquette indiquant la présence ou non d'un crash. Des fonctionnalités d'hyperparamétrage et d'équilibrage des classes sont également disponibles.

---

## Prérequis

- Python 3.x
- Bibliothèques : `numpy`, `pandas`, `scikit-learn`, `joblib`

Installez les dépendances avec la commande :
```bash
pip install numpy pandas scikit-learn joblib
```

---

## Structure des Données

Les fichiers JSON d'entraînement doivent suivre cette structure :
```json
{
  "data": [
    {"accel": [x, y, z]},
    ...
  ],
  "iscrash": true | false
}
```

Les fichiers CSV de test doivent contenir les colonnes suivantes :
- `X (m/s²)`
- `Y (m/s²)`
- `Z (m/s²)`

---

## Utilisation des Fonctions Principales

### Entraînement du Modèle : `load_and_train`

```python
from votre_script import load_and_train

clf, scaler = load_and_train(
    folder_path='chemin/vers/donnees',
    pourcent_accident=0.1,
    save_model=True,
    model_name='trained_model_Random_forest.joblib'
)
```

**Arguments :**
- `folder_path` : Chemin vers le dossier contenant les fichiers JSON
- `pourcent_accident` : Proportion de données "crash" souhaitée
- `save_model` : Sauvegarde du modèle après entraînement
- `model_name` : Nom du fichier du modèle sauvegardé

---

### Test d'un Fichier : `test_file`

```python
from votre_script import test_file

test_file(
    file_path='chemin/vers/fichier_test.csv',
    scaler=scaler,
    clf=clf,
    threshold=0.7
)
```

**Arguments :**
- `file_path` : Chemin vers le fichier CSV à tester
- `scaler` : StandardScaler utilisé pour la normalisation
- `clf` : Modèle Random Forest entraîné
- `threshold` : Seuil de probabilité pour prédire un crash

---

## Recherche d'Hyperparamètres

### Pour Random Forest

```python
from votre_script import hyperparameter_search_Random_forest

best_model, best_params = hyperparameter_search_Random_forest(
    folder_path='chemin/vers/donnees'
)
```

### Pour Isolation Forest

```python
from votre_script import hyperparameter_search_outlier

best_model, best_params = hyperparameter_search_outlier(
    folder_path='chemin/vers/donnees'
)
```

---

## Résultats et Évaluation

Les performances sont évaluées via :
- Rapport de classification : Précision, Rappel, F1-Score
- Matrice de confusion

---

## Sauvegarde des Modèles

Les modèles entraînés sont sauvegardés au format `.joblib` avec le scaler associé.

## Additional Information

This project also includes .ipynb files demonstrating the application of these functions and testing the model’s performance with the data in the dataNous/ folder. These notebooks evaluate the model’s effectiveness through precision, recall, F1 score, and other performance metrics.

