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
import numpy as np
from datetime import datetime #to add datetime to history page.


#updated code organisation, this is now primary app.py

app = Flask(__name__)
app.secret_key = "secret_key"

#load the trained model
with open("rf_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
#load vectorizer
with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)#

#load trigram vectorizer
#with open("trigram_vectorizer.pkl", "rb") as trigram_vec_file:
    #trigram_vectorizer = pickle.load(trigram_vec_file)



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
    
   
    headers = dict(msg.items()) #to dict
    auth_res = headers.get("authentication-Results", "").lower()

    

    dkim_fail = "dkim=fail" in auth_res
    spf_fail = "spf=fail" in auth_res
    dmarc_fail = "dmarc=fail" in auth_res

    y_true_label = 1 if dkim_fail or spf_fail or dmarc_fail else 0

    return email_body, y_true_label # should return exactly 2 vals



def calc_sus_score(ml_prob):
    #need to compute sus score based on the ml model probabilty output.
    if ml_prob >= 0.8:
        severity = "High"
        score = 5
    elif ml_prob >= 0.6:
        severity = "Medium"
        score = 3
    elif ml_prob >= 0.4:
        severity = "Low"
        score = 1
    else:
        severity = "None"
        score = 0
    
    return score, severity

#for sus email content to be highlighted for better user interaction.
'''def highlight_sus_content(email_text, vectorizer, trigram_vectorizer, model):
    
    #get feature names from both vects
    bigram_words= vectorizer.get_feature_names_out()
    trigram_words = trigram_vectorizer.get_feature_names_out()

    all_words = np.concatenate([bigram_words, trigram_words]) #merge feature names

    #compute the feature importance from rf
    feature_importances = np.mean([tree.feature_importances_ for tree in model.estimators_], axis=0)

    #get top 10 sus words
    top_sus_words = [all_words[i] for i in np.argsort(feature_importances)[-10]]
    #highlight top sus words in email text
    for word in top_sus_words:
        email_text = re.sub(f"({word})", r'<span style="background-color: #FFD700;">\1</span>', email_text, flags=re.IGNORECASE)



    #highlighted words based on importance in ml model
    words = vectorizer.get_feature_names_out()
    
    #calc feature importance form RF model
    feature_importances = np.mean([tree.feature_importances_ for tree in model.estimators_], axis=0)
    top_sus_words = [words[i] for i in np.argsort(feature_importances)[-10:]] #tje top 10 indicators.
    #highlihgt the top sus words.
    for word in top_sus_words:
        email_text = re.sub(f"({word})", r'<span style="background-colour: #FFD700;">\1<span>', email_text, flags=re.IGNORECASE)
    
    return email_text
'''

