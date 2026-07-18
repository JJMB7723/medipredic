import os
import urllib.request
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Define paths
DATASET_DIR = 'dataset'
MODEL_DIR = os.path.join('predictor', 'ml_models')
TRAINING_CSV_PATH = os.path.join(DATASET_DIR, 'training_data.csv')
TEST_CSV_PATH = os.path.join(DATASET_DIR, 'test_data.csv')
MODEL_PKL_PATH = os.path.join(MODEL_DIR, 'disease_predictor_model.pkl')
SYMPTOMS_JSON_PATH = os.path.join(MODEL_DIR, 'symptoms_list.json')

# Raw dataset URLs from GitHub
TRAINING_URL = "https://raw.githubusercontent.com/anujdutt9/Disease-Prediction-from-Symptoms/master/dataset/training_data.csv"
TEST_URL = "https://raw.githubusercontent.com/anujdutt9/Disease-Prediction-from-Symptoms/master/dataset/test_data.csv"

# List of 132 standard symptoms from the Kaggle dataset
SYMPTOMS_LIST = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", "joint_pain",
    "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition",
    "spotting_urination", "fatigue", "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss",
    "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes",
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea",
    "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea",
    "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure", "fluid_overload", "swelling_of_stomach",
    "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes",
    "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate",
    "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "neck_pain",
    "dizziness", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes",
    "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger", "extra_marital_contacts",
    "drying_of_lips_and_mouth", "slurred_speech", "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck",
    "swelling_joints", "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness",
    "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine",
    "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_(typhos)", "depression",
    "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain", "abnormal_menstruation",
    "dischromic_patches", "watering_from_eyes", "increased_appetite", "polyuria", "family_history", "mucoid_sputum",
    "rusty_sputum", "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion",
    "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen",
    "history_of_alcohol_consumption", "fluid_overload.1", "blood_in_sputum", "prominent_veins_on_calf",
    "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring", "skin_peeling",
    "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose",
    "yellow_crust_ooze"
]

# List of 41 unique diseases matching prognosis
DISEASES_LIST = [
    "Fungal infection", "Allergy", "GERD", "Chronic cholestasis", "Drug Reaction",
    "Peptic ulcer disease", "AIDS", "Diabetes ", "Gastroenteritis", "Bronchial Asthma",
    "Hypertension ", "Migraine", "Cervical spondylosis", "Paralysis (brain hemorrhage)",
    "Jaundice", "Malaria", "Chicken pox", "Dengue", "Typhoid", "hepatitis A",
    "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Alcoholic hepatitis",
    "Tuberculosis", "Common Cold", "Pneumonia", "Dimorphic hemmorhoids(piles)",
    "Heart attack", "Varicose veins", "Hypothyroidism", "Hyperthyroidism",
    "Hypoglycemia", "Osteoarthristis", "Arthritis", "(vertigo) Paroxysmal Positional Vertigo",
    "Acne", "Urinary tract infection", "Psoriasis", "Impetigo"
]

