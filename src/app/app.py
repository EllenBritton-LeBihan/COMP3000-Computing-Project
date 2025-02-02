from flask import request, render_template, Flask, flash, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
import email
import re
import pickle
import textstat

#tryig again with new model, ignored last flask integration for now

app = Flask(__name__)
app.secret_key = "secret_key"
#load new model
with open("rf_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

ALLOWED_EXTENSIONS = {'eml', 'txt', 'html'}

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#ensure upload folder exists.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#func to extract email text from .eml files
def extract_email_text(file_path):
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f)
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
    num_urls = len(re.findall(r"https?://\S+", text)) #find all occurences, contnue /w NON-whitespace chars
    avg_url_lngth = sum(len(url) for url in re.findall(r"https?://\S+", text)) / num_urls if num_urls > 0 else 0
    #calc total lngth of all urls ensure div by 0 doesnt happen. return 0 if no urls found.
    num_special_chars = len(re.findall(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`]", text))#count n of special char
    bigram_count = len(re.findall(r"\b\w+\s\w+\b", text))  
    trigram_count = len(re.findall(r"\b\w+\s\w+\s\w+\b", text))  

    
    #linguistic/punctuation features
    avg_sentence_lngth = sum(len(sentence.split()) for sentence in text.split('.')) / (len(text.split('.')) + 1) if len(text.split('.')) > 0 else 0 
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
    return pd.DataFrame([[avg_sentence_lngth, avg_word_length, punctuation_count,
                          exclamation_count, question_count, uppercase_ratio,
                          bigram_count, trigram_count, num_urls, avg_url_lngth,
                          imperative_word_count, politeness_word_count, num_special_chars,
                          readability_score, num_shortened_urls]],
                        columns=["avg_sentence_lngth", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count", "trigram_count", "num_urls", "num_shortened_urls",
                                 "avg_url_lngth", "imperative_word_count", "politeness_word_count", "num_special_chars",
                                ])
#'avg_sentence_lngth', 'avg_word_length', 'punctuation_count', 'exclamation_count', 'question_count', 
# 'uppercase_ration', 'readability_score', 'bigram_count', 'trigram_count', 'num_urls', 'num_shortened_urls', 
# 'avg_url_lngth', 'imperative_word_count', 'politeness_word_count', 'num_special_chars'


@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None  # debugging

    if request.method == "POST":
        if "clear" in request.form:
            flash("Form cleared. You can upload a new file.", "info")
            return redirect(url_for('index'))
        

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

        email_text = extract_email_text(file_path)
        features = extract_features(email_text)
        print(f"Extracted Features: {features}")

        #feature consistency
        expected_features = ["avg_sentence_lngth", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count", "trigram_count", "num_urls", "num_shortened_urls",
                                 "avg_url_lngth", "imperative_word_count", "politeness_word_count", "num_special_chars",
                                ]
        
     
        for feature in expected_features:
            if feature not in features.columns:
                features[feature] = 0 

        features = features[expected_features]



        prediction = model.predict(features)[0]
        prediction_result = "Phishing Email" if prediction == 1 else "Legitimate Email"  
        print(f"Prediction: {prediction_result}")

        flash(f"Prediction: {prediction_result}", "success")  
        return redirect(url_for('index'))
    
    return render_template("index.html", prediction_result=prediction_result)


if __name__ == "__main__":
    app.run(debug=True)