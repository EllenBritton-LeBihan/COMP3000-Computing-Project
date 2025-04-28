from flask import Blueprint, request, render_template, current_app, F
import pandas as pd
from app.utils import preprocess_email, parse_eml_file, save_confusion_matrix, get_explanation_from_openai
import os
from flask import Flask
from werkzeug.utils import secure_filename
import email
import pickle
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score


#Archived script. Used in first iterations and "shaping" of the project.
#old routes

#load new model
with open("rf_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#ensure upload folder exists.

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#func to extract email text from .eml files
def extract_email_text(file_path):
    with open(file_path, "rb", encoding="utf-8", errors="ignore") as f:
        msg = email.message_from_file(f)
        email_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            email_body= msg.get_payload(decode=True).decode(errors="ignore")
    
    return email_body

#feature extraction func (to match trianing features)
def extract_features(text):
    num_urls = len(re.findall(r"https?://\S+", text))
    avg_url_length = sum(len(url) for url in re.findall(r"https?://\S+", text)) / num_urls if num_urls > 0 else 0
    num_special_chars = len(re.findall(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`]", text))

    return pd.DataFrame([[num_urls, avg_url_length, num_special_chars]],
                        columns=["num_urls", "avg_url_lngth", "num_special_chars"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files["files"]
        if file.filename == "":
            return "No selected fle"
        
        #save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        #extract text from email
        email_text = extract_email_text(file_path)

        #extract features
        features = extract_features(email_text)

        #predict phishing or not 
        prediction = model.predict(features)[0]

        #convert prediction to a label
        result = "Phishing Email!" if prediction == 1 else "Legitimate Email"

        return f"Prediciton: {result}"
    return render_template("templates/index.html")

if __name__ == "__main__":
    app.run(debug=True)





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