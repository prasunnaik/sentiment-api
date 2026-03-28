from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from preprocessing import clean_text

app = FastAPI()

# Allow Chrome extension to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the saved models
model = joblib.load('models/sentiment_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(input: TextInput):
    # Clean the text
    cleaned = clean_text(input.text)
    
    # Convert to numbers
    vectorized = vectorizer.transform([cleaned])
    
    # Predict
    result = model.predict(vectorized)[0]
    proba = model.predict_proba(vectorized)[0]
    confidence = round(max(proba) * 100, 1)
    
    return {
        "text": input.text,
        "sentiment": result,
        "confidence": confidence
    }

@app.get("/")
def root():
    return {"message": "✅ Sentiment API is running!"}
