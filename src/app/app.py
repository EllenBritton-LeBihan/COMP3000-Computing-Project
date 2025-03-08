from flask import request, render_template, Flask, flash, redirect, url_for, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
import email
import re
import pickle
import textstat
import email
import email.policy
from datetime import datetime #to add datetime to history page.


#updated code organisation, this is now primary app.py

app = Flask(__name__)
app.secret_key = "secret_key"

#load the trained model
with open("rf_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

ALLOWED_EXTENSIONS = {'eml', 'txt', 'html'}

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#ensure upload folder exists.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#to store histroy of predictions
history = []


#ARCHIVED store predictions history for confusion matrix -- not using a conf matrix anymore.
session_data = {"y_true": [], "y_pred": []}

#func to extract email text from .eml files
def extract_email_text(file_path):
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

        #mke sure integrates with imported figma index.html
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain": 
                    email_body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            email_body= msg.get_payload(decode=True).decode(errors="ignore")
    

    #extract auth 
    dkim_pass = False
    spf_pass = False
    dmarc_pass = False

    headers = dict(msg.items()) #to dict
    auth_res = headers.get("authentication-Results", "")

    #check res
    if "dkim=pass" in auth_res:
            dkim_pass = True
    if "spf=pass" in auth_res:
        spf_pass = True
    if "dmarc=pass" in auth_res:
        dmarc_pass = True   

    y_true_label = 0 if dkim_pass and spf_pass and dmarc_pass else 1

    return email_body, y_true_label # should return exactly 2 vals


#feature extraction func (to match trianing features)
def extract_features(text):
    num_urls = len(re.findall(r"https?://\S+", text)) #find all occurences, contnue /w NON-whitespace chars
    avg_url_lngth = sum(len(url) for url in re.findall(r"https?://\S+", text)) / num_urls if num_urls > 0 else 0
    #calc total lngth of all urls ensure div by 0 doesnt happen. return 0 if no urls found.
    num_special_chars = len(re.findall(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`]", text))#count n of special char
    bigram_count = len(re.findall(r"\b\w+\s\w+\b", text))  
    trigram_count = len(re.findall(r"\b\w+\s\w+\s\w+\b", text))  

    
    #linguistic/punctuation features
    avg_sentence_length = sum(len(sentence.split()) for sentence in text.split('.')) / (len(text.split('.')) + 1) if len(text.split('.')) > 0 else 0 
    #for each sentence n of words counted and calc avg. div by n of sentences.
    avg_word_length = sum(len(word) for word in text.split()) / (len(text.split()) + 1) if len(text.split()) > 0 else 0
    #split text into words sum lngths div total n of words.
    punctuation_count = len(re.findall(r"[,.!?;]", text))
    exclamation_count = text.count('!')#use count() 
    question_count = text.count('?')#use count() 
    uppercase_ratio = sum(1 for char in text if char.isupper()) / (len(text) + 1) if len(text) > 0 else 0 #div by tot text lngth

    #placeholder politeness/immediate action words (extend later on)
    #list imp../poli.._words
    imperative_words = ["click", "hurry", "act", "now", "urgent"]
    politeness_words = ["please", "thank you", "regards", "kind regards", "many thanks", "dear"]
    imperative_word_count = sum(text.lower().count(word) for word in imperative_words) 
    politeness_word_count = sum(text.lower().count(word) for word in politeness_words)

    #higher score = easier to read
    readability_score = textstat.flesch_reading_ease(text)
    num_shortened_urls = len(re.findall(r"https?://(?:bit\.ly|t\.co|goo\.gl)/\S+", text))

    #return 
    return pd.DataFrame([[avg_sentence_length, avg_word_length, punctuation_count,
                          exclamation_count, question_count, uppercase_ratio,
                          bigram_count, trigram_count, num_urls, avg_url_lngth,
                          imperative_word_count, politeness_word_count, num_special_chars,
                          readability_score, num_shortened_urls]],
                        columns=["avg_sentence_length", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count", "trigram_count", "num_urls", "num_shortened_urls",
                                 "avg_url_lngth", "imperative_word_count", "politeness_word_count", "num_special_chars",
                                ])


#route
@app.route("/", methods=["GET", "POST"])
def index():
    session.setdefault("y_true", [])
    session.setdefault("y_pred", [])

    prediction_result = None  # debugging

    #issue with "clear" btn sometimes !!
    if request.method == "POST":
        if "clear" in request.form:
            session["y_true"]
            session["y_pred"]
            flash("Form cleared. You can upload a new file.", "info")
            return redirect(url_for('index'))
        
        #logic SHOULD be fine for integration
        if "file" not in request.files:
            flash("No file uploaded", "error")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)
        
        

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        #unpack 2 vals 
        email_text, y_true_label = extract_email_text(file_path)


        #feature consistency
        expected_features = ["avg_sentence_length", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count", "trigram_count", "num_urls", "num_shortened_urls",
                                 "avg_url_lngth", "imperative_word_count", "politeness_word_count", "num_special_chars",
                                ]
        
        features = extract_features(email_text)
        print(f"Extracted Features:", features.shape)

        #extract features predict us
        for feature in expected_features:
            if feature not in features.columns:
                features[feature] = 0 
        features = features[expected_features]

        if features.empty:
            flash("Error extracted features are empty", "error")
            return redirect(url_for('index'))
        

        prediction = model.predict(features)[0]
        prediction_result = "Phishing Email" if prediction == 1 else "Legitimate Email"  
        print(f"Prediction: {prediction_result}")
        
        #Add to history here
        history.append({"filename": filename, 
                        "prediction": prediction_result,
                        "date": datetime.now().strftime("%m/%d/%Y")
                        })
        

        session_data["y_true"].append(y_true_label)
        session_data["y_pred"].append(prediction)
        session.modified = True
        #debig
        print(f"y_true_label: {y_true_label}") 
        print(f"Updated y_true: {session_data['y_true']}")
        print(f"Updated y_pred: {session_data['y_pred']}")


        #gen confusion matrix only if at least 2 predictions exist
        if len(session_data["y_true"]) > 1 != len(session_data["y_pred"]):
            flash("Warning y_true and y_pred lengths don't match.", "warning")
            session_data["y_true"].clear()
            session_data["y_pred"].clear()
            return redirect(url_for('index'))
        
            
        flash(f"Prediction: {prediction_result}", "success") 
        session["last_prediction"] = prediction_result

        #return redirect(url_for('label_email'))
        return redirect(url_for('index'))
    
    
    

    return render_template("index.html", prediction_result=session.get("last_prediction"))

#route for history
@app.route("/history")
def history_page():
    return render_template("history.html", history=history) #load history.html to display

if __name__ == "__main__":
    app.run(debug=True)