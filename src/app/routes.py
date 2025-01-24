from flask import Blueprint, request, render_template, current_app
import pandas as pd
import plotly.graph_objects as go
from app.utils import preprocess_email, parse_eml_file, save_confusion_matrix, get_explanation_from_openai
import os
import seaborn as sns
import matplotlib.pyplot as plt
import io 
import base64
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score


main_blueprint = Blueprint("main", __name__) #construct

@main_blueprint.route("/")
def home():
    return render_template("index.html")

@main_blueprint.route('/test_email', methods = ['POST'])
def test_email():
    
    uploaded_file = request.files.get("email_file")
    if not uploaded_file:
        return "No file was uploaded", 400

    filename = uploaded_file.filename
    file_ext = os.path.splitext(filename)[-1].lower()

    if file_ext not in [".txt", ".html", ".eml"]:
        return "Invalid file type. Only .txt, .html, and .eml supported.", 400

    # process file content
    if file_ext == ".eml":
        email_content = parse_eml_file(uploaded_file.read())
    else:
        email_content = uploaded_file.read().decode("utf-8")
    
    #preprocess
    processed_email = preprocess_email(email_content)

    #transform wiht tfidf vectorizer
    X_test = current_app.vectorizer.transform([processed_email])
    #predict with RF
    prediction = current_app.rf_model.predict(X_test)[0]

    #load data for metrics
    test_data = pd.read_csv('data/test_email_dataset.csv')
    test_data['processed_body'] = test_data['v2'].apply(preprocess_email)
    X_test_data = current_app.vectorizer.transform(test_data['processed_body'])
    y_test_data = test_data['v1']
    y_pred = current_app.rf_model.predict(X_test_data)

    #calc conf matrix
    cm = confusion_matrix(y_test_data, y_pred)
    metrics = {
        'TP': cm[1, 1],
        'TN': cm[0, 0],
        'FP': cm[0, 1],
        'FN': cm[1, 0],
        'precision': precision_score(y_test_data, y_pred),
        'recall': recall_score(y_test_data, y_pred),
        'f1_score': f1_score(y_test_data, y_pred),
        'accuracy': accuracy_score(y_test_data, y_pred),
    }

    #save confusion matrix PNG
    confusion_matrix_path = os.path.join('static', 'confusion_matrix.png')
    save_confusion_matrix(y_test_data, y_pred, confusion_matrix_path)

    #gen xplanation using OpenAI API
    explanation = get_explanation_from_openai(metrics)

    #render results
    return render_template(
        'results.html',
        prediction=prediction,
        confusion_matrix_img=confusion_matrix_path,
        explanation=explanation
    )
    

    
