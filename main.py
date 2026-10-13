# from flask import Flask, request, render_template, send_from_directory
# import pickle
# import os
# from pharma_utils import get_drug_details, summarize_interaction, interaction_summary

# # Register functions for unpickling
# globals()['get_drug_details'] = get_drug_details
# globals()['summarize_interaction'] = summarize_interaction
# globals()['interaction_summary'] = interaction_summary

# # Load your pickle file
# with open('pharmaguard_functions.pkl', 'rb') as f:
#     data = pickle.load(f)

# df = data['df']
# drug_names = sorted(df['NAME'].dropna().unique().tolist())

# # Flask app setup
# app = Flask(__name__)

# # ---------- ROUTES ---------- #

# # Home page
# @app.route('/intro')
# def intro():
#     return render_template('intro.html')

# # Drug interaction page
# @app.route('/index')
# def index():
#     options = "\n".join(f"<option value='{name}'>" for name in drug_names)
#     return render_template("index.html", drug_options=options)

#     # options = "\n".join(f"<option value='{name}'>{name}</option>" for name in drug_names)
#     # return render_template('index.html', drug_options=options)
   

# # Visualization page (optional)
# @app.route('/visualize')
# def visualize():
#     return render_template('visualize.html')

# # CSS
# @app.route('/style.css')
# def serve_css():
#     return send_from_directory(os.getcwd(), 'style.css')

# # Result after form submission
# @app.route('/result', methods=['POST'])
# def result():
#     drug_a = request.form.get('drug_a')
#     drug_b = request.form.get('drug_b')
#     gender = request.form.get('gender')
#     age = request.form.get('age')
#     diabetes = request.form.get('diabetes')

#     user_info = {
#         'gender': gender,
#         'age': age,
#         'diabetes': diabetes
#     }

#     summary = summarize_interaction(drug_a, drug_b, user_info, df)

#     return f"""
#     <html>
#     <head>
#         <link rel="stylesheet" href="/style.css">
#         <title>PharmaGuard Result</title>
#     </head>
#     <body>
#         <div class="result-box">
#             <pre style="white-space: pre-wrap;">{summary}</pre>
#             <br>
#             <a href="/index">🔙 Back to Interaction</a>
#         </div>
#     </body>
#     </html>
#     """

# # Error handling
# @app.errorhandler(404)
# def page_not_found(e):
#     return "<h1>404 - Page Not Found</h1><a href='/intro'>Back to Home</a>", 404

# # Run app
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, send_from_directory
import pickle
import os
from pharma_utils import get_drug_details, summarize_interaction, interaction_summary

# Register functions for unpickling
globals()['get_drug_details'] = get_drug_details
globals()['summarize_interaction'] = summarize_interaction
globals()['interaction_summary'] = interaction_summary

# Load your pickle file

with open('pharmaguard_functions.pkl', 'rb') as f:
    data = pickle.load(f)

df = data['df']
drug_names = sorted(df['NAME'].dropna().unique().tolist())

# Flask app setup
app = Flask(__name__)

# ---------- ROUTES ---------- #

# Home page
@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

# Drug interaction page
@app.route('/index')
def index():
    options = "\n".join(f"<option value='{name}'>" for name in drug_names)
    return render_template("index.html", drug_options=options)

# Visualization page
@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

# CSS
@app.route('/style.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'style.css')

# Result after form submission
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
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: 'Segoe UI', sans-serif;
            background: url('https://t4.ftcdn.net/jpg/10/27/40/71/360_F_1027407115_f9OsOMcgehl82FKwpNCgCBROJqmDyX3M.jpg') no-repeat center center fixed;
            background-size: cover;
            overflow-x: hidden;
        }}

        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            z-index: 0;
        }}

        .result-box {{
            max-width: 90%;
            width: 1000px;
            margin: 100px auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.2);  /* Transparent white */
            border-radius: 15px;
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px); /* Frosted glass effect */
            color: white;
            position: relative;
            z-index: 1;
        }}

        a {{
            text-decoration: none;
            color: #00ffff;
            font-weight: bold;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        pre {{
            white-space: pre-wrap;
            font-size: 1.1rem;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="result-box">
        <pre>{summary}</pre>
        <br>
        <a href="/index">🔙 Back to Interaction</a>
    </div>
</body>
</html>
"""



# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1><a href='/'>Back to Home</a>", 404

# Run app
if __name__ == '__main__':
    app.run(debug=True)