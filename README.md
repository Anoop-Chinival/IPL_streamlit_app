# 🏏 IPL Analytics Dashboard

A professional, interactive Streamlit dashboard providing deep insights and data exploration for the Indian Premier League (IPL) from 2008 to 2025.

## 🌟 Features
- **📊 Data Explorer:** View and filter raw datasets for IPL Matches and Ball-by-Ball Deliveries with mini-distribution charts for quick feature analysis.
- **💡 Deep Insights (18+ Visualizations):** Categorized insights into:
  - **🏏 Batsmen:** Top Run-Scorers, Most 6s, 4s, and Boundaries.
  - **🎯 Bowlers:** Top Wicket-Takers, Maidens Bowled, and Dismissal Types.
  - **🏟️ Team:** IPL Trophies Won, Most Wins, Total Runs/Wickets by Franchises, and Scoring Rates.
  - **⭐ General:** Player of the Match awards and Top Venues.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd IPL_streamlit_app
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Data:**
   Due to GitHub file size limits, the `archive/` folder containing the datasets is not uploaded. 
   - Create a folder named `archive` in the root directory.
   - Place your dataset files (`matches_updated_ipl_upto_2025.csv` and `deliveries_updated_ipl_upto_2025.csv`) inside the `archive/` folder.

4. **Run the Streamlit App:**
   ```bash
   python3 -m streamlit run app.py
   ```
   The application will open in your default browser at `http://localhost:8501`.

## 🛠️ Tech Stack
- **Python:** Data Processing logic
- **Pandas:** Data Manipulation and Aggregation
- **Plotly:** Interactive Visualizations
- **Streamlit:** Web Framework & UI

## 🎨 Design
The dashboard features a premium dark theme (`#0F172A`) with Gold and Light Blue accents for a highly professional aesthetic. Player initials have been mapped to their full names for better readability.

---
*Developed for IPL Analytics (2026).*
