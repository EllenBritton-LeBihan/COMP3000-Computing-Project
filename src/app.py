from flask import Flask, request, render_template, jsonify
import joblib
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics import classification_report
import plotly.graph_objects as go

app=Flask(__name__, template_folder='templates', static_folder='static')

#models
rf_model = joblib.load('models/random_forest_model.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')


def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text) 
    text = re.sub(r'http\S+', '', text)  
    text = re.sub(r'[^a-z\s]', '', text)  
    return text

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/test_email', methods=['POST'])
def test_email():
    email_text = request.form['email_text']
    
    #preprocess
    processed_email = preprocess_email(email_text)
    
    #transform using tfidf
    X_test = vectorizer.transform([processed_email])
    
    #predict the label (0 = Legit, 1 = Phishing)
    prediction = rf_model.predict(X_test)[0]
    
    #prepare metrics to load 
    test_data = pd.read_csv('data/test_email_dataset.csv')  #load the test data
    test_data['processed_body'] = test_data['v2'].apply(preprocess_email)
    X_test_data = vectorizer.transform(test_data['processed_body'])
    y_test_data = test_data['v1']
    
    #Predict using model
    y_pred = rf_model.predict(X_test_data)
    
    #gen classification report
    report = classification_report(y_test_data, y_pred, output_dict=True)
    
    #extract metrics for visuals
    metrics = {
        'precision': [report['0']['precision'], report['1']['precision']],
        'recall': [report['0']['recall'], report['1']['recall']],
        'f1-score': [report['0']['f1-score'], report['1']['f1-score']],
        'accuracy': [report['accuracy']],
    }

    #create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Precision', x=['Non-phishing', 'Phishing'], y=metrics['precision']),
        go.Bar(name='Recall', x=['Non-phishing', 'Phishing'], y=metrics['recall']),
        go.Bar(name='F1-Score', x=['Non-phishing', 'Phishing'], y=metrics['f1-score'])
    ])
    
    fig.update_layout(
        title="Model Performance Metrics",
        xaxis_title="Class",
        yaxis_title="Score",
        barmode='group'
    )
    
    #convert figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('results.html', prediction=prediction, graph_html=graph_html)


if __name__ == "__main__":
    app.run(debug=True)