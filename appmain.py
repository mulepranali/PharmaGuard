# TRY CODE
import streamlit as st
import pickle
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

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
st.set_page_config(page_title="PharmaGuard 💊", layout="wide")
st.title("🧪 PharmaGuard: AI-Driven Drug Interaction & Side Effect Checker")

# Layout: Two columns
left, right = st.columns(2)

with left:
    name = st.text_input("👤 Patient Name", value="John Doe")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    diabetes = st.selectbox("Diabetes", ["No", "Yes"])
    user_info = {"gender": gender, "age": age, "diabetes": diabetes}

with right:
    st.markdown("### 💊 Select Drugs")
    drug_names = sorted(df['NAME'].dropna().unique().tolist())
    drug_a_name = st.selectbox("Drug A", drug_names)
    drug_b_name = st.selectbox("Drug B", drug_names, index=1)

# Check Interaction
if st.button("🔍 Check Interaction"):
    if drug_a_name == drug_b_name:
        st.warning("⚠️ Please select two different drugs.")
    else:
        try:
            drug_a = get_drug_details(drug_a_name, df)
            drug_b = get_drug_details(drug_b_name, df)
            combined = drug_a['side_effect'] + " " + drug_b['side_effect']
            serious, moderate, mild = classify_side_effects(combined)

            # Final summary
            summary = f"""
👩 User Profile:
- Name: {name}
- Gender: {user_info['gender']}
- Age: {user_info['age']}
- Diabetes: {user_info['diabetes']}

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

📊 Side Effect Risk Levels:
- Serious: {len(serious)}
- Moderate: {len(moderate)}
- Mild: {len(mild)}

📝 Interaction Summary:
{drug_a['name']} and {drug_b['name']} may interact. Patients may experience a range of side effects. Monitoring is advised especially for elderly or diabetic patients.
"""
            st.markdown(summary.replace("\n", "  \n"))

            # Chart
            plot_severity_chart(serious, moderate, mild)

            # Downloadable Report
            if st.button("📝 Generate Report PDF"):
                pdf_path = generate_report_pdf(summary, name)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Report",
                        data=f,
                        file_name=f"{name.replace(' ', '_')}_drug_interaction.pdf",
                        mime="application/pdf"
                    )
                os.remove(pdf_path)

        except Exception as e:
            st.error(f"❌ Error: {e}")