# Disease to key symptoms mapping for high-fidelity synthetic fallback
DISEASE_SYMPTOMS_MAP = {
    "Fungal infection": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"],
    "Allergy": ["continuous_sneezing", "shivering", "chills", "watering_from_eyes"],
    "GERD": ["stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "cough", "chest_pain"],
    "Chronic cholestasis": ["itching", "vomiting", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes"],
    "Drug Reaction": ["itching", "skin_rash", "stomach_pain", "burning_micturition", "spotting_urination"],
    "Peptic ulcer disease": ["vomiting", "indigestion", "loss_of_appetite", "abdominal_pain", "passage_of_gases", "internal_itching"],
    "AIDS": ["muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts"],
    "Diabetes ": ["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "excessive_hunger", "increased_appetite", "polyuria"],
    "Gastroenteritis": ["vomiting", "dehydration", "indigestion", "diarrhoea"],
    "Bronchial Asthma": ["fatigue", "cough", "high_fever", "breathlessness", "family_history", "mucoid_sputum"],
    "Hypertension ": ["headache", "chest_pain", "dizziness", "loss_of_balance", "lack_of_concentration"],
    "Migraine": ["acidity", "indigestion", "headache", "blurred_and_distorted_vision", "depression", "irritability", "visual_disturbances"],
    "Cervical spondylosis": ["back_pain", "neck_pain", "dizziness", "loss_of_balance"],
    "Paralysis (brain hemorrhage)": ["vomiting", "headache", "weakness_in_limbs", "altered_sensorium"],
    "Jaundice": ["vomiting", "yellowish_skin", "abdominal_pain", "dark_urine", "fatigue"],
    "Malaria": ["chills", "vomiting", "high_fever", "sweating", "headache", "nausea", "muscle_pain"],
    "Chicken pox": ["itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache", "loss_of_appetite", "mild_fever", "swelled_lymph_nodes", "red_spots_over_body"],
    "Dengue": ["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "muscle_pain", "red_spots_over_body"],
    "Typhoid": ["chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation", "abdominal_pain", "diarrhoea", "toxic_look_(typhos)"],
    "hepatitis A": ["joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes"],
    "Hepatitis B": ["itching", "fatigue", "lethargy", "yellowish_skin", "dark_urine", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "receiving_blood_transfusion", "receiving_unsterile_injections"],
    "Hepatitis C": ["fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes", "family_history"],
    "Hepatitis D": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
    "Hepatitis E": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes", "acute_liver_failure", "coma", "stomach_bleeding"],
    "Alcoholic hepatitis": ["vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload.1"],
    "Tuberculosis": ["chills", "vomiting", "fatigue", "weight_loss", "cough", "high_fever", "breathlessness", "sweating", "loss_of_appetite", "mild_fever", "phlegm", "swelled_lymph_nodes", "malaise", "blood_in_sputum"],
    "Common Cold": ["continuous_sneezing", "chills", "fatigue", "cough", "high_fever", "headache", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "loss_of_smell", "muscle_pain"],
    "Pneumonia": ["chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "chest_pain", "malaise", "phlegm", "rusty_sputum"],
    "Dimorphic hemmorhoids(piles)": ["constipation", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus"],
    "Heart attack": ["vomiting", "breathlessness", "sweating", "chest_pain", "palpitations"],
    "Varicose veins": ["cramps", "obesity", "swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf"],
    "Hypothyroidism": ["fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "lethargy", "dizziness", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "depression", "irritability", "abnormal_menstruation"],
    "Hyperthyroidism": ["fatigue", "mood_swings", "weight_loss", "restlessness", "sweating", "diarrhoea", "fast_heart_rate", "excessive_hunger", "muscle_weakness", "irritability", "abnormal_menstruation"],
    "Hypoglycemia": ["vomiting", "fatigue", "anxiety", "sweating", "headache", "nausea", "blurred_and_distorted_vision", "excessive_hunger", "slurred_speech", "irritability"],
    "Osteoarthristis": ["joint_pain", "neck_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking"],
    "Arthritis": ["muscle_wasting", "stiff_neck", "swelling_joints", "movement_stiffness", "painful_walking"],
    "(vertigo) Paroxysmal Positional Vertigo": ["vomiting", "headache", "nausea", "spinning_movements", "loss_of_balance", "unsteadiness"],
    "Acne": ["skin_rash", "pus_filled_pimples", "blackheads", "scurring"],
    "Urinary tract infection": ["burning_micturition", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine"],
    "Psoriasis": ["skin_rash", "joint_pain", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails"],
    "Impetigo": ["skin_rash", "high_fever", "blister", "red_sore_around_nose", "yellow_crust_ooze"]
}

def download_or_generate_datasets():
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Try downloading Training dataset
    training_loaded = False
    test_loaded = False
    
    print("Attempting to fetch Training data from GitHub...")
    try:
        urllib.request.urlretrieve(TRAINING_URL, TRAINING_CSV_PATH)
        print("Training dataset downloaded successfully.")
        training_loaded = True
    except Exception as e:
        print(f"Could not download training dataset: {e}")
        
    print("Attempting to fetch Test data from GitHub...")
    try:
        urllib.request.urlretrieve(TEST_URL, TEST_CSV_PATH)
        print("Test dataset downloaded successfully.")
        test_loaded = True
    except Exception as e:
        print(f"Could not download test dataset: {e}")
        
    # Fallback to generating synthetic data if either failed
    if not training_loaded or not test_loaded:
        print("Generating high-fidelity synthetic fallback dataset...")
        
        # We will create 200 samples per disease for training (~8200 rows)
        train_rows = []
        test_rows = []
        
        np.random.seed(42)
        
        for disease in DISEASES_LIST:
            symptoms = DISEASE_SYMPTOMS_MAP.get(disease, [])
            if not symptoms:
                # Fallback to a random selection of symptoms if not specified
                symptoms = list(np.random.choice(SYMPTOMS_LIST, 3, replace=False))
                
            # Train samples
            for _ in range(200):
                row = {sym: 0 for sym in SYMPTOMS_LIST}
                # Active main symptoms with high probability (80-95%)
                for s in symptoms:
                    if np.random.rand() < 0.90:
                        row[s] = 1
                # Active random symptoms with very low noise probability (1-5%)
                for s in SYMPTOMS_LIST:
                    if s not in symptoms and np.random.rand() < 0.02:
                        row[s] = 1
                row['prognosis'] = disease
                train_rows.append(row)
                
            # Test samples (20 per disease)
            for _ in range(20):
                row = {sym: 0 for sym in SYMPTOMS_LIST}
                for s in symptoms:
                    if np.random.rand() < 0.85:
                        row[s] = 1
                for s in SYMPTOMS_LIST:
                    if s not in symptoms and np.random.rand() < 0.02:
                        row[s] = 1
                row['prognosis'] = disease
                test_rows.append(row)
                
        df_train = pd.DataFrame(train_rows)
        df_test = pd.DataFrame(test_rows)
        
        # Ensure correct column ordering matching SYMPTOMS_LIST and prognosis
        cols = SYMPTOMS_LIST + ['prognosis']
        df_train = df_train[cols]
        df_test = df_test[cols]
        
        df_train.to_csv(TRAINING_CSV_PATH, index=False)
        df_test.to_csv(TEST_CSV_PATH, index=False)
        print("High-fidelity synthetic dataset generated and saved locally.")

def train_and_save_model():
    print("Loading datasets...")
    df_train = pd.read_csv(TRAINING_CSV_PATH)
    df_test = pd.read_csv(TEST_CSV_PATH)
    
    # Strip whitespace from prognosis column values
    df_train['prognosis'] = df_train['prognosis'].str.strip()
    df_test['prognosis'] = df_test['prognosis'].str.strip()
    
    # Split features and target
    X_train = df_train.drop('prognosis', axis=1)
    y_train = df_train['prognosis']
    X_test = df_test.drop('prognosis', axis=1)
    y_test = df_test['prognosis']
    
    # Clean up column names in case there is trailing spaces
    X_train.columns = X_train.columns.str.strip()
    X_test.columns = X_test.columns.str.strip()
    
    symptoms = list(X_train.columns)
    print(f"Features dimension: {len(symptoms)} symptoms detected.")
    
    # Train Random Forest Classifier
    print("Training Random Forest Classifier model...")
    # Using high depth and estimators to build a highly accurate model
    rf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model trained successfully. Accuracy on test dataset: {acc * 100:.2f}%")
    
    # Create output directories
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save the model pickle
    with open(MODEL_PKL_PATH, 'wb') as f:
        pickle.dump(rf, f)
    print(f"Saved trained model to: {MODEL_PKL_PATH}")
    
    # Save the symptom features list as JSON
    with open(SYMPTOMS_JSON_PATH, 'w') as f:
        json.dump(symptoms, f)
    print(f"Saved symptoms feature checklist to: {SYMPTOMS_JSON_PATH}")

if __name__ == '__main__':
    download_or_generate_datasets()
    train_and_save_model()
