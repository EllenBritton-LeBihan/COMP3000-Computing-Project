import re
from email import message_from_bytes
import openai
from openai import OpenAI
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import os


#keeping utils here for potential integration of OpenAI API since this file was used for the "old" app.py
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
def get_explanation_from_openai(confusion_matrix, metrics):
    from openai import OpenAI

    true_positive = confusion_matrix[1][1]
    true_negative = confusion_matrix[0][0]
    false_positive = confusion_matrix[0][1]
    false_negative = confusion_matrix[1][0]
    
    prompt = (
        "Analyze and explain the following confusion matrix and metrics in a simple, user-friendly way for a non-technical audience:\n\n"
        "Confusion Matrix:\n"
        f"\tPredicted: Not Phishing\tPredicted: Phishing\n"
        f"Actual: Not Phishing\t{true_negative}\t\t\t{false_positive}\n"
        f"Actual: Phishing\t\t{false_negative}\t\t\t{true_positive}\n\n"
        "Metrics:\n"
        f"- True Positive: {metrics['True Positive']}\n"
        f"- True Negative: {metrics['True Negative']}\n"
        f"- False Positive: {metrics['False Positive']}\n"
        f"- False Negative: {metrics['False Negative']}\n"
        "Provide a concise explanation of the performance of this model."
    )
    """
    might change my mind later about using an image.
    #get path for img
    crt_dir = os.path.dirname(__file__)
    image_file_path = os.path.join(crt_dir, "static", "imgs", "confusion_matrix.png")



    #encode to base64 and check if the file exists
    if os.path.exists(image_file_path):
        with open(image_file_path, "rb") as image_file:
            base64_encoded_img = base64.b64encode(image_file.read()).decode("utf-8")
    else:
        return f"File not found: {image_file_path}"
    """

    #init openai
    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  
            max_tokens=300, #increase if getting cut off
            messages=[
                {
                    "role": "system", "content": "You are a helpful assistant specializing in machine learning explanations."
                },
                {
                    "role": "user", "content": prompt
                }
            ],
        )

        explanation = response.choices[0].message.content
        return explanation
    
    except Exception as e:
        #catch errors and rtrn
        return f"Error generating explanation: {str(e)}"


def save_confusion_matrix(y_true, y_pred, labels, output_path="static/imgs/confusion_matrix.png"):
   
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()