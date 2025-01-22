import re

def preprocess_email(text):
   
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)  #rem HTML 
    text = re.sub(r'http\S+', '', text)  #rem links (for now)
    text = re.sub(r'[^a-z\s]', '', text)  #rem special chars
    return text