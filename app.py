# ========================================
# 🚀 STARTUP FUNDING + AI INSIGHTS DASHBOARD
# ========================================

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import plotly.express as px

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(layout="wide", page_title='Startup Funding Dashboard', page_icon='💰')

# --- LOAD DATA ---
df = pd.read_csv('startup_clean.csv')
df['startup'] = df['startup'].str.strip().str.lower()
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df.rename(columns={'vertical': 'sector'}, inplace=True)

# --- LOAD ML MODEL AND ENCODERS ---
model = joblib.load("investment_model.pkl")
le_sector = joblib.load("sector_encoder.pkl")
le_city = joblib.load("city_encoder.pkl")

# --- PAGE TITLE ---
st.title("🚀 Startup Funding & AI Investment Dashboard")
st.markdown("""
A unified platform analyzing Indian startup funding trends and leveraging AI to predict top-performing startups and sectors for investors.
""")

# ==============================
# 1️⃣ BASIC DASHBOARD INSIGHTS
# ==============================

col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    selected_startup = st.selectbox('Select Startup (or All)', ['All'] + sorted(df['startup'].dropna().unique()))
with col_filter2:
    all_investors = sorted(set([i.strip() for investors in df['Investor'].dropna() for i in investors.split(',')]))
    selected_investor = st.selectbox('Select Investor (or All)', ['All'] + all_investors)

filtered_df = df.copy()
if selected_startup != 'All':
    filtered_df = filtered_df[filtered_df['startup'] == selected_startup]
if selected_investor != 'All':
    filtered_df = filtered_df[filtered_df['Investor'].str.contains(selected_investor, case=False, na=False)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    total_investments = filtered_df['amount'].sum()
    total_startups = filtered_df['startup'].nunique()
    total_investors = len(set([i.strip() for investors in filtered_df['Investor'].dropna() for i in investors.split(',')]))
    total_sectors = filtered_df['sector'].nunique()

    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Investment", f"{total_investments:,.0f} Cr")
    col2.metric("🏢 Startups Funded", total_startups)
    col3.metric("👥 Unique Investors", total_investors)
    col4.metric("📈 Sectors Covered", total_sectors)

    st.subheader("📈 Last 10 Investments")
    last_10 = filtered_df[['date', 'startup', 'sector', 'city', 'Type', 'amount']].sort_values('date', ascending=False).head(10)
    last_10['amount'] = last_10['amount'].astype(str) + ' Cr'
    st.dataframe(last_10.reset_index(drop=True))

    st.subheader("📉 Visual Insights")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Top 5 Biggest Investments**")
        top_investments = filtered_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top_investments.values, y=top_investments.index, palette="Blues_d", ax=ax)
        ax.set_xlabel("Investment (Cr)")
        ax.set_ylabel("Startup")
        st.pyplot(fig)

    with col_b:
        st.markdown("**Top Sectors (by Investment)**")
        sector_series = filtered_df.groupby('sector')['amount'].sum().sort_values(ascending=False)
        top5 = sector_series[:5]
        others = sector_series[5:].sum()
        if others > 0:
            top5['Others'] = others
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        top5.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax2, colors=sns.color_palette('Set2'))
        ax2.set_ylabel('')
        st.pyplot(fig2)

    st.subheader("📅 Year-over-Year Investment Trend")
    yoy_series = filtered_df.groupby('year')['amount'].sum()
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=yoy_series.index, y=yoy_series.values, marker='o', ax=ax3)
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Investment (Cr)")
    ax3.set_title("YOY Investment Growth")
    ax3.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig3)

# ==============================
# 2️⃣ AI MODEL INSIGHTS
# ==============================

st.header("💡 AI-Powered Startup Predictions")

sector_choice = st.selectbox("Select a Sector (optional)", ['All'] + sorted(df['sector'].dropna().unique()))
city_choice = st.selectbox("Select a City (optional)", ['All'] + sorted(df['city'].dropna().unique()))

agg = df.groupby('startup').agg({
    'amount': ['sum', 'mean', 'count'],
    'year': ['min', 'max', 'nunique'],
    'Investor': 'nunique',
    'sector': 'first',
    'city': 'first'
}).reset_index()

agg.columns = ['startup', 'total_investment', 'avg_investment', 'rounds',
               'first_year', 'last_year', 'active_years', 'unique_investors', 'sector', 'city']

