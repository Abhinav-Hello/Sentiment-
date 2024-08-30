# -*- coding: utf-8 -*-
"""majorprojectNLP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rfWmMuU650W-6tStMX7z774XzfvIV46Z
"""

import requests
from bs4 import BeautifulSoup
import csv

def scrape_imdb_reviews(url, num_pages):
    reviews = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for page in range(num_pages):
        response = requests.get(f"{url}?start={page*10}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for review in soup.find_all('div', class_='text show-more__control'):
            body = review.text.strip()
            reviews.append({'body': body})

    return reviews
# List of movie URLs and their titles
movies = [
    {'url': 'https://www.imdb.com/title/tt2560140/reviews?ref_=tt_urv', 'title': 'Attack on Titan'},
    {'url': 'https://www.imdb.com/title/tt0944947/reviews?ref_=tt_urv', 'title': 'Game of Thrones'},
    # Add more movies as needed
]

num_pages = 5  # Adjust the number of pages to scrape

with open('imdb_reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for movie in movies:
        reviews = scrape_imdb_reviews(movie['url'], num_pages)
        for review in reviews:
            review['title'] = movie['title']
            writer.writerow(review)

import pandas as pd

# Load the data
df = pd.read_csv('imdb_reviews_Series.csv')
print(df.head())

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Convert to lowercase
    tokens = [token.lower() for token in tokens]
    # Remove stopwords
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Join tokens back into a single string
    return ' '.join(tokens)

df['cleaned_body'] = df['body'].apply(preprocess_text)
print(df.head())

from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Determine the sentiment
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df['sentiment'] = df['cleaned_body'].apply(analyze_sentiment)
print(df.head())

# Display the results
print(df[['title','body', 'sentiment']])

# Save the results to a new CSV file
df.to_csv('imdb_reviews_with_sentiments_Series.csv', index=False)

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from textblob import TextBlob
# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
# Load the preprocessed data with sentiment analysis by TextBlob
df = pd.read_csv('imdb_reviews_with_sentiments_Series.csv')
# Remove neutral sentiments for binary classification
df = df[df['sentiment'] != 'Neutral']
# Map sentiment to binary labels
df['sentiment'] = df['sentiment'].map({'Positive': 1, 'Negative': 0})
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_body'], df['sentiment'], test_size=0.2, random_state=42)

# Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Define models to compare
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Support Vector Machine": SVC(kernel='linear')
}

# Train and evaluate each model
results = {}
for model_name, model in models.items():
    # Train the model
    model.fit(X_train_vec, y_train)
    # Predict the sentiment of the test set
    y_pred = model.predict(X_test_vec)
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    results[model_name] = {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": confusion
    }

# Print the results for each model
for model_name, metrics in results.items():
    print(f"Model: {model_name}")
    print(f"Accuracy: {metrics['accuracy']}")
    print("Classification Report:")
    print(metrics['classification_report'])
    print("Confusion Matrix:")
    print(metrics['confusion_matrix'])
    print("\n")

# Compare with TextBlob results
textblob_sentiments = X_test.apply(lambda x: 1 if TextBlob(x).sentiment.polarity > 0 else 0)
textblob_accuracy = accuracy_score(y_test, textblob_sentiments)

print("TextBlob Accuracy:", textblob_accuracy)

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load the preprocessed data with sentiment analysis by TextBlob
df = pd.read_csv('imdb_reviews_with_sentiments.csv')

# Remove neutral sentiments for binary classification
df = df[df['sentiment'] != 'Neutral']

# Map sentiment to binary labels
df['sentiment'] = df['sentiment'].map({'Positive': 1, 'Negative': 0})

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_body'], df['sentiment'], test_size=0.2, random_state=42)

# Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Define models to compare
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Support Vector Machine": SVC(kernel='linear')
}

# Train and evaluate each model
results = {}
for model_name, model in models.items():
    # Train the model
    model.fit(X_train_vec, y_train)
    # Predict the sentiment of the test set
    y_pred = model.predict(X_test_vec)
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    results[model_name] = {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": confusion
    }

# Print the results for each model
for model_name, metrics in results.items():
    print(f"Model: {model_name}")
    print(f"Accuracy: {metrics['accuracy']}")
    print("Classification Report:")
    print(metrics['classification_report'])
    print("Confusion Matrix:")
    print(metrics['confusion_matrix'])
    print("\n")

# Compare with TextBlob results
textblob_sentiments = X_test.apply(lambda x: 1 if TextBlob(x).sentiment.polarity > 0 else 0)
textblob_accuracy = accuracy_score(y_test, textblob_sentiments)

print("TextBlob Accuracy:", textblob_accuracy)