import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load the dataset from CSV file
data_path = "feedback_data.csv"  # Ensure this file is in the same directory as train_model.py
df = pd.read_csv(data_path)

# Separate features (feedback) and labels (categories)
texts = df['feedback_text'].values
labels = df['category'].values

# Vectorize the text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train the Logistic Regression model
model = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model and vectorizer
joblib.dump(model, 'model/model.pkl')
joblib.dump(vectorizer, 'model/vectorizer.pkl')
print("Model and vectorizer saved successfully!")
