import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('HBL_Dummy_Data.csv')

# Set up the title and description of the app
st.title("HBL Dummy Data Interactive Dashboard")
st.write("""
    Explore various statistics and visualizations of the HBL Dummy Data, including transaction flows, account types, and more!
""")

# Sidebar filters
st.sidebar.header("Filters")
account_type_filter = st.sidebar.multiselect(
    "Select Account Types", df['Account Type'].unique(), default=df['Account Type'].unique())
region_filter = st.sidebar.multiselect(
    "Select Region", df['Region'].unique(), default=df['Region'].unique())

# Apply filters to the dataset
filtered_data = df[df['Account Type'].isin(account_type_filter) & df['Region'].isin(region_filter)]

# Show filtered data (optional)
st.write("Filtered Data", filtered_data)

# Visualization 1: Account Type Distribution (Pie Chart)
st.subheader("Account Type Distribution")
account_type_counts = filtered_data['Account Type'].value_counts()
fig, ax = plt.subplots(figsize=(8, 8))
account_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3', ax=ax)
ax.set_ylabel('')
st.pyplot(fig)

# Visualization 2: Transaction Flow by Beneficiary Bank (Top 5 Beneficiaries by Region)
st.subheader("Top 5 Beneficiary Banks by Region (Credit Transactions)")
transaction_flow = filtered_data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
top_banks = transaction_flow.groupby('Region').apply(lambda x: x.nlargest(5, 'Credit')).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_banks, x='Transaction To', y='Credit', hue='Region', ax=ax)
ax.set_title('Top 5 Beneficiary Banks by Credit Transactions')
ax.set_xlabel('Beneficiary Bank')
ax.set_ylabel('Credit Amount')
st.pyplot(fig)

# Visualization 3: Geographic Heatmap of Transactions
st.subheader("Transaction Intensity by Region (Heatmap)")

# Aggregate data by region for heatmap
transaction_intensity = filtered_data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()

# Plotting Heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(transaction_intensity.set_index('Region').T, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
ax.set_title('Transaction Intensity by Region')
st.pyplot(fig)

# Visualization 4: Time-Based Analysis (if applicable)
if 'Date' in df.columns:
    st.subheader("Transaction Trends Over Time")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    time_trend = df.groupby('Year')[['Credit', 'Debit']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=time_trend, x='Year', y='Credit', label='Credit', ax=ax)
    sns.lineplot(data=time_trend, x='Year', y='Debit', label='Debit', ax=ax)
    ax.set_title('Transaction Trends Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount')
    st.pyplot(fig)

# Visualization 5: Anomalies in Transactions
st.subheader("Anomalies in Credit and Debit Transactions")

# Calculate Z-scores to find outliers
from scipy import stats
filtered_data['Z-score Credit'] = stats.zscore(filtered_data['Credit'])
filtered_data['Z-score Debit'] = stats.zscore(filtered_data['Debit'])

# Identify outliers (Z-score > 3 or < -3)
anomalies = filtered_data[(filtered_data['Z-score Credit'].abs() > 3) | (filtered_data['Z-score Debit'].abs() > 3)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=anomalies, x='Credit', y='Debit', hue='Account Type', style='Region', ax=ax)
ax.set_title('Anomalies in Credit and Debit Transactions')
ax.set_xlabel('Credit Amount')
ax.set_ylabel('Debit Amount')
st.pyplot(fig)

# Footer text
st.write("""
    ### Note:
    You can adjust filters in the sidebar to see the different visualizations based on your selections.
""")
