#might remove later don't need this file anymore
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os


base_dir = os.path.dirname(os.path.abspath(__file__))  
data_path = os.path.join(base_dir, '../data/CEAS_08.csv')

#load
data = pd.read_csv(data_path)

#preprocess
data["processed_body"] = data["body"].str.lower().str.replace(r"[^a-z\s]", "", regex=True)

#vectorize text
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data["processed_body"])
y = data["label"]

data.to_csv("src/data/training_data.csv", index=False)

#split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#train RF model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# evaluate
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))

#again to fix file or dir not found error, need to define base path 
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
#create the dir if it doesnt exist
os.makedirs(base_path, exist_ok=True)
#save the models
joblib.dump(rf_model, os.path.join(base_path, "random_forest_model.pkl"))
joblib.dump(vectorizer, os.path.join(base_path, "tfidf_vectorizer.pkl"))