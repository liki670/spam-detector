import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load base dataset (SMS spam dataset)
df = pd.read_csv("sms.tsv", sep="\t", header=None, names=["label", "text"])

# Convert labels: spam = 1, ham = 0
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Additional custom data for better accuracy (email-style spam)
extra_data = pd.DataFrame({
    "text": [

        # Job scams
        "Earn money daily from home apply now",
        "No experience required job apply immediately",
        "Work from home and earn high income",
        "Part time job with attractive salary",
        "Easy online job opportunity available",

        # Financial scams
        "Your bank account is blocked verify immediately",
        "You have received a refund claim now",
        "Update your bank details to continue service",
        "Suspicious activity detected login now",
        "Claim your cashback reward today",

        # Delivery scams
        "Your parcel delivery failed update your address",
        "Courier service pending payment click to release",
        "Shipment delayed due to unpaid charges",
        "Your package is on hold confirm your details",
        "Delivery failed due to incorrect address",

        # Threat and urgency
        "Your account will be suspended verify now",
        "Legal action will be taken if you do not respond",
        "Immediate action required to secure account",
        "Your email will be deactivated soon",
        "Failure to respond will result in penalty",

        # Romance scams
        "Hello I would like to connect with you",
        "I am interested in you please reply",
        "I have a proposal for you contact me",
        "Waiting for your response dear friend",

        "Sex available 2km away ",

        # Gaming and rewards
        "Get free game coins now click here",
        "Claim your free rewards instantly",
        "Unlock premium features for free",
        "Win gaming prizes now",
        "Free diamonds available click now",

        # General promotional spam
        "Congratulations you have won a gift",
        "Limited time offer buy now",
        "Exclusive deal just for you",
        "Offer expires soon act now",
        "Huge discount available today",

        # Phishing messages
        "Click the link to verify your account",
        "Login now to secure your account",
        "Confirm your identity immediately",
        "Update your information using this link",
        "Verify your account details now"
    ],
    "label": [1] * 40
})

# Combine datasets
df = pd.concat([df, extra_data], ignore_index=True)

# Convert text into numerical features using TF-IDF with n-grams
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
X = vectorizer.fit_transform(df["text"])

# Train Naive Bayes model
model = MultinomialNB()
model.fit(X, df["label"])

# Save trained model and vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully")