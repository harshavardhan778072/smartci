import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load build history
data = pd.read_csv("data/build_history.csv")

# Select input features and target
features = [
    "previous_failures",
    "changed_files",
    "code_churn",
    "test_count"
]

X = data[features]
y = data["failed"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train the machine learning model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the trained model
joblib.dump(model, "build_failure_model.pkl")
print("Model saved successfully!")

# Predict the result for a sample new build
new_build = pd.DataFrame([{
    "previous_failures": 2,
    "changed_files": 8,
    "code_churn": 150,
    "test_count": 40
}])

prediction = model.predict(new_build)[0]
probability = model.predict_proba(new_build)[0][1]

print("\nNew Build Prediction:")

if prediction == 1:
    print("Prediction: BUILD FAILURE")
else:
    print("Prediction: BUILD SUCCESS")

print(f"Estimated failure probability: {probability * 100:.2f}%")