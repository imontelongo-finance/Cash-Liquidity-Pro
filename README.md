💰 Cash-Liquidity-Pro
Strategic Finance Control Tower & Automated Liquidity Pipeline
Cash-Liquidity-Pro is a professional-grade financial engine designed to bridge the gap between raw operational data and executive-level strategy. It replaces manual, error-prone spreadsheets with a robust Python-based architecture for managing 13-week cash runways and unit economics.

🚀 Executive Value-Add
This project demonstrates a Finance 4.0 approach to corporate treasury and FP&A:

Automated ETL: Eliminates manual data entry by cleaning and processing raw ERP/Ops exports via a standardized Python pipeline.

Verified Accuracy: Includes an integrated pytest suite to ensure 100% mathematical integrity—preventing "broken cell" syndrome found in legacy spreadsheets.

Scenario Modeling: Interactive "Strategic Levers" allow executives to simulate the cash impact of vendor DPO (Days Payable Outstanding) negotiations and OpEx efficiency gains.

Audit Ready: Maintains a full execution history in /logs, providing a transparent audit trail for all financial transformations.

🏗️ Project Architecture
The repository follows a modular, production-ready structure:

app.py: The Executive Dashboard (Streamlit).

scripts/: Python engines for data generation and transformation.

data/: Tiered storage (Raw vs. Processed) to maintain data lineage.

tests/: Automated internal controls and logic verification.

logs/: System audit trails.

🛠️ Installation & Setup
To run this project locally, ensure you have Python 3.12+ installed.

Clone the repository:

Bash
git clone https://github.com/[YOUR-USERNAME]/Cash-Liquidity-Pro.git
cd Cash-Liquidity-Pro
Set up a Virtual Environment:

Bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
Install Dependencies:

Bash
pip install -r requirements.txt
Initialize the Data & Run Tests:

Bash
python scripts/generate_mock_data.py
python scripts/process_data.py
python -m pytest tests/test_liquidity_math.py
Launch the Dashboard:

Bash
streamlit run app.py
📈 Key Metrics Tracked
CM2 Margin: Contribution Margin 2 (Revenue - COGS - Logistics - Waste).

13-Week Runway: Projected cash-out dates based on current burn and AP aging.

Covenant Compliance: Real-time monitoring against minimum cash requirements.