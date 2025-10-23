<h1 align="center">🚀 AI‑Powered Startup Funding & Investment Insights Dashboard</h1>

<p align="center">
  <a href="https://startup-dash.streamlit.app" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App">
  </a>
</p>

<p align="center">
  <i>An interactive AI‑driven dashboard built with <b>Streamlit</b> to analyze Indian startup funding trends, predict growth sectors, 
  and provide data‑driven investment recommendations for investors and analysts.</i>
</p>

<hr>

<h2>📘 Overview</h2>

<p>
This dashboard uses real startup funding data and a trained <b>Random Forest Machine Learning model</b> to uncover 
investment patterns, forecast high‑potential sectors, and support smarter funding decisions.
</p>

<p>
✨ <b>Live Demo:</b> <a href="https://startup-dash.streamlit.app" target="_blank">https://startup-dash.streamlit.app</a>
</p>

<hr>

<h2>🔍 Key Features</h2>

<ul>
  <li>📊 <b>Comprehensive Funding Analysis:</b> Explore funding amounts, top investors, and sectors over time.</li>
  <li>🧠 <b>AI Predictions:</b> Machine learning generates performance scores (0–1) for each startup.</li>
  <li>💡 <b>Investor Recommendation Engine:</b> Provides clear calls to action — <code>Buy</code>, <code>Hold</code>, <code>Explore</code>, or <code>Avoid</code>.</li>
  <li>🌱 <b>Sector Growth Insights:</b> Uses Year‑over‑Year investment analysis to measure market momentum.</li>
  <li>📈 <b>Dynamic Visuals:</b> Plotly & Seaborn charts for intuitive data interpretation.</li>
</ul>

<hr>

<h2>🧩 Tech Stack</h2>

<table>
<tr><td><b>Framework</b></td><td>Streamlit</td></tr>
<tr><td><b>Languages</b></td><td>Python 3.10+</td></tr>
<tr><td><b>Libraries</b></td><td>Pandas, NumPy, Seaborn, Plotly, Matplotlib, Scikit‑learn, Joblib</td></tr>
<tr><td><b>Model</b></td><td>RandomForestRegressor</td></tr>
<tr><td><b>Deployment</b></td><td>Streamlit Community Cloud</td></tr>
</table>

<hr>

<h2>📂 Project Structure</h2>

<pre>
startup-dashboard/
│
├── app.py                     # Main Streamlit application
├── model_training.py          # ML model training script
│
├── data/
│   └── startup_clean.csv       # Startup funding dataset
│
├── models/
│   ├── investment_model.pkl
│   ├── sector_encoder.pkl
│   └── city_encoder.pkl
│
├── requirements.txt           # Dependencies list
└── README.md                  # Documentation
</pre>

<hr>

<h2>⚙️ How to Run Locally</h2>

<pre>
# Clone this repository
git clone https://github.com/dubeyvimlendu/startup-dashboard.git
cd startup-dashboard

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
</pre>

<p>🌐 Access locally at <a href="http://localhost:8501" target="_blank">http://localhost:8501</a></p>

<hr>

<h2>🧮 Machine Learning Model Details</h2>

<ul>
  <li><b>Total Investment:</b> Total capital raised per startup.</li>
  <li><b>Funding Velocity:</b> Speed of fundraising across active years.</li>
  <li><b>Investor Density:</b> Number of unique investors per round.</li>
  <li><b>Funding Stability:</b> Variability control for each funding round.</li>
</ul>

<p>The model outputs a <b>Predicted Score (0–1)</b> — a data‑driven indicator of startup momentum and investor confidence.</p>

<hr>

<h2>💼 Investor Recommendation Logic</h2>

<table>
<tr><th>Category</th><th>Condition</th><th>Meaning</th></tr>
<tr><td>BUY</td><td>Predicted > 0.7 & growth_rate > 10%</td><td>Invest confidently — strong growth & low risk.</td></tr>
<tr><td>HOLD</td><td>Predicted > 0.6 but stable growth</td><td>Maintain portfolio position.</td></tr>
<tr><td>EXPLORE</td><td>Predicted ≥ 0.4 & growth rising</td><td>Emerging opportunity worth tracking.</td></tr>
<tr><td>AVOID</td><td>Predicted < 0.4</td><td>Risky — weak investor activity.</td></tr>
</table>

<hr>

<h2>📊 Sample Insights</h2>

<ul>
  <li>🏦 FinTech, EdTech, and E‑Commerce lead in total investment volume.</li>
  <li>🌱 Agritech & Logistics show strong YOY growth momentum.</li>
  <li>💡 Emerging cities (beyond Bengaluru/Mumbai) attract increasing investor interest.</li>
</ul>

<hr>

<h2>🚀 Deployment Details</h2>

<table>
<tr><td><b>GitHub Repo</b></td><td><a href="https://github.com/dubeyvimlendu/startup-dashboard" target="_blank">dubeyvimlendu/startup-dashboard</a></td></tr>
<tr><td><b>Branch</b></td><td>main</td></tr>
<tr><td><b>App File</b></td><td>app.py</td></tr>
<tr><td><b>Live App</b></td><td><a href="https://startup-dash.streamlit.app" target="_blank">https://startup-dash.streamlit.app</a></td></tr>
</table>

<hr>

<h2>🌟 Future Enhancements</h2>

<ul>
  <li>Integration with Crunchbase or AngelList APIs for live deal data.</li>
  <li>Predictive funding forecasts (ARIMA / Prophet).</li>
  <li>Investor behavior analysis modules.</li>
  <li>Dark theme and sector‑wise themes for visualization.</li>
</ul>

<hr>

<h2>👨‍💻 Author</h2>

<p>
Developed with ❤️ by <b>Vimlendu Dubey</b><br>
📧 <a href="mailto:dubeyvimlendu@gmail.com">dubeyvimlendu@gmail.com</a><br>
💼 <a href="https://github.com/dubeyvimlendu" target="_blank">GitHub Profile</a><br>
🌐 <a href="https://startup-dash.streamlit.app" target="_blank">Live Streamlit Dashboard</a>
</p>

<hr>

<h3 align="center">⭐ If you found this useful, please star the repository!</h3>
