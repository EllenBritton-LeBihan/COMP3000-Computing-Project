import re
from email import message_from_bytes
import openai
from openai import OpenAI
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import os
from openai import OpenAI



def preprocess_email(text):
   
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)  #rem HTML 
    text = re.sub(r'http\S+', '', text)  #rem links (for now)
    text = re.sub(r'[^a-z\s]', '', text)  #rem special chars
    return text


def parse_eml_file(eml_content):
    
    msg = message_from_bytes(eml_content)
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode("utf-8")
    else:
        return msg.get_payload(decode=True).decode("utf-8")
    


#implementing openai api for better user exp
def get_explanation_from_openai(confusion_matrix_data):
    
    prompt = (
        f"Explain the following confusion matrix results to a non-technical user:\n\n"
        f"Confusion Matrix:\n"
        f"True Positive (TP): {confusion_matrix_data['TP']}\n"
        f"True Negative (TN): {confusion_matrix_data['TN']}\n"
        f"False Positive (FP): {confusion_matrix_data['FP']}\n"
        f"False Negative (FN): {confusion_matrix_data['FN']}\n\n"
        f"Metrics:\n"
        f"Precision: {confusion_matrix_data['precision']:.2f}\n"
        f"Recall: {confusion_matrix_data['recall']:.2f}\n"
        f"F1 Score: {confusion_matrix_data['f1_score']:.2f}\n"
        f"Accuracy: {confusion_matrix_data['accuracy']:.2f}\n\n"
        f"Provide the explanation in plain language suitable for a layperson."
    )
    
    try:
        
        openai.api_key= ""

        client = OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "developer", "content": "You are a helpful assistant who explains technical concepts to non-technical users."},
                {"role": "user", "content": prompt}
            ],
        )

        explanation = response.choices[0].message
        return explanation
    except openai.OpenAIError as e:
        #catch errors and rtrn
        return f"Error generating explanation: {str(e)}"


def save_confusion_matrix(y_true, y_pred, labels, output_path="static/confusion_matrix.png"):
   
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()