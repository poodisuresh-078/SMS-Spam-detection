# 🛡️ SMS Spam Detection & URL Malicious Classification Using Machine Learning

## 📌 Project Description

SMS Spam Detection & URL Malicious Classification is a Python-based web application that uses Machine Learning and Natural Language Processing (NLP) to detect spam messages and classify URLs as potentially malicious or legitimate.

The system helps users recognize unwanted messages and suspicious website links through a simple, interactive web interface.

## 🎯 Objectives

* Detect spam SMS messages using Machine Learning.
* Classify URLs based on suspicious characteristics.
* Apply NLP techniques to process text messages.
* Provide a user-friendly cybersecurity dashboard.
* Store previous scan results using SQLite.
* Demonstrate practical applications of Python and Machine Learning.

## 🚀 Features

### 📩 1. SMS Spam Detection

* Accepts SMS messages as input.
* Processes text using NLP techniques.
* Converts text into numerical features using TF-IDF.
* Uses a trained Multinomial Naive Bayes classifier.
* Predicts Spam or Not Spam.
* Displays the classification result.

### 🔗 2. Malicious URL Classification

* Accepts website URLs from users.
* Extracts URL-related features.
* Examines URL length, dots, hyphens, digits, and suspicious patterns.
* Uses a trained Random Forest classifier.
* Classifies URLs as Likely Legitimate or Potentially Malicious.
* Does not need to open submitted URLs to perform feature-based classification.

### 📊 3. Detection Dashboard

* Displays SMS and URL detection statistics.
* Provides separate sections for SMS and URL analysis.
* Presents results using a clean interface.
* Helps users understand detection activity.

### 🗃️ 4. Scan History

* Stores previous predictions in an SQLite database.
* Records scan timestamps and classification results.
* Displays historical scan information.
* Supports management of stored records.

### 📱 5. Responsive User Interface

* Built using HTML, CSS, and JavaScript.
* Includes input forms and result displays.
* Supports desktop and mobile screen sizes.
* Provides clear warnings for suspicious results.

## 🛠️ Technologies Used

| Technology              | Purpose                           |
| ----------------------- | --------------------------------- |
| Python 3                | Main programming language         |
| Flask                   | Web application framework         |
| Scikit-learn            | Machine Learning algorithms       |
| Pandas                  | Dataset processing                |
| NumPy                   | Numerical operations              |
| NLP                     | SMS text processing               |
| TF-IDF                  | Text feature extraction           |
| Multinomial Naive Bayes | SMS classification                |
| Random Forest           | URL classification                |
| SQLite                  | Scan history storage              |
| Joblib                  | Saving and loading trained models |
| HTML                    | Webpage structure                 |
| CSS                     | Styling and responsive design     |
| JavaScript              | Frontend interactions             |
| Git                     | Version control                   |
| GitHub                  | Source code hosting               |

## ⚙️ System Requirements

* Operating System: Windows, Linux, or macOS
* Python: Python 3
* Code Editor: Visual Studio Code
* Web Browser: Chrome, Edge, or Firefox
* Git: For version control and GitHub uploads
* Internet Connection: Required for initial package installation and dataset downloads

## 🧠 Machine Learning Algorithms

### 1. TF-IDF Vectorization

TF-IDF converts SMS text into numerical features that a Machine Learning model can process. It assigns weights to words based on their importance within the text and dataset.

### 2. Multinomial Naive Bayes

This algorithm is suitable for many text-classification tasks. It learns from labeled SMS messages and predicts whether a new message is spam or legitimate.

### 3. Random Forest Classifier

Random Forest combines predictions from multiple decision trees. It can classify URLs using extracted features such as URL length, number of dots, digits, and suspicious patterns.

**Note:** The selected algorithms must be implemented and trained in the actual project code.

## 🔄 Project Workflow

1. User enters an SMS message or URL.
2. Flask receives the submitted input.
3. The application validates and preprocesses the input.
4. Feature extraction converts the input into a suitable representation.
5. The trained Machine Learning model generates a prediction.
6. Flask sends the result to the webpage.
7. The application displays the result.
8. If enabled, the scan result is saved in SQLite.

## 📂 Dataset Requirements

### SMS Dataset

The SMS dataset should contain labeled messages.

Example structure:

