import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

st.title("📊 AI Sentiment Intelligence Dashboard")

# -------------------------------
# SINGLE TEXT
# -------------------------------
st.subheader("✍️ Analyze Single Text")

text = st.text_area("Enter text")

if st.button("Analyze"):
    if text:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"text": text}
            )
            data = res.json()

            col1, col2 = st.columns(2)

            with col1:
                if data["sentiment"] == "positive":
                    st.success(f"😊 Positive ({data['confidence']}%)")
                else:
                    st.error(f"😞 Negative ({data['confidence']}%)")

            with col2:
                st.metric("Confidence Score", f"{data['confidence']}%")

            if "aspects" in data:
                st.info("🔍 Aspects: " + ", ".join(data["aspects"]))

        except:
            st.error("API not running")

# -------------------------------
# MULTIPLE REVIEWS
# -------------------------------
st.subheader("📥 Bulk Review Analysis")

reviews_input = st.text_area("Paste multiple reviews (one per line)")

if st.button("Analyze Bulk"):
    reviews = [r for r in reviews_input.split("\n") if r.strip()]

    sentiments = []
    aspect_list = []

    for review in reviews:
        res = requests.post(
            "http://127.0.0.1:8000/predict",
            json={"text": review}
        )
        data = res.json()

        sentiments.append(data["sentiment"])
        aspect_list.extend(data.get("aspects", []))

    # -------------------------------
    # METRICS
    # -------------------------------
    pos = sentiments.count("positive")
    neg = sentiments.count("negative")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Reviews", len(reviews))
    col2.metric("Positive", pos)
    col3.metric("Negative", neg)

    # -------------------------------
    # PIE CHART
    # -------------------------------
    st.subheader("📊 Sentiment Distribution")

    fig, ax = plt.subplots()
    ax.pie([pos, neg], labels=["Positive", "Negative"], autopct="%1.1f%%")
    st.pyplot(fig)

    # -------------------------------
    # ASPECT ANALYSIS
    # -------------------------------
    st.subheader("🔍 Aspect Insights")

    aspect_counts = Counter(aspect_list)

    if aspect_counts:
        st.bar_chart(aspect_counts)
    else:
        st.write("No aspects detected")

    # -------------------------------
    # RAW OUTPUT
    # -------------------------------
    st.subheader("📋 Detailed Results")

    for r, s in zip(reviews, sentiments):
        st.write(f"{s.upper()} → {r}")