from flask import Blueprint, request, render_template, current_app
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import classification_report
from app.utils import preprocess_email
import json

main_blueprint = Blueprint("main", __name__) #construct

@main_blueprint.route("/")
def home():
    return render_template("index.html")

@main_blueprint.route('/test_email', methods = ['POST'])
def test_email():
    email_text = request.form['email_text']

    #preprocess
    processed_email = preprocess_email(email_text)

    #transform wiht tfidf vectorizer
    X_test = current_app.vectorizer.transform([processed_email])

    #predict with RF
    prediction = current_app.rf_model.predict(X_test)[0]

    #load test data for metrics 
    test_data = pd.read_csv('data/test_email_dataset.csv')
    test_data['processed_body'] = test_data['v2'].apply(preprocess_email)
    X_test_data = current_app.vectorizer.transform(test_data['processed_body'])
    y_test_data = test_data['v1']

    #classification rep
    y_pred = current_app.rf_model.predict(X_test_data)
    report = classification_report(y_test_data, y_pred, output_dict=True)

    #extract for visuals
    metrics = {
        'precision': [report['0']['precision'], report['1']['precision']],
        'recall': [report['0']['recall'], report['1']['recall']],
        'f1-score': [report['0']['f1-score'], report['1']['f1-score']],
        'accuracy': [report['accuracy']],
    }

    #Plotly bar chart
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
    
    #convert to HTML
    graph_html = fig.to_html(full_html=False)
    
    return render_template('results.html', prediction=prediction, graph_html=graph_html)



@main_blueprint.route('/upload_email', methods=['POST'])
def upload_email():
    email_text = request.form.get("email_text", "")
    if not email_text:
        return jsonify({"error": "No email text provided"}), 400

    #preprocess/predict
    processed_email = current_app.preprocess_email(email_text)
    X_test = current_app.vectorizer.transform([processed_email])
    prediction = current_app.rf_model.predict(X_test)[0]


    #calc probs for explanation
    probabilities = current_app.rf_model.predict_proba(X_test)[0]

    explanation = {
        "Legitimate": f"{probabilities[0] * 100:.2f}% confidence",
        "Phishing": f"{probabilities[1] * 100:.2f}% confidence",
    }

    return jsonify({
        "prediction": "Phishing" if prediction == 1 else "Legitimate",
        "explanation": explanation,
    })

@main_blueprint.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    if not feedback_data:
        return jsonify({"error": "No feedback data provided"}), 400

    # save feedback data for future model improvements
    with open("data/user_feedback.json", "a") as f:
        json.dump(feedback_data, f)
        f.write("\n")

    return jsonify({"message": "Feedback received. Thank you!"}), 200