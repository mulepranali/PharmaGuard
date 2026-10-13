import streamlit as st
import dill as pickle   # dill is more robust than pickle
import torch
from transformers import AutoTokenizer, AutoModel
import numpy, sys

# Compatibility shim for old pickle files referencing numpy._core
sys.modules['numpy._core'] = numpy.core
from transformers import AutoTokenizer, AutoModel

print("Transformers working fine!")

# Re-define BioBERTPipeline (must match the one used in training)
class BioBERTPipeline:
    def __init__(self, tokenizer, model, classifier):
        self.tokenizer = tokenizer
        self.model = model
        self.classifier = classifier

    def predict(self, text):
        inputs = self.tokenizer([text], return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].numpy()
        return self.classifier.predict(embedding)

# Load the saved BioBERT pipeline
with open(r"C:\Users\prana\OneDrive\Desktop\Drug\biobert_ddi_model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Drug Interaction Risk Analysis", page_icon="💊", layout="centered")

st.title("💊 Drug-Drug Interaction Risk Analyzer")
st.markdown("This app uses **BioBERT + Logistic Regression** to analyze if two drugs may interact with potential risks.")

# Input from user
drug_input = st.text_area(
    "Enter Drug Combination / Description:",
    placeholder="Example: Paracetamol with Ibuprofen may increase stomach pain"
)

if st.button("Analyze Risk"):
    if drug_input.strip() == "":
        st.warning("⚠️ Please enter a drug combination text.")
    else:
        # Make prediction
        prediction = model.predict(drug_input)
        if prediction[0] == 1:
            st.error("🚨 Potential Risk Detected! This combination may cause side effects.")
        else:
            st.success("✅ Safe Combination! No major risk detected.")

st.markdown("---")
st.caption("Powered by BioBERT + Streamlit")