#feature extraction func (to match trianing features)
def extract_features(text):
    num_urls = len(re.findall(r"https?://\S+", text)) #find all occurences, contnue /w NON-whitespace chars
    avg_url_lngth = sum(len(url) for url in re.findall(r"https?://\S+", text)) / num_urls if num_urls > 0 else 0
    #calc total lngth of all urls ensure div by 0 doesnt happen. return 0 if no urls found.
    num_special_chars = len(re.findall(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`]", text))#count n of special char
    
    #bigram trigram count
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

    #convert txt features to vectors with bigram/trigram vectorizers.
    bigram_features = vectorizer.transform([text]).toarray()
    #trigram_features = trigram_vectorizer.transform([text]).toarray()

    #return combined array of features merging linguistic and structual features
    combined_features = np.hstack([ #stack extracted scalar feat to single array.
        np.array([[avg_sentence_length, #avg sentence length (words)
                   avg_word_length, #avg word lengths (char)
                   punctuation_count, #total punctuation marks (text)
                   exclamation_count, #n of !
                   question_count,  #n of  ?
                   uppercase_ratio, #ratio of uppercase letters to total chars
                   bigram_count, #count of bigrams in txt
                   #trigram_count, #count of trigrams in txt
                   num_urls, #n of urls in text
                   avg_url_lngth, #avg lngth of urls found in txt
                   imperative_word_count, #count of command-like words
                   politeness_word_count, #count of polite words 
                   num_special_chars, #count of special chars 
                   readability_score, #computed readability score of text
                   num_shortened_urls]]),  #count of shortened urls 

        #appeneded vectorized bigram/trigram features
        bigram_features,
    #   trigram_features
    ])

    #define olumn names for DF
    feature_columns = [
        'avg_sentence_length', 'avg_word_length', 'punctuation_count', 'exclamation_count', 'question_count',
        'uppercase_ratio', 'bigram_count', 'num_urls', 'avg_url_length', 'imperative_word_count',
        'politeness_word_count', 'num_special_chars', 'readability_score', 'num_shortened_urls'
    ]

    #append bi/trigram column names
    bigram_columns = [f'bigram_{i+1}' for i in range(bigram_features.shape[1])]
    #trigram_columns = [f'trigram_{i+1}' for i in range(trigram_features.shape[1])]

    #merge
    all_columns = feature_columns + bigram_columns 

    #convert to DF
    feature_df = pd.DataFrame(combined_features, columns=all_columns)

    return feature_df


    ''' REMOVE
    return pd.DataFrame([[avg_sentence_length, avg_word_length, punctuation_count,
                          exclamation_count, question_count, uppercase_ratio,
                          bigram_count, trigram_count, num_urls, avg_url_lngth,
                          imperative_word_count, politeness_word_count, num_special_chars,
                          readability_score, num_shortened_urls]],
                        columns=["avg_sentence_length", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count", "trigram_count", "num_urls", 
                                 "num_shortened_urls", "avg_url_lngth", "imperative_word_count", 
                                 "politeness_word_count", "num_special_chars",
                                ])
'''


#route
@app.route("/", methods=["GET", "POST"])
def index():
    session.setdefault("y_true", [])
    session.setdefault("y_pred", [])

    prediction_result = None  # debugging

    #issue with "clear" btn sometimes !!
    if request.method == "POST":
        if "clear" in request.form:
            session["y_true"].clear() #might fix clear btn issues
            session["y_pred"].clear()
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
        
        
        #secure file save
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)


        #extract email txt & auth res
        email_text, y_true_label = extract_email_text(file_path)

        #extract featres using both of the vectorizers
        features_df = extract_features(email_text)

        #checks for if features_df is a DF 
        if not isinstance(features_df, pd.DataFrame):
            flash("Error: Features extraction returned invalid format.", "error")
            return redirect(url_for('index'))
        #check if correct shape
        print(f"Expected features shape: {features_df.shape}")
        #features_df = features_df.values #cnvrt to 2d numpy array.
    
    

         #feature consistency
        expected_features = ["avg_sentence_length", "avg_word_length", "punctuation_count",
                                 "exclamation_count", "question_count", "uppercase_ration",
                                 "readability_score", "bigram_count",  "num_urls", "num_shortened_urls",
                                 "avg_url_lngth", "imperative_word_count", "politeness_word_count", "num_special_chars",
                                ]
        
        
        '''#validate compatibility, replaces "expected_features"
        if features.shape[1] != model.n_features_in_:
            flash("Features mismatch error! Model expects different input features.")
            return redirect(url_for('index'))
        
        print("Extracted Features:", features)
'''

        #unpack 2 vals 
        #email_text, y_true_label = extract_email_text(file_path)
       
    
        #extract features predict us
        for feature in expected_features:
            if feature not in features_df.columns:
                features_df[feature] = 0 

        feature_df = features_df[expected_features]


    #to handle empty feature instances
        if features_df.empty:
            flash("Error extracted features are empty", "error")
            return redirect(url_for('index'))

    #predict phishing
        prediction = model.predict(feature_df)[0]

        #predict probabilities of phishing
        probabilities = model.predict_proba(feature_df)[0]  
        phishing_prob = probabilities[1]
    
        #compute sus score
        sus_score = int(phishing_prob *100) # cvrts prob to a percentage
        
        prediction_res = "Phishing Email" if prediction == 1 else "Legitimate Email"
        #debug
        print(f"Prediction result (scalar): {prediction}")
        print(f"Prediction: {prediction_res}")
        print(f"Suspicion Score: {sus_score}%")


        #highlihg sus words
        #highlighted_email = highlight_sus_content(email_text, vectorizer, trigram_vectorizer, model)

        #Add to history here
        history.append({"filename": filename,
                        "sus_score": sus_score,
                        "prediction": prediction_res,
                        "date": datetime.now().strftime("%m/%d/%Y")
                        })
        
#fix y_true_label -- update data for session
        session["y_true"].append(int(y_true_label)) #to int to fix TypeError
        session["y_pred"].append(int(prediction))
        session.modified = True

        #debug
        print(f"Session y_true: {session['y_true']}")
        print(f"Session y_pred: {session['y_pred']}")
        #debig
        print(f"y_true_label: {y_true_label}") 
        print(f"Updated y_true: {session['y_true']}")
        print(f"Updated y_pred: {session['y_pred']}")



        #ceck that y_true and y_pred match ok
        #Maybe problem here since returns bool.Review this.
        if len(session["y_true"]) != len(session["y_pred"]):
            flash("Warning y_true and y_pred lengths don't match.", "warning")
            session["y_true"].clear()
            session["y_pred"].clear()
            return redirect(url_for('index'))
       

        # ------- Authentication reasoning logic --------- 
        #evaluate ground truth label for phishing classification
        #if y_true_label == 1, sample is a confirmed phishing email
        #assign static reason to for failure of email auth protocols.
        reason_auth = ""
        #reason_sender = ""
        reason_language = ""
        reason_attachments = ""
        #reason_subject = ""

        if y_true_label == 1: #y_true_label = 1 when one of the three auth fails.
            #Authentication failure, failure suggests spoofed or untrusted origns.
            reason_auth = "The email failed SPF/DKIM/DMARC authentication checks."
        
        #---Language based risk---
        #>0.5       :High risk
        #0.4 - 0.5  :Moderate risj
        #<0.4       :low risk

        if phishing_prob > 0.5:
            #higher probability
            reason_language = "High urgency detected in the language, suggesting a potential phishing attempt."
        
        elif 0.4 <= phishing_prob <= 0.5:
            reason_language = "Moderate urgency and suspicious language patterns detected."
        
        else:
            reason_language = "Low levels of urgency in the language, but some suspicious cues still present."

        #---Attachment based risk
        #lowercased normalisation for better matching
        if any(ext in filename.lower() for ext in ['.ext', 'scr', ',bat']):
            reason_attachments = "The email contains potentially dangerous attachemnets."

        #flash prediction msg
        flash(f"Prediction: {prediction_res}, (Suspicion Score: {sus_score})", "success") 
        session["last_prediction"] = prediction_res
        session["last_sus_score"] = sus_score

        #POST return
        return render_template("index.html", 
                               prediction_res=prediction_res, 
                               sus_score=sus_score,
                               uploaded_filename=filename, #for stopping form and label reloading on "check"
                               reason_auth=reason_auth,
                               reason_language=reason_language,
                               reason_attachments = reason_attachments)
    
    #GET retunr
    return render_template("index.html", 
                           prediction_res=session.get("last_prediction"), 
                           sus_score=session.get("last_sus_score"),
                           reason_auth=session.get("last_reason_auth"),
                           reason_language=session.get("last_reason_language"),
                           reason_attachments=session.get("last_reason_attachments"))

#route for history
@app.route("/history")
def history_page():
    return render_template("history.html", history=history) #load history.html to display

if __name__ == "__main__":
    app.run(debug=True)