import joblib
import pandas as pd

class Diabetes:
    def __init__(self):
        self.model = joblib.load("logreg_3feature.pkl")


    def prediction(self, bmi, age, glucose):
        data = pd.DataFrame([[bmi, age, glucose]],
                            columns=["BMI", "Age", "Glucose"])
        probs = self.model.predict_proba(data)[0]
        preds = self.model.predict(data)[0]

        if max(probs) < 0.6:
            print("Model cannot make confident diagnosis. A medical check is needed to be sure.")
        elif preds == 0:
            print(f"Model has {max(probs) * 100:.1f}% confidence: low diabetes risk.")
        elif preds == 1:
            print(f"Model has {max(probs) * 100:.1f}% confidence: high diabetes risk.")

        return preds, max(probs), probs


    def try_again(self, answer):
        answer = answer.strip().lower()
        if answer in ["y", "yes"]:
            return True
        else:
            print("Thank you for using the Diabetes Checker App.")
            return False


symptoms = {
    "a": "Frequent Urination",
    "b": "Sudden loss of weight",
    "c": "Increased thirst or hunger",
    "d": "Nausea and Vomiting",
    "e": "Blurry Vision",
    "f": "Urinary Tract Infection"
}

print("Thank you for using the Diabetes Checker.")
for key, value in symptoms.items():
    print(key, value)

diabetes = Diabetes()

while True:
    user_input = input("Select all symptoms that apply: (a b c d e f, or q to quit): "
                       "").lower().split()

    if "q" in user_input:
        print("Goodbye.")
        break

    elif not all(choice in symptoms for choice in user_input):
        print("Invalid selection. Try again.")
        continue
    urgent = {"a", "b", "c"}
    age = input("Enter your age: ").strip()
    if not age.isdigit():
        print("Invalid age.")
        continue
    age = int(age)
    if urgent.issubset(user_input) and age <= 21:
        print("Your symptoms match Type 1 Diabetes. Please consult a doctor immediately.")
        continue
    if len(user_input) >= 2 and age >= 22:
        print("Let's investigate further.")
        bmi = input("Enter your BMI: ").strip()
        if not bmi.replace('.', '', 1).isdigit():
            print("Invalid BMI.")
            continue
        bmi = float(bmi)
        glucose = input("Enter your glucose level: ").strip()
        if not glucose.replace('.', '', 1).isdigit():
            print("Invalid glucose.")
            continue
        glucose = float(glucose)
        result = diabetes.prediction(bmi, age, glucose)
        if not diabetes.try_again(input("Would you like to do another check? y/n: ")):
            break
    else:
        print("With only one symptom, you likely do not have diabetes.")
        if not diabetes.try_again(input("Would you like to do another check? y/n: ")):
            break
