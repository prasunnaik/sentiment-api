import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from preprocessing import clean_text

# Step 1 - Load dataset
df = pd.read_csv('data/train.csv')

print("Dataset loaded:", df.shape)

# Step 2 - Clean text
df['clean_text'] = df['text'].apply(clean_text)

# Step 3 - Features and labels
X = df['clean_text']
y = df['label']

# Step 4 - Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5 - TF-IDF (IMPROVED)
vectorizer = TfidfVectorizer(
    max_features=5000,        # limits vocab (faster + better)
    ngram_range=(1, 2),       # unigrams + bigrams
    stop_words='english'      # remove useless words
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Step 6 - Model (IMPROVED)
model = LogisticRegression(max_iter=200)

model.fit(X_train_vec, y_train)

# Step 7 - Evaluation
predictions = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, predictions)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%\n")

print("📊 Classification Report:")
print(classification_report(y_test, predictions, target_names=["negative", "positive"]))

# Step 8 - Save models
joblib.dump(model, 'models/sentiment_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("\n✅ Model saved successfully!")
print("✅ Vectorizer saved successfully!")