agg['funding_velocity'] = agg['total_investment'] / (agg['active_years'] + 1)
agg['investor_density'] = agg['unique_investors'] / (agg['rounds'] + 1)
agg['funding_stability'] = agg['avg_investment'] / (agg['total_investment'] + 1)

# --- Ensure prediction column exists ---
if 'predicted_score' not in agg.columns:
    agg['sector_encoded'] = le_sector.transform(agg['sector'])
    agg['city_encoded'] = le_city.transform(agg['city'])
    X_new = agg[['total_investment', 'avg_investment', 'rounds', 'active_years',
                 'unique_investors', 'funding_velocity', 'investor_density',
                 'funding_stability', 'sector_encoded', 'city_encoded']]
    agg['predicted_score'] = model.predict(X_new)

subset = agg.copy()
if sector_choice != 'All':
    subset = subset[subset['sector'] == sector_choice]
if city_choice != 'All':
    subset = subset[subset['city'] == city_choice]

if subset.empty:
    st.warning("No startups found for these filters.")
else:
    st.subheader(f"🏆 Top Startups Based on AI Performance")
    top_results = subset.sort_values('predicted_score', ascending=False).head(10)
    st.dataframe(top_results[['startup', 'sector', 'city', 'predicted_score']])

# ==============================
# 3️⃣ INVESTOR VALUE ENHANCEMENT
# ==============================

st.header("💼 Investor Recommendation Insights")

def assign_rating(score):
    if score >= 0.75:
        return "High Potential"
    elif score >= 0.55:
        return "Promising"
    elif score >= 0.35:
        return "Watchlist"
    else:
        return "Risky"

agg['investment_rating'] = agg['predicted_score'].apply(assign_rating)

st.markdown("#### 🔍 Startup Ratings based on AI Predictions")
top_rated = agg.sort_values('predicted_score', ascending=False)[['startup', 'sector', 'city', 'predicted_score', 'investment_rating']].head(15)
st.dataframe(top_rated)

# --- Sector Attractiveness ---
sector_strength = agg.groupby('sector')['predicted_score'].mean().sort_values(ascending=False).reset_index()
fig1 = px.bar(sector_strength, x='predicted_score', y='sector', orientation='h',
              color='predicted_score', color_continuous_scale='tealrose',
              labels={'predicted_score': 'Predicted Performance', 'sector': 'Sector'},
              title='📊 Sector Attractiveness (AI Performance Average)')
fig1.update_layout(yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig1, use_container_width=True)

# --- Combine Growth for Opportunity Index ---
sector_trend = df.groupby(['sector', 'year'])['amount'].sum().reset_index()
sector_trend['growth_rate'] = sector_trend.groupby('sector')['amount'].pct_change().fillna(0)
sector_growth = sector_trend.groupby('sector')['growth_rate'].mean().reset_index()
combined = pd.merge(sector_strength, sector_growth, on='sector', how='left')

combined['opportunity_index'] = (
    0.6 * combined['predicted_score'] +
    0.4 * combined['growth_rate'].clip(lower=-0.2, upper=0.5)
)

# --- Recommendations ---
def investor_recommendation(row):
    if row['predicted_score'] > 0.7 and row['growth_rate'] > 0.1:
        return "Buy"
    elif row['predicted_score'] > 0.6 and row['growth_rate'] <= 0.1:
        return "Hold"
    elif row['predicted_score'] >= 0.4 and row['growth_rate'] > 0.15:
        return "Explore"
    else:
        return "Avoid"

combined['recommendation'] = combined.apply(investor_recommendation, axis=1)

st.subheader("🧭 Sector Recommendations (Buy / Hold / Explore / Avoid)")
st.dataframe(combined[['sector', 'predicted_score', 'growth_rate', 'opportunity_index', 'recommendation']].sort_values('opportunity_index', ascending=False).head(15))

fig2 = px.bar(combined.sort_values('opportunity_index', ascending=False).head(10),
              x='opportunity_index', y='sector', color='recommendation', orientation='h',
              title='💡 Recommended Sectors for Investment',
              labels={'opportunity_index': 'Composite Opportunity Index', 'sector': 'Sector'})
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
---
### 🎯 Investor Takeaways
- **AI Ratings:** Identify high-performing startups (High Potential, Promising, Risky).
- **Sector Heatmap:** Shows investor-attractive industries.
- **Opportunity Index:** Combines AI score & market growth rate.
- **Actionable Guidance:** BUY → GO; HOLD → Monitor; EXPLORE → Emerging; AVOID → High-risk.
---
""")
