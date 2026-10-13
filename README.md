# PharmaGuard - AI Drug Interaction Assistant

PharmaGuard is a web application designed to analyze drug-drug interactions and predict potential risks based on patient profiles (such as age, gender, and diabetes condition).

## Features
- **Drug Interaction Analysis**: Compares pairs of drugs and assesses interaction severity and symptoms.
- **Patient Profiling**: Incorporates patient attributes like age, gender, and diabetes status into risk summaries.
- **Interactive Web Interface**: Built with Flask, featuring a clean UI with frosted glass design elements.

## Tech Stack
- **Backend**: Python 3.9+, Flask
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mulepranali/PharmaGuard.git
   cd PharmaGuard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Data & Model Files:**
   Due to GitHub's file size limits, the large dataset and model files are hosted on Google Drive:
   - 🔗 **[Download Model & Data Files (Google Drive)](https://drive.google.com/drive/folders/14UFHRAOnEUPB79WdDU8JvJuUFkYLwUha)**

   Download `pharmaguard_functions.pkl` from the link above and place it in the project root directory before running the application.

5. **Run the Application:**
   ```bash
   python main.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.
