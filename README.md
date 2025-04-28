# 2024/2025-COMP3000-Computing-Project 

# PhishNet | A Context-Aware Phishing Detection Tool for Emails 

![Image](https://github.com/user-attachments/assets/3491a07c-1431-4e2f-bc56-f85cc84918c3)

![Static Badge](https://img.shields.io/badge/python-python?style=for-the-badge&logo=python&logoColor=22ffc4&label=Made%20With&labelColor=585873&color=22ffc4)
![Static Badge](https://img.shields.io/badge/Jupyter%20Notebook%20-%20Jupyter%20Notebook?style=for-the-badge&logo=jupyter&label=MADE%20WITH&labelColor=585873&color=0900FF)
![Static Badge](https://img.shields.io/badge/JavaScript%20-%20JavaScript?style=for-the-badge&logo=javascript&label=MADE%20WITH&labelColor=585873&color=F5E101)
![Static Badge](https://img.shields.io/badge/HTML%20-%20HTML?style=for-the-badge&logo=html5&label=MADE%20WITH&labelColor=585873&color=E0F0FF)
![Static Badge](https://img.shields.io/badge/CSS%20-%20CSS?style=for-the-badge&logo=css&label=MADE%20WITH&labelColor=585873&color=E4917E)

PhishNet is a machine learning-powered web app designed to detect phishing emails by analysing their content and header signals with the Random Forest Classifier. Upload .eml, files to receive a phishing prediction along with clear explanations of the results.



## INSTALLATION
	1. Clone the repository into your file system >> command >> git clone --recursive <repo name>
	2. Ensure Python 3.9+ is installed.
	3. Install the required dependencies using >> pip install -r requirements.txt
	4. Launch the application by running >> python app.py
    5. Access the web app at http://127.0.0.1:5000/ in your browser.



## USAGE 

demo of phishing email upload and detection.

![Image](https://github.com/user-attachments/assets/ba3bc4a2-f020-4f76-bad6-a2fcf2a3a80f)

TOOL AIM: Analyses email file. Checks for authentication failures and suspicious language patterns. Detects label (phishing or legitimate).

### SUPPORTED FILE FORMATS
* .eml

### HOW TO USE

	1. Start the application locally.
	2. On the main page (Checker), upload an email file (supported format only).
	3. Click "Check".
	4. View prediciton results:
   		- Phishing or Legitimate
   		- Suspicion Score (%)
   		- Clear reasoning (Language, Urgency, Tone)
	5. Optionally, clear history and upload a new email.
	6. History page available to review previous uploads.



### PREDICTION DETAILS

* Language Analysis:
  - Detects urgency, imperative words, suspicious patterns.
* Authentication Checks:
  - Analyses SPF, DKIM, DMARC headers.
* Attachment Risk
  - Flag potentially dangerous file types like .exe, .scr, .bat.
* Feature Analysis:
  - Analyses sentence length, word length, punctuation, URL frequency, and other linguistic patterns.
* Suspicion Score
  -  Calculated based on the model's prediction probability, presented as a percentage.
  -  High Suspicion (score ≥ 60%)
  -  Medium Suspicion (score 40-60%)
  -  Low Suspicion (score ≤ 40%)
* Prediction Output
  - The email is labelled as either "Phishing" or "Legitimate" based on the model's decision.



## ADVANCED/EXTRAS
### ADVANCED FEATURES IMPLEMENTED

Suspicion Scoring System
* Emails are assigned a Suspicion Score based on model output probabilitys.
* Session-based history tracking.
* Dynamic Reasoning.

## TECHNOLOGIES USED
* Python (Flask, scikit-learn, pandas, numpy)
* Jupyter Notebook (For data pre-processing and model training)
* HTML/CSS/JavaScript (Figma-inspired front-end)

## REQUIREMENTS 
* Python 3.9+
* Flask
* pandas
* scikit-learn
* textstat
* numpy
* Werkzeug



## FUTURE IMPROVEMENTS

1. Real-time email scannig and integration
   - Integrate real-time email scanning, allowing automatic evaluation of incoming emails for phishing threats, with potential integration into major email platforms.
2. UI and Accessibility Improvement
   - Enhance the user interface to support advanced accessibility features such as screen readers and responsive layouts for better usability.
3. Additional advanced features such as:
   - Provide optional display of visually highlighted suspicious phrases or keywords in the email body for better user interaction and easier understanding.
   - User visible authentication results. Shows which authenticators were flagged.
   - Integrate an AI-chatbot for clearer explainability of results.



## THIRD-PARTY LICENSES

This project uses [Textstat](https://pypi.org/project/textstat/) (© 2024 Textstat Developers) for computing readability scores.
Textstat is licensed under the [MIT License](https://opensource.org/licenses/MIT), which allows for free use, modification, and distribution, provided the original license and attribution are maintained.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


### Dataset Sources:


#### Phishing Email Dataset
By Naser Abdullah Alam, available on Kaggle under the CC BY-SA 4.0 license.  

The machine learning model in this project was trained and validated using the publicly available [**Phishing Email Dataset**](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset) hosted on Kaggle (Alam, 2024).  
This dataset is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license.
> This means it can be used for educational and research purposes, with appropriate credit. Any derivative work must also be shared under the same license, and is restricted to **non-commercial** use.

Proper attribution has been given to the original author, and usage in this project remains aligned with the dataset’s licensing terms.


#### Enron Email Dataset
Earlier stages of development made use of the **Enron Email Dataset**, originally compiled and released by the **CALO Project** at **Carnegie Mellon University (CMU)**. The dataset was made public as part of the U.S. **Federal Energy Regulatory Commission’s** investigation and was intended for academic and scientific research.

For this project, the dataset was accessed via [**Kaggle**](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset) (Wcukierski, 2019), where it is available for research and educational use.

> Attribution has been provided to both the original dataset creators and the Kaggle uploader. This dataset was used only for **non-commercial educational** purposes in accordance with its licensing terms.
**Note**: The Enron dataset was used only in early development stages and is not part of the final deployed version of this project.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


### BSD 3-Clause License
This project incorporates several open-source libraries (see below), all of which are distributed under the BSD 3-Clause License [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause), a permissive license that allows for use, redistribution, and modification with attribution.


### Flask
Copyright 2010 Pallets  
https://flask.palletsprojects.com/

### Pandas
Copyright (c) 2008-2024, pandas development team  
All rights reserved.  
https://pandas.pydata.org/

### NumPy
Copyright (c) 2005-2024, NumPy Developers  
All rights reserved.  
https://numpy.org/

### Werkzeug
Copyright 2007 Pallets  
https://palletsprojects.com/p/werkzeug/

### Scikit-learn
© 2007–2024 Scikit-learn Developers  
https://scikit-learn.org/  



----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


