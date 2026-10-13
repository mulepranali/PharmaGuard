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
   Place the required dataset and model pickle files in the project root:
   - `pharmaguard_functions.pkl`
   - `pharmaguard_df.pkl`
   *(Note: Large binary pickle files are excluded from git history due to GitHub file size limits).*

5. **Run the Application:**
   ```bash
   python main.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.
