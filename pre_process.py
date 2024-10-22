import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import json

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy's English model and NLTK's stopwords
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(text):
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # 3. Remove stopwords
    text = " ".join([word for word in text.split() if word not in stop_words])

    # 4. Lemmatize using spaCy and NLTK
    text = custom_lemmatize(text)

    return text

# Custom lemmatization function using both spaCy and NLTK
def custom_lemmatize(text):
    doc = nlp(text)
    lemmatized_words = []

    for token in doc:
        # Keep named entities as they are, lemmatize others
        if token.ent_type_:
            lemmatized_words.append(token.text)
        else:
            lemmatized_words.append(lemmatizer.lemmatize(token.text.lower()))

    return " ".join(lemmatized_words)

# Load original FAQs from a JSON file
with open("faqs.json", 'r') as file:
    faqs_data = json.load(file)

# Dictionary to hold cleaned questions and answers
cleaned_data = {}

# Preprocess questions and answers, store them in cleaned_data
for category, faqs in faqs_data.items():
    cleaned_data[category] = []

    for faq in faqs:
        cleaned_faq = {
            'question': preprocess_text(faq['question']),
            'answer': preprocess_text(faq['answer'])
        }
        cleaned_data[category].append(cleaned_faq)

# Save the cleaned questions and answers to a new JSON file
with open("cleaned_faqs.json", 'w') as outfile:
    json.dump(cleaned_data, outfile, indent=4)

print("Cleaned FAQs have been saved to 'cleaned_faqs.json'")