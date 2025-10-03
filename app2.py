import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(layout="wide", page_title='Startup Dashboard')

# Load dataset
df = pd.read_csv('startup_clean.csv')

# Preprocess date and year
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year.astype('Int64')  # keeps integers with NA support

# Sidebar selection
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis Type', ['Overall Analysis', 'Startup', 'Investor'])


# Function to load investor details
def load_investor_details(investor):
    st.title(f"Investor: {investor}")

    # Filter rows for selected investor
    filtered_df = df[df['Investor'].str.contains(investor, case=False, na=False)]
    if filtered_df.empty:
        st.warning("No data available for this investor")
        return

    # --- Metrics cards ---
    total_investments = filtered_df['amount'].sum()
    total_startups = filtered_df['startup'].nunique()
    total_verticals = filtered_df['vertical'].nunique()

    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
    col_metrics1.metric("Total Investment", f"${total_investments:,.0f}")
    col_metrics2.metric("Startups Funded", total_startups)
    col_metrics3.metric("Sectors Invested In", total_verticals)

    # --- Last 5 investments ---
    st.subheader('Last 5 Investments')
    last_5 = filtered_df[['date', 'startup', 'vertical', 'city', 'Type', 'amount']] \
        .sort_values('date', ascending=False).head(5)
    st.dataframe(last_5)

    # --- Plots: Biggest Investments & Sectors ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Top 5 Biggest Investments')
        big_series = filtered_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(big_series.index, big_series.values, color='#4e79a7')
        ax.set_ylabel('Amount ($)')
        ax.set_xlabel('Startup')
        ax.set_title('Biggest Investments')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors Invested In')
        grouped = filtered_df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
        top = grouped[:5]
        others = grouped[5:].sum()
        if others > 0:
            top['Others'] = others
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        colors = plt.get_cmap('tab20').colors
        top.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax1, colors=colors)
        ax1.set_ylabel('')
        ax1.set_title('Top 5 Sectors + Others')
        st.pyplot(fig1)

    # --- YOY Investments ---
    st.subheader('Year-over-Year Investments')
    year_series = filtered_df.groupby('year')['amount'].sum()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(year_series.index, year_series.values, marker='o', linestyle='-', color='#e15759')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Amount ($)')
    ax2.set_title('YOY Investments')
    ax2.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig2)


# --- Main page logic ---
if option == 'Overall Analysis':
    st.title('Overall Startup Funding Analysis')
    st.write("Summary of all investments, startups, and sectors (can expand later).")

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique()))
    st.title(f"Startup Analysis: {selected_startup}")
    # You can add startup-specific plots here

else:  # Investor
    # Split multi-investor strings into unique list
    all_investors = sorted(set([i.strip() for investors in df['Investor'].dropna()
                                for i in investors.split(',')]))
    selected_investor = st.sidebar.selectbox('Select Investor', all_investors)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
