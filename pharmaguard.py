from pharmaguard import Flask, request, render_template_string, send_from_directory
import pickle
import os
from pharma_utils import get_drug_details, summarize_interaction, interaction_summary

# Register functions required for unpickling
globals()['get_drug_details'] = get_drug_details
globals()['summarize_interaction'] = summarize_interaction
globals()['interaction_summary'] = interaction_summary

# Load the pickle data
with open('pharmaguard_functions.pkl', 'rb') as f:
    data = pickle.load(f)

df = data['df']
drug_names = sorted(df['NAME'].dropna().unique().tolist())

app = Flask(__name__)

@app.route('/')
def index():
    # Load the index.html as string
    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()

    # Create all <option> entries for datalist
    options = "\n".join(f"<option value='{name}'>" for name in drug_names)

    # Inject dropdown list into placeholder
    html = html.replace("{{ drug_options }}", options)

    return render_template_string(html)

@app.route('/style.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'style.css')

@app.route('/result', methods=['POST'])
def result():
    drug_a = request.form.get('drug_a')
    drug_b = request.form.get('drug_b')
    gender = request.form.get('gender')
    age = request.form.get('age')
    diabetes = request.form.get('diabetes')

    user_info = {
        'gender': gender,
        'age': age,
        'diabetes': diabetes
    }

    summary = summarize_interaction(drug_a, drug_b, user_info, df)

    return f"""
    <html>
    <head>
        <link rel="stylesheet" href="/style.css">
        <title>PharmaGuard Result</title>
    </head>
    <body>
        <div class="result-box">
            <pre style="white-space: pre-wrap;">{summary}</pre>
            <br>
            <a href="/">🔙 Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
