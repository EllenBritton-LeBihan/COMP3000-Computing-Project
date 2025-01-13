from flask import Flask, request, render_template, jsonify
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer

app=Flask(__name__)

rf_model = joblib.load('random_forest_model.pkl')

#load TFIDF vectorizer (used during training)
vectorizer = joblib.load('tfidf_vectorizer.pkl')  

#function to clean and preprocess email content
def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)  #remove HTML tags
    text = re.sub(r'http\S+', '', text)  # remove urls
    text = re.sub(r'[^a-z\s]', '', text)  #remove nonalphabetic chars
    return text

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    #GET email content from form
    email_content = request.form['email_content']

    #preprocess email
    processed_email = preprocess_email(email_content)

    #transform with TF-IDF vectorizer
    email_features = vectorizer.transform([processed_email])

    #predict with RF model
    prediction = rf_model.predict(email_features)

    #return 
    result = 'Phishing Email Detected!' if prediction[0] == 1 else 'Email is Safe.'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)