| Message                           | Label |
| --------------------------------- | ----- |
| Congratulations! You won a prize. | Spam  |
| Hello, see you tomorrow.          | Ham   |
| Claim your free reward now!       | Spam  |

A suitable public dataset is the SMS Spam Collection dataset.

### URL Dataset

The URL dataset should contain website URLs and corresponding labels.

Example structure:

| URL                                  | Label      |
| ------------------------------------ | ---------- |
| https://www.example.com              | Legitimate |
| http://suspicious-example.test/login | Malicious  |

These rows are illustrative examples, not verified training records. Use a properly labeled dataset for actual training.

**Important:** Dataset quality strongly affects the reliability of the model. A URL's appearance alone cannot establish whether it is safe.

## 📈 Model Evaluation

Evaluate the trained models using:

* **Accuracy:** Overall proportion of correct predictions.
* **Precision:** Proportion of positive predictions that are correct.
* **Recall:** Proportion of actual positive cases detected.
* **F1-Score:** Harmonic mean of precision and recall.
* **Confusion Matrix:** Shows correct and incorrect classifications by class.

For security-related applications, precision and recall are important alongside accuracy, especially when the dataset contains imbalanced classes.

Do not report evaluation scores until the models have been tested on appropriate held-out data.

## ⚙️ Installation & Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/poodisuresh-078/SMS-Spam-Detection.git
cd SMS-Spam-Detection
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Environment on Windows

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Prepare the Datasets

Download the required datasets and place them in the appropriate project directories. Follow the dataset paths and column names expected by the training scripts.

### Step 6: Train the Models

If these training scripts exist in the repository:

```bash
python train_sms_model.py
python train_url_model.py
```

Confirm that the training process completes successfully and saves the model files.

### Step 7: Run the Flask Application

```bash
python app.py
```

### Step 8: Open the Application

Open the local address displayed in the terminal. It is commonly:

http://127.0.0.1:5000/

The application should display its dashboard if the configuration and dependencies are correct.

**Note:** The commands above assume that the repository contains the specified files. Adjust them if your actual project structure differs.

## 📁 Suggested Project Structure

```text
SMS-Spam-Detection/
│
├── app.py
├── train_sms_model.py
├── train_url_model.py
├── sms_detector.py
├── url_classifier.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── datasets/
│   └── README.md
│
├── models/
│   └── .gitkeep
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── sms_detection.html
│   ├── url_detection.html
│   ├── history.html
│   └── about.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

This is a suggested structure. The actual repository may contain different files.

## 🔐 Security Considerations

* Do not automatically open or execute submitted URLs.
* Validate user input before processing it.
* Use parameterized SQL queries.
* Avoid displaying unescaped user input in HTML.
* Do not store sensitive message content unnecessarily.
* Do not commit passwords, API keys, or private data.
* Treat model predictions as estimates rather than guarantees.

## ✅ Advantages

* Automates basic SMS spam classification.
* Helps identify potentially suspicious URLs.
* Combines text processing and Machine Learning.
* Provides fast predictions after models are trained.
* Offers a simple web interface.
* Demonstrates practical Python and cybersecurity skills.
* Can be extended with additional threat-detection features.

## 🌐 Applications

* Spam message filtering.
* Cybersecurity education.
* Suspicious URL screening.
* Phishing-awareness applications.
* Machine Learning demonstrations.
* Student projects and developer portfolios.

## 🔮 Future Enhancements

* Integrate reputable threat-intelligence services.
* Add multilingual SMS classification.
* Improve detection using larger, regularly updated datasets.
* Add secure user authentication.
* Develop an administrator dashboard.
* Improve visualization of detection statistics.
* Deploy the application to a cloud platform.
* Add automated model evaluation and retraining.
* Build a mobile-friendly application.

## 🎯 Conclusion

The SMS Spam Detection & URL Malicious Classification project demonstrates how Machine Learning and NLP can support the identification of spam messages and potentially malicious URLs.

By combining Python, Flask, Scikit-learn, and SQLite, the application provides a practical foundation for learning web development, data processing, and cybersecurity.

The system is intended as a screening tool and cannot guarantee that every malicious message or URL will be detected.

## 👨‍💻 Author

**Poodi Suresh Reddy**

GitHub:https://github.com/poodisuresh-078/SMS-Spam-detection
## 📜 License

This project can be distributed under the MIT License if an appropriate LICENSE file is added to the repository.

