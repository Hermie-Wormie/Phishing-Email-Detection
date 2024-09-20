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


"""
Test for non-phishing:

Subject: Team Meeting Reminder

Body: Hi Team,

This is a reminder for our weekly team meeting scheduled for Thursday at 3 PM. We will discuss project updates and any challenges you might be facing.

Please be prepared to share your progress.

Best regards,
James

"""

"""
Test for phishing:

Subject: Urgent: Update Your Account Information

Body: Dear Valued Customer,

We noticed unusual activity in your account. To ensure your security, we need you to verify your account information immediately. Click the link below to secure your account:

[Update Your Account Now](https://fakebank.com/secure)

Failure to verify your information within 24 hours will result in account suspension.

Thank you for your prompt attention to this matter.

Sincerely,
Customer Support Team
Fake Bank Inc.


"""