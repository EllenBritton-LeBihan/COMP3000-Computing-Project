import joblib
import os


def load_models():
    #abs path to current file dir
    base_dir = os.path.dirname(os.path.abspath(__file__))

    #build paths 
    rf_model_path = os.path.join(base_dir, '../models/random_forest_model.pkl')
    vectorizer_path = os.path.join(base_dir, '../models/tfidf_vectorizer.pkl')
#   load
    rf_model = joblib.load(rf_model_path)
    vectorizer = joblib.load(vectorizer_path)
    return rf_model, vectorizer