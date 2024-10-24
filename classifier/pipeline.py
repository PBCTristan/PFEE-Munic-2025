import os
import json
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

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

# Demander le dossier contenant les données d'entraînement
folder_path = input("Entrez le dossier contenant les données d'entraînement (ex: './dataNous') : ")
X, y = load_data(folder_path)

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normaliser/standardiser les caractéristiques
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Entraîner un classificateur (Random Forest dans ce cas)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Prédire les probabilités (pour appliquer des seuils ensuite)
y_prob = clf.predict_proba(X_test)[:, 1]  # Probabilité pour la classe 'crash'

# Fonction pour prédire en fonction d'un seuil
def predic_with_threshold(probs, threshold):
    return np.array(probs > threshold, dtype=int)

# Sélection du meilleur seuil (exemple: 0.7 trouvé plus tôt)
threshold = 0.7

# Étape 4: Fonction pour extraire les caractéristiques d'un fichier de test CSV
def extract_features_from_test(df):
    # Utiliser les colonnes X, Y, Z correspondant aux valeurs de l'accélération
    accel = df[['X (m/s²)', 'Y (m/s²)', 'Z (m/s²)']].values

    # Extraction des caractéristiques (moyenne, écart-type, min, max)
    features = []
    features.append(np.mean(accel, axis=0))
    features.append(np.std(accel, axis=0))
    features.append(np.min(accel, axis=0))
    features.append(np.max(accel, axis=0))
    
    return np.concatenate(features)

# Demander le fichier CSV à tester
file_path = input("Entrez le nom du fichier CSV à tester (ex: 'dataMunich/ACCData/device3-2024-09-14T18_29_05.csv') : ")

# Charger les données de test
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
