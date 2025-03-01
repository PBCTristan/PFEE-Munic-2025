
"""
2 fonctions seulement à lancer :
load_and_train pour entraîner le modèle
test_file pour tester un fichier et savoir si il y a un crash ou non
"""
import os
import joblib
import json
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.utils import resample



# Étape 1: Fonction pour extraire les caractéristiques des données d'entraînement (uniquement l'accéléromètre)
def extract_features_train(data):
    accel = np.array([entry['accel'] for entry in data])
    
    # Extraction des caractéristiques (moyenne, écart-type, min, max pour l'accéléromètre)
    features = []
    features.append(np.mean(accel, axis=0))
    features.append(np.std(accel, axis=0))
    features.append(np.min(accel, axis=0))
    features.append(np.max(accel, axis=0))
    
    return np.concatenate(features)

# Étape 2: Charger les données d'entraînement
def load_data(folder):
    X = []
    y = []
    
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r') as f:
                json_data = json.load(f)
                features = extract_features_train(json_data['data'])  # Utilise uniquement l'accélération
                X.append(features)
                y.append(1 if json_data['iscrash'] else 0)
    
    return np.array(X), np.array(y)

# Ajuster la proportion des données "iscrash"
def adjust_crash_proportion_max_dataset(X, y, pourcent_accident):
    """
    Ajuste la proportion de données "iscrash" tout en maximisant la taille finale du dataset.
    
    Arguments :
    - X : numpy array, caractéristiques du dataset.
    - y : numpy array, labels associés (0 pour "non crash", 1 pour "crash").
    - pourcent_accident : float, proportion désirée de données "iscrash" (entre 0 et 1).
    
    Retourne :
    - X_new : numpy array, caractéristiques après rééchantillonnage.
    - y_new : numpy array, labels après rééchantillonnage.
    """
    if not (0 <= pourcent_accident <= 1):
        raise ValueError("Le pourcentage pourcent_accident doit être entre 0 et 1.")
    
    # Séparer les données en deux groupes
    X_crash = X[y == 1]
    X_non_crash = X[y == 0]
    
    # Taille cible des données "crash" pour respecter la proportion
    total_non_crash = len(X_non_crash)
    desired_crash_samples = int(total_non_crash * (pourcent_accident / (1 - pourcent_accident)))
    
    # Rééchantillonner les données "crash"
    if len(X_crash) >= desired_crash_samples:
        X_crash_resampled = resample(X_crash, n_samples=desired_crash_samples, random_state=42, replace=False)
    else:
        X_crash_resampled = resample(X_crash, n_samples=desired_crash_samples, random_state=42, replace=True)
    
    # Combiner les données "non crash" et "crash"
    X_new = np.vstack((X_non_crash, X_crash_resampled))
    y_new = np.hstack((np.zeros(len(X_non_crash)), np.ones(len(X_crash_resampled))))
    
    # Mélanger les données
    shuffled_indices = np.random.permutation(len(y_new))
    return X_new[shuffled_indices], y_new[shuffled_indices]

# Fonction principale pour charger les données, ajuster la proportion et entraîner le modèle
def load_and_train(folder_path, pourcent_accident=0.1, save_model=False, model_name="trained_model_Random_forest.joblib", n_estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1):
    # Charger les données d'entraînement
    X, y = load_data(folder_path)
    
    # Ajuster la proportion des données "crash"
    X, y = adjust_crash_proportion_max_dataset(X, y, pourcent_accident)
    
    # Séparer les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Normaliser/standardiser les caractéristiques
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Entraîner un classificateur (Random Forest dans ce cas)
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=42)
    clf.fit(X_train, y_train)
    
    # Prédire les probabilités (pour appliquer des seuils ensuite)
    y_prob = clf.predict_proba(X_test)[:, 1]  # Probabilité pour la classe 'crash'
    
    print("Rapport de classification sur les données de test :")
    print(classification_report(y_test, clf.predict(X_test)))
    
    # Sauvegarder le modèle si demandé
    if save_model:
        save_path = os.path.join(os.getcwd(), model_name)
        joblib.dump({"model": clf, "scaler": scaler}, save_path)
        print(f"Le modèle a été sauvegardé sous : {save_path}")
    
    return clf, scaler

def train_outlier_model(folder_path, pourcent_accident=0.1, save_model=False, model_name="outlier_model.joblib", n_estimators=100, contamination=0.1):
    # Charger les données d'entraînement
    X, y = load_data(folder_path)
    
    # Ajuster la proportion des données "crash"
    X, y = adjust_crash_proportion_max_dataset(X, y, pourcent_accident)
    
    # Séparer les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Normaliser/standardiser les caractéristiques
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Entraîner l'Isolation Forest
    clf = IsolationForest(n_estimators=n_estimators, random_state=42, contamination=contamination)
    clf.fit(X_train)
    
    # Sauvegarder le modèle si demandé
    if save_model:
        save_path = os.path.join(os.getcwd(), model_name)
        joblib.dump({"model": clf, "scaler": scaler}, save_path)
        print(f"Le modèle a été sauvegardé sous : {save_path}")
    
    return clf, scaler


