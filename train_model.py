# ============================================================
# AI TRAINING
# ------------------------------------------------------------
# This script:
# 1. Loads the ML-ready dataset
# 2. Converts text into numerical features (TF-IDF)
# 3. Trains the best-performing model (Random Forest)
# 4. Evaluates performance
# 5. Saves the trained model for Flask integration
# ============================================================

# ------------------------------
# Importing required libraries
# ------------------------------

import pandas as pd
import joblib  # I'm using joblib to save the trained model

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


# ============================================================
# Load the dataset
# ============================================================

# I'm loading the ML-ready dataset from the project folder.
# question_text -> input feature
# method -> target label

df = pd.read_csv("Mathematics-questions-training-dataset-ML.csv")

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)


# ============================================================
# Defining features (X) and labels (y)
# ============================================================

# I'm using question_text as input to predict solving method
X = df["question_text"]

# The model will learn to predict the correct method
y = df["method"]


# ============================================================
# Converting text into numerical format
# ============================================================

# Machine learning models cannot understand raw text.
# So I'm converting text into numerical features using TF-IDF.

vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

print("Text successfully vectorized.")


# ============================================================
# Spliting into training and testing sets
# ============================================================

# I'm splitting data into 80% training and 20% testing
# This allows me to evaluate performance properly.

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

print("Data successfully split.")


# ============================================================
# Training Random Forest model
# ============================================================

# Based on earlier evaluation, Random Forest performed best.
# So I am selecting it as the final production model.

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

print("Model training completed.")


# ============================================================
# Evaluating the model
# ============================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n===============================")
print("Final Model: Random Forest")
print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))


# ============================================================
# Saving the model + vectorizer
# ============================================================

# I must save BOTH:
# 1. The trained model
# 2. The TF-IDF vectorizer
# Because Flask will need both during prediction

joblib.dump(model, "trained_method_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully.")