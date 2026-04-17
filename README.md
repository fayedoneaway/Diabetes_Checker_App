
1. OVERVIEW:
This project predicts diabetes or no diabetes based on the person's 
age, bmi, glucose level and symptoms.

This is from my project where I compared Naive Bayes and Logistic Regression 
with L2 regularization for the Pima Indians Diabetes Dataset.

For the purposes of making this application, I retrained the model on 
Logistic Regression using only three features: age, bmi and glucose.


2. DATASET:
 - Pima-Indians-Diabetes Dataset from Kaggle


3. MODEL USED:
 - Logistic Regression with L2 Regularization


4. DATA INSPECTION/PREPROCESSING:
 - The CSV I downloaded didn’t include column headers, so I looked up the correct feature names and added them to the dataset.

 - The CSV doesn’t contain any NaN values, but several medical measurement columns use 0 as a placeholder for missing data. 
   Since values like 0 for glucose, blood pressure, BMI, insulin, and skin thickness are not physiologically possible, 
   these zeros need to be treated as missing values.

 - Based on my research, the following columns should never contain a value of 0: 
   Glucose, BloodPressure, SkinThickness, Insulin, and BMI. 

   In the original dataset, zeros in these fields represent missing or unrecorded measurements, 
   not valid physiological values.

 - I converted the zeros in these medical measurement columns to NaN so that I could properly treat them 
    as missing values and later impute them using an appropriate statistic.

 - To choose the appropriate imputation statistic, I examined the distribution of each column. 
   Mean imputation is generally suitable for roughly Gaussian or symmetric distributions, 
   while median imputation is preferred for skewed distributions or those containing outliers.

 - After reviewing the distributions, I found that most columns, except BloodPressure, were noticeably skewed. 
   Because skewed medical variables often contain outliers and long tails, I used the median for imputation. 
   The median is more robust than the mean in these situations and provides a more reliable central tendency for skewed data.

 
5. FIT: 
 - Before imputing missing values, I first split the dataset into training and validation sets to avoid data leakage. 

   If I were to fill in missing values before splitting, the imputation statistics would be computed using 
   information from the entire dataset, giving the model an unintended preview of the validation data. 

- When splitting the data, I used the stratify parameter because the dataset is imbalanced: 
  there are significantly more patients without diabetes than with diabetes. 

  Stratified splitting preserves this class distribution in both the training and validation sets, 
  ensuring that each split reflects the original imbalance. I also considered the skewness and 
  imbalance of each feature distribution when planning the rest of my preprocessing workflow.

- After splitting the data, I imputed the missing values using the median and then normalized the numerical features. 

  Logistic Regression benefits from normalization because it helps stabilize the 
  optimization process and helps the L2 regularizer behave consistently across features.


6. TRAIN: 
 - Logistic Regression applying L2 Regularization.
 - I used an L2 penalty because I wanted the model to retain all features rather than zeroing out coefficients. 
   Even if some features are weak individually, they still contribute useful signal when combined with others, 
   and L2 regularization shrinks weights without eliminating them.
 - Logistic Regression performed better than Naive Bayes on the following metrics: f1 score, accuracy and confusion matrix.
   But produced the same results for ROC AUC.



 - LOGISTICS REGRESSION WITH L2 REGULARIZATION:
    Metrics Compared:
	accuracy: 0.7077922077922078
	f1 score:0.6017699115044248
	ROAC AUC: 0.7292592592592593
	Confusion Matrix: 75 25
  			  26 28


 - TRAINING CONCLUSION: 
 - Although not on this notebook, I initially trained this dataset on Naive Bayes.
 - I expected Naïve Bayes to perform well on this dataset because it uses a probabilistic approach. 
  However, the dataset is imbalanced, with far more non‑diabetic patients than diabetic ones, and Naïve Bayes tends 
  to lean heavily toward the majority class. As a result, it correctly predicts many ‘no diabetes’ cases but struggles 
  to identify diabetic patients, which is reflected in its low F1 score. 

 - The core issue is that Naïve Bayes assumes feature independence, which is not true for this dataset.
 Since many medical features are correlated, it cannot model these relationships. 
 The Naive Bayes model collapses toward the majority class and underperforms on the positive class.


  - Logistic Regression performed better on this dataset because it can take advantage of the correlations 
 between features rather than ignoring them. Unlike Naïve Bayes, it does not assume independence, 
 so it can use those relationships to form a more accurate decision boundary. 

  - Applying L2 regularization further stabilizes the model by shrinking coefficients and preventing variance 
 from exploding in the presence of noise or multicollinearity. As a discriminative model, 
 Logistic Regression directly learns the boundary between diabetic and non‑diabetic patients. 

 - While both models predicted the ‘no diabetes’ class similarly, Logistic Regression was significantly better 
 at identifying actual diabetic patients.
 

7. LOADING MODEL:
the model is saved using
joblib.dump(model, "logreg_3feature.pkl)

loaded in backend using:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "logreg_3feature.pkl")
model = joblib.load(model_path)


8. PROJECT ARCHITECTURE
DiabetesCheckerApp/
├── backend/
│   ├── backend_app.py
│   ├── model.py
│   ├── logic.py
│   ├── logreg_3feature.pkl
│   └── requirements.txt
├── frontend/
│   └── frontend_app.py
│   └── requirements.txt
└── notebooks/
│   └── Pima_Indians_Diabetes.ipynb
└── docs
│   └── diabetes checker screenshot.pdf
└── README.md
└── .gitignore

9. INSTALLATION
 - git clone https://github.com/fayedoneaway/repository/Diabetes_Checker_App
 - cd Diabetes_Checker_App
 - python -m venv venv
 - venv\Scripts\activate (windows)
 - source venv/bin/activate (mac or linux)
 - pip install -r backend/requirements.txt
 - pip install -r frontend/requirements.txt

10. RUN 
 a. backend
 - uvicorn backend.backend_app:app --reload
   http://127.0.0.1:8000/docs

 b. frontend
 - streamlit run frontend/frontend_app.py


11. MECHANICS
 - "bmi": 55
 - "age":
 - "glucose":
 - "Enter symptoms: Frequent Urination", Sudden loss of weight, Increased thirst or hunger, Nausea and Vomiting, Blurry Vision, Urinary Tract Infection"


12. REQUIREMENTS 
 a. backend
 - fastapi
 - uvicorn
 - scikit-learn
 - numpy
 - pandas
 - matplotlib
 - joblib

 b. frontend
 - streamlit
 - requests
