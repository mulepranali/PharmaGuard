# pharma_utils.py

def get_drug_details(df, drug_name):
    drug_row = df[df['NAME'].str.lower() == drug_name.lower()]
    if drug_row.empty:
        return None

    row = drug_row.iloc[0]
    return {
        'name': row['NAME'],
        'uses': row['USES'],
        'side_effects': row['SIDE_EFFECT'],
        'class': row.get('THERAPEUTIC_CLASS', 'Unknown'),
        'pregnancy_advice': row.get('SAFETY_ADVICE_TO_PREGNANCY', 'Not Available'),
    }

def summarize_interaction(drug_a, drug_b, user_info, df):
    info_a = get_drug_details(df, drug_a)
    info_b = get_drug_details(df, drug_b)

    if not info_a or not info_b:
        return "One or both drugs not found in the dataset."

    # Extract side effects
    effects_a = info_a['side_effects'].split('\n') if info_a['side_effects'] else []
    effects_b = info_b['side_effects'].split('\n') if info_b['side_effects'] else []

    combined = list(set(effects_a + effects_b))
    serious = [e for e in combined if any(w in e.lower() for w in ['severe', 'anaphylactic', 'serious', 'pressure'])]
    moderate = [e for e in combined if any(w in e.lower() for w in ['require', 'bother', 'consult'])]
    mild = [e for e in combined if e not in serious + moderate]

    summary = f"""
👩 User Profile:
- Gender: {user_info['gender']}
- Age: {user_info['age']}
- Diabetes: {user_info['diabetes']}

💊 Drug A: {info_a['name']}
  - Uses:    {info_a['uses']}
  - Class: {info_a['class']}
  - Side Effects: {info_a['side_effects']}
  - Pregnancy Advice: {info_a['pregnancy_advice']}, label: CONSULT YOUR DOCTOR

💊 Drug B: {info_b['name']}
  - Uses:    {info_b['uses']}
  - Class: {info_b['class']}
  - Side Effects: {info_b['side_effects']}
  - Pregnancy Advice: {info_b['pregnancy_advice']}, label: CONSULT YOUR DOCTOR

✅ Combined Summary:
🔴 Serious Side Effects:
- {chr(10).join(serious) if serious else 'None'}

🟡 Moderate Side Effects:
- {chr(10).join(moderate) if moderate else 'None'}

🟢 Mild Side Effects:
- {chr(10).join(mild) if mild else 'None'}

📊 Side Effect Risk Levels:
- Serious: {len(serious)}
- Moderate: {len(moderate)}
- Mild: {len(mild)}

📝 Interaction Summary:
{drug_a} and {drug_b} may interact. Patients may experience a range of side effects from mild to severe. Monitoring is advised especially for elderly or diabetic patients.
"""
    return summary


def interaction_summary(drug_a_info, drug_b_info, user_info):
    summary = []

    summary.append(f"👩 User Profile:")
    summary.append(f"- Gender: {user_info['gender']}")
    summary.append(f"- Age: {user_info['age']}")
    summary.append(f"- Diabetes: {user_info['diabetes']}\n")

    summary.append(f"💊 Drug A: {drug_a_info['name']}")
    summary.append(f"  - Uses: {drug_a_info['uses']}")
    summary.append(f"  - Class: {drug_a_info['class']}")
    summary.append(f"  - Side Effects: {drug_a_info['side_effects']}")
    summary.append(f"  - Pregnancy Advice: {drug_a_info['pregnancy_advice']}, label: CONSULT YOUR DOCTOR\n")

    summary.append(f"💊 Drug B: {drug_b_info['name']}")
    summary.append(f"  - Uses: {drug_b_info['uses']}")
    summary.append(f"  - Class: {drug_b_info['class']}")
    summary.append(f"  - Side Effects: {drug_b_info['side_effects']}")
    summary.append(f"  - Pregnancy Advice: {drug_b_info['pregnancy_advice']}, label: CONSULT YOUR DOCTOR\n")

    # Combine side effects
    combined = list(set(drug_a_info['side_effects'].split('\n') + drug_b_info['side_effects'].split('\n')))
    serious = [e for e in combined if any(w in e.lower() for w in ['severe', 'anaphylactic', 'serious', 'pressure'])]
    moderate = [e for e in combined if any(w in e.lower() for w in ['require', 'bother', 'consult'])]
    mild = [e for e in combined if e not in serious + moderate]

    summary.append("✅ Combined Summary:")
    summary.append("🔴 Serious Side Effects:\n- " + "\n- ".join(serious) if serious else "- None")
    summary.append("🟡 Moderate Side Effects:\n- " + "\n- ".join(moderate) if moderate else "- None")
    summary.append("🟢 Mild Side Effects:\n- " + "\n- ".join(mild) if mild else "- None")

    summary.append("\n📊 Side Effect Risk Levels:")
    summary.append(f"- Serious: {len(serious)}")
    summary.append(f"- Moderate: {len(moderate)}")
    summary.append(f"- Mild: {len(mild)}")

    summary.append("\n📝 Interaction Summary:")
    summary.append(f"{drug_a_info['name']} and {drug_b_info['name']} may interact. Patients may experience a range of side effects. Monitoring is advised.")

    return "\n".join(summary)
