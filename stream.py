# TRY CODE
import streamlit as st
import pickle
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os
import base64
import io
import plotly.graph_objects as go
import json
# ------------------ Load data ------------------
with open(r"C:\Users\prana\OneDrive\Desktop\Drug\pharmaguard_df.pkl", "rb") as f:
    df = pickle.load(f)

# ------------------ Functions ------------------
def get_drug_details(drug_name, df):
    row = df[df['NAME'] == drug_name].iloc[0]
    return {
        "name": row['NAME'],
        "uses": row.get('USES', 'Not available'),
        "class": row.get('CHEMICAL_CLASS', 'Not available'),
        "action": row.get('ACTION_CLASS', 'Not available'),
        "side_effect": row.get('SIDE_EFFECT', 'Not available'),
        "pregnancy": row.get('SAFETY_ADVICE_TO_PREGNANCY', 'Not available'),
        "breast_feeding": row.get('SAFETY_ADVICE_TO_BREAST_FEEDING', 'Not available'),
        "driving": row.get('SAFETY_ADVICE_TO_DRIVING', 'Not available'),
        "liver": row.get('SAFETY_ADVICE_TO_LIVER', 'Not available'),
        "kidney": row.get('SAFETY_ADVICE_TO_KIDNEY', 'Not available')
    }

def classify_side_effects(text):
    words = list(set(text.split()))
    serious_keywords = {'convulsion', 'abdominal', 'thromboembolism', 'procedural', 'rash', 'injection', 'hypertension', 'pressure'}
    mild_keywords = {'agitation', 'breathlessness', 'cough', 'insomnia', 'headache'}
    moderate_keywords = {'pain', 'dizziness', 'nausea', 'vomiting'}

    serious = [w for w in words if any(k in w.lower() for k in serious_keywords)]
    mild = [w for w in words if any(k in w.lower() for k in mild_keywords)]
    moderate = [w for w in words if w not in serious + mild]
    return serious, moderate, mild


import matplotlib.pyplot as plt
import streamlit as st

def plot_severity_chart(serious, moderate, mild):
    total = len(serious) + len(moderate) + len(mild)
    if total == 0:
        st.info("No side effects to display.")
        return

    # Calculate percentages
    pct = [len(serious)/total*100, len(moderate)/total*100, len(mild)/total*100]
    labels = ['Serious', 'Moderate', 'Mild']
    colors = ['#FF6B6B', '#FFD93D', '#6BCB77']

    # 👇 Define manual, tightly packed x positions
    x = [0, 0.3, 0.6]  # Less spacing than default (which is usually 1.0 apart)

    fig, ax = plt.subplots(figsize=(6, 2.5))  # Size still small

    bars = ax.bar(x, pct, color=colors, width=0.1)

    # Set custom ticks and labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=4)

    ax.set_ylim(0, max(pct) + 2)
    ax.set_ylabel('% of Side Effects', fontsize=4)
    ax.set_title('Side Effect Severity', fontsize=5)
    ax.tick_params(axis='y', labelsize=6)

    # Add percentage labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}%",
            ha='center',
            fontsize=4
        )

    plt.tight_layout()
    st.pyplot(fig)





def generate_report_pdf(summary, name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=6)
    for line in summary.split('\n'):
        pdf.multi_cell(0, 5, line)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# ------------------ Streamlit App ------------------
# ------------------ Streamlit Layout ------------------
st.set_page_config("Pharmaguard", layout="centered")
st.markdown("<h1 style='text-align: center;'>💊 Pharmaguard: Drug Interaction Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Check interactions between two drugs and download a side-effect report.</p>", unsafe_allow_html=True)
st.divider()

# User Info Inputs
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 Patient Name", value="John Doe")
    age = st.number_input("🎂 Age", min_value=1, max_value=120, value=30)
with col2:
    gender = st.selectbox("⚧ Gender", ["Male", "Female"])
    diabetes = st.selectbox("🩸 Diabetes", ["No", "Yes"])
user_info = {"gender": gender, "age": age, "diabetes": diabetes}

# Drug Selection Inputs
st.markdown("### 💊 Select Drugs to Compare")
drug_names = sorted(df['NAME'].dropna().unique().tolist())
col3, col4 = st.columns(2)
with col3:
    drug_a_name = st.selectbox("Drug A", drug_names)
with col4:
    drug_b_name = st.selectbox("Drug B", drug_names, index=1)

# Interaction Button
if st.button("🔍 Check Interaction", use_container_width=True):
    if drug_a_name == drug_b_name:
        st.warning("⚠️ Please select two different drugs.")
    else:
        try:
            drug_a = get_drug_details(drug_a_name, df)
            drug_b = get_drug_details(drug_b_name, df)
            combined = drug_a['side_effect'] + " " + drug_b['side_effect']
            serious, moderate, mild = classify_side_effects(combined)

            st.markdown(f"### ⚠️ Interaction Report for {drug_a_name} + {drug_b_name}")

            # Side Effects Categorization
            if serious:
                st.markdown("#### 🔴 Serious Side Effects")
                for s in serious[:10]:
                    st.markdown(f"- {s}")
            if moderate:
                st.markdown("#### 🟡 Moderate Side Effects")
                for m in moderate[:10]:
                    st.markdown(f"- {m}")
            if mild:
                st.markdown("#### 🟢 Mild Side Effects")
                for l in mild[:10]:
                    st.markdown(f"- {l}")

            # Personalized Warnings
            st.markdown("#### 🧑‍⚕ Personalized Advice")
            if age >= 65:
                st.info("👵 Elderly patients (65+) are more vulnerable to side effects. Monitoring or dose adjustments may be needed.")
            if gender == "Female":
                st.info("⚠️ Note: Some drugs may behave differently in females due to hormonal factors.")
            if diabetes == "Yes":
                st.info("🩺 Diabetic patients may need to monitor glucose levels when combining these medications.")

            # Summary Block
            st.markdown("#### 📋 Summary")
            st.info(f"{drug_a_name} and {drug_b_name} may interact. Patients may experience side effects ranging from mild to serious. Please consult a healthcare provider.")

            # Bar Chart
            plot_severity_chart(serious, moderate, mild)

            # Summary Text
            summary = f"""
👩 User Profile:
- Name: {name}
- Gender: {gender}
- Age: {age}
- Diabetes: {diabetes}

💊 Drug A: {drug_a['name']}
  - Uses: {drug_a['uses']}
  - Class: {drug_a['class']}
  - Side Effects: {drug_a['side_effect']}
  - Pregnancy Advice: {drug_a['pregnancy']}

💊 Drug B: {drug_b['name']}
  - Uses: {drug_b['uses']}
  - Class: {drug_b['class']}
  - Side Effects: {drug_b['side_effect']}
  - Pregnancy Advice: {drug_b['pregnancy']}

✅ Combined Summary:
🔴 Serious Side Effects: {', '.join(serious[:10])}
🟡 Moderate Side Effects: {', '.join(moderate[:10])}
🟢 Mild Side Effects: {', '.join(mild[:10])}

📊 Risk Levels:
- Serious: {len(serious)}
- Moderate: {len(moderate)}
- Mild: {len(mild)}

📝 Interaction Summary:
{drug_a['name']} and {drug_b['name']} may interact. Monitoring is advised, especially for elderly or diabetic patients.
"""

            st.markdown("#### 📄 Downloadable Report")
            if st.button("📝 Generate Report PDF"):
                pdf_path = generate_report_pdf(summary, name)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download PDF", data=f, file_name=f"{name}_interaction.pdf", mime="application/pdf")
                os.remove(pdf_path)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("💼 Created with ❤ by Pharmaguard")


