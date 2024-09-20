# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Step 1: Load the cleaned dataset
# Assuming your dataset has two columns: 'email_text' (the email content) and 'label' (0 for non-phishing, 1 for phishing)
df = pd.read_csv('CLEANDATA/body.csv')

# Step 2: Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(df['body'], df['label'], test_size=0.2, random_state=42)

# Step 3: Apply TF-IDF Vectorization to the email text
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust max_features based on your data
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Step 4: Initialize and train a Logistic Regression model
log_reg_model = LogisticRegression(solver='lbfgs', max_iter=1000)
log_reg_model.fit(X_train_tfidf, y_train)

# Step 5: Make predictions on the test set
y_pred = log_reg_model.predict(X_test_tfidf)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Optionally, print out a more detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
