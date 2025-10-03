import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide",page_title='Startup Dashboard')

df=pd.read_csv('startup_clean.csv')

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
# errors='coerce' will convert invalid parsing to NaT
# Now you can safely extract the year
# df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
#     total invested amount
    total=round(df['amount'].sum())
    # st.metric('Total',str(total) + 'Cr')
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    num_startups=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total Amount:',str(total)+' Cr')

    with col2:
        st.metric('Max:',str(max_funding)+' Cr')

    with col3:
        st.metric('Avg Amount:',(str(round(avg_funding))) +' Cr')

    with col4:
        st.metric("Funded Startups:",num_startups)

    st.header('MoM Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3=plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)
def load_investor_details(investor):
    st.title(investor)

    # Filter rows for the selected investor
    filtered_df = df[df['Investor'].str.contains(investor, case=False, na=False)]

    # Last 5 investments
    last_5 = filtered_df[['date', 'startup', 'vertical', 'city', 'Type', 'amount']] \
                .sort_values('date', ascending=False).head(5)
    st.subheader('Last 5 Investments')
    st.dataframe(last_5)

    col1, col2 = st.columns(2)

    with col1:
        # Biggest investments
        big_series = filtered_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values, align='center')
        ax.set_ylabel('Amount')
        ax.set_xlabel('Startup')
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors invested in')

        # Group by vertical and sum amount for the selected investor
        grouped = filtered_df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
        top = grouped[:5]
        others = grouped[5:].sum()
        top['Others'] = others

        fig1, ax1 = plt.subplots(figsize=(6,6))
        top.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax1)
        ax1.set_ylabel('')  # remove y-label for clarity
        ax1.set_title('Top 5 Sectors + Others')
        st.pyplot(fig1)
    # print(df.info())
    # year on year investment
    # df.loc[:, 'year'] = df['date'].dt.year
    # df['year']=df['date'].dt.year
    year_series = filtered_df.groupby('year')['amount'].sum()

    # Plot using matplotlib
    st.subheader('YOY Investments')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)  # Use the Series directly
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Amount')
    ax2.set_title('YOY Investments')
    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
# df['Investors Name']=df['Investors Name'].fillna('Undisclosed')
if option=='Overall Analysis':
    # st.title('Overall Analysis')
    load_overall_analysis()
    # btn0=st.sidebar.button('Overall Analysis')
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    bt1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['Investor'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
    # st.title('Investor Analysis')
# General Analysis


