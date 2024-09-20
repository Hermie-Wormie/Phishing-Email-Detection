import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model and vectorizer
with open('logistic_regression_model.pkl', 'rb') as model_file:
    log_reg_model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

def check_email(subject, body):
    # Combine subject and body for classification
    full_email_text = f"Subject: {subject} Body: {body}"
    
    # Debugging: Print the full email text being classified
    print(f"Classifying email: {full_email_text}")
    
    # Transform the user input using the loaded vectorizer
    email_tfidf = tfidf_vectorizer.transform([full_email_text])
    
    # Predict whether the email is phishing (1) or non-phishing (0)
    prediction = log_reg_model.predict(email_tfidf)
    
    # Debugging: Print the raw prediction output
    print(f"Raw prediction output: {prediction}")
    
    # Interpret the result
    if prediction == 1:
        print("This email is classified as a phishing email.")
    else:
        print("This email is classified as a non-phishing email.")

if __name__ == "__main__":
    # Get user input for both subject and body
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    
    # Call the function to check the email
    check_email(subject, body)