# Fonction pour prédire en fonction d'un seuil
def predic_with_threshold(probs, threshold):
    return np.array(probs > threshold, dtype=int)

# Étape 4: Fonction pour extraire les caractéristiques d'un fichier de test CSV
def extract_features_from_test(df):
    accel = df[['X (m/s²)', 'Y (m/s²)', 'Z (m/s²)']].values

    # Extraction des caractéristiques (moyenne, écart-type, min, max)
    features = []
    features.append(np.mean(accel, axis=0))
    features.append(np.std(accel, axis=0))
    features.append(np.min(accel, axis=0))
    features.append(np.max(accel, axis=0))
    
    return np.concatenate(features)

# Demander le fichier CSV à tester
def test_file(file_path, scaler, clf, threshold=0.7):
    df_test = pd.read_csv(file_path)

    # Retirer les colonnes non nécessaires
    df_test = df_test.drop(columns=['received_at', 'cloud_event_id'], errors='ignore')

    # Simplifier les noms des colonnes commençant par "MESSAGES"
    df_test.columns = [
        col.split('.')[-1].replace('ACC_', '') if 'MESSAGES' in col else col
        for col in df_test.columns
    ]

    # Extraire les caractéristiques des données de test
    X_test_new = extract_features_from_test(df_test)

    # Normaliser les nouvelles données de test
    X_test_new_scaled = scaler.transform([X_test_new])

    # Prédire les probabilités pour la classe 'iscrash' (1)
    y_prob_new = clf.predict_proba(X_test_new_scaled)[:, 1]

    # Appliquer le seuil pour la prédiction
    y_pred_new = predic_with_threshold(y_prob_new, threshold)

    # Afficher la prédiction finale
    if y_pred_new[0] == 1:
        print(f"Le fichier {file_path} contient des données montrant : \nPrédiction: Crash détecté")
    else:
        print(f"Le fichier {file_path} contient des données montrant : \nPrédiction: Pas de crash")



def hyperparameter_search_Random_forest(folder_path, param_grid=None, pourcent_accident=0.1, cv=3):
    """
    Effectue une recherche d'hyperparamètres pour le RandomForestClassifier.
    
    Arguments :
    - folder_path : str, chemin vers le dossier contenant les données d'entraînement.
    - param_grid : dict, grille des hyperparamètres à tester.
    - pourcent_accident : float, proportion des données de crash après rééchantillonnage.
    - cv : int, nombre de folds pour la validation croisée.
    
    Retourne :
    - Le meilleur modèle entraîné.
    - Les meilleurs hyperparamètres trouvés.
    """
    if param_grid is None:
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
    
    # Charger les données
    X, y = load_data(folder_path)
    X, y = adjust_crash_proportion_max_dataset(X, y, pourcent_accident)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Normaliser les données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Instancier le modèle de base
    clf = RandomForestClassifier(random_state=42)
    
    # GridSearchCV pour trouver les meilleurs hyperparamètres
    grid_search = GridSearchCV(clf, param_grid, cv=cv, scoring='f1', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    print("Meilleurs hyperparamètres :", grid_search.best_params_)
    print("Meilleur score F1 :", grid_search.best_score_)
    
    return grid_search.best_estimator_, grid_search.best_params_

def hyperparameter_search_outlier(folder_path, param_grid=None, pourcent_accident=0.1, cv=3):
    """
    Effectue une recherche d'hyperparamètres pour l'IsolationForest.
    
    Arguments :
    - folder_path : str, chemin vers le dossier contenant les données d'entraînement.
    - param_grid : dict, grille des hyperparamètres à tester.
    - pourcent_accident : float, proportion des données de crash après rééchantillonnage.
    - cv : int, nombre de folds pour la validation croisée.
    
    Retourne :
    - Le meilleur modèle entraîné.
    - Les meilleurs hyperparamètres trouvés.
    """
    if param_grid is None:
        param_grid = {
            'n_estimators': [50, 100, 200],
            'contamination': [0.05, 0.1, 0.2]
        }
    
    # Charger les données
    X, y = load_data(folder_path)
    X, y = adjust_crash_proportion_max_dataset(X, y, pourcent_accident)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Normaliser les données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Instancier le modèle de base
    clf = IsolationForest(random_state=42)
    
    # GridSearchCV pour trouver les meilleurs hyperparamètres
    grid_search = GridSearchCV(clf, param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    print("Meilleurs hyperparamètres :", grid_search.best_params_)
    print("Meilleur score :", grid_search.best_score_)    
    return grid_search.best_estimator_, grid_search.best_params_

