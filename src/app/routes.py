from flask import Blueprint, request, render_template, current_app
import pandas as pd
from app.utils import preprocess_email, parse_eml_file, save_confusion_matrix, get_explanation_from_openai
import os
from flask import jsonify
from werkzeug.utils import secure_filename
import email
import pickle
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score


#tryig again with new model, ignored last flask integration for now







#IGNORING FOR NOW TRYING SOMETHNIG OUT
'''
main_blueprint = Blueprint("main", __name__) #construct

@main_blueprint.route("/")
def home():
    return render_template("index.html")

@main_blueprint.route('/test_email', methods = ['POST'])
def test_email():

    uploaded_file = request.files.get("email_file")
    if not uploaded_file:
        return jsonify({"error": "No file was uploaded"}), 400
    
    filename = uploaded_file.filename
    file_ext = os.path.splitext(filename)[-1].lower() #work around

    if file_ext not in [".txt", ".html", ".eml"]:
        return jsonify({"error": "Invalid file type. Only .txt, .html, and .eml supported."}), 400


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
    cm_list = cm.tolist() 

    metrics = {
        'True Positive': cm[1, 1],
        'True Negative': cm[0, 0],
        'False Positive': cm[0, 1],
        'False Negative': cm[1, 0],
    }
    
    #gen xplanation using OpenAI API
    explanation = get_explanation_from_openai(cm_list, metrics)

    return jsonify({
    "prediction": int(prediction),
    "explanation": explanation,
    "confusion_matrix": cm_list,
})
   return jsonify({
        "prediction": int(prediction),
        "explanation": explanation,
        "confusion_matrix": cm_list,
    })
   x

    
'''