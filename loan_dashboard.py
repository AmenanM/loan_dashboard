import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui


# Load dataset
data = pd.read_csv('Loan_details_updated.csv')

# Data Cleaning & Feature Engineering
def classify_risk(row):
    if row['Credit_Score'] < 600 and row['Income'] < 30000:
        return 'High Risk'
    elif row['Credit_Score'] >= 600 and row['Income'] >= 30000:
        return 'Low Risk'
    else:
        return 'Medium Risk'

data['Risk_Category'] = data.apply(classify_risk, axis=1)

# Add income brackets
bins = [0, 30000, 60000, 90000, 120000, 150000]
labels = ['<30k', '30k-60k', '60k-90k', '90k-120k', '>120k']
data['Income_Bracket'] = pd.cut(data['Income'], bins=bins, labels=labels)

st.set_page_config(layout="wide")
# Streamlit Dashboard
st.title("Loan application dashboard")

# Subtitle
st.subheader("Insights to Empower Smarter Lending Decisions")
st.markdown(
    """
    Welcome to the **Loan Applicant Dashboard**! This tool helps banks analyze applicant data and make informed decisions. 

    ### Key Features:
    - **Filters**: Adjust age, income, credit score, and more in the sidebar.
    - **Visualizations**: Explore trends in demographics, loan amounts, and default rates.
    - **Risk Profiles**: Segment applicants into High, Medium, or Low Risk.

    Use the filters to customize the data and scroll down to explore insights!
    """
)


# Sidebar Filters
st.sidebar.header("Filter Options")
age_range = st.sidebar.slider("Select Age Range", int(data['Age'].min()), int(data['Age'].max()), (25, 50))
income_range = st.sidebar.slider("Select Income Range", int(data['Income'].min()), int(data['Income'].max()), (30000, 90000))
credit_range = st.sidebar.slider("Select Credit Score Range", int(data['Credit_Score'].min()), int(data['Credit_Score'].max()), (500, 800))
employment_status = st.sidebar.multiselect("Employment Status", data['Employment_Status'].unique(), default=data['Employment_Status'].unique())
marital_status = st.sidebar.multiselect("Marital Status", data['Marital_Status'].unique(), default=data['Marital_Status'].unique())
education_level = st.sidebar.multiselect("Education Level", data['Education_Level'].unique(), default=data['Education_Level'].unique())

# Apply filters to data
filtered_data = data[
    (data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1]) &
    (data['Income'] >= income_range[0]) & (data['Income'] <= income_range[1]) &
    (data['Credit_Score'] >= credit_range[0]) & (data['Credit_Score'] <= credit_range[1]) &
    (data['Employment_Status'].isin(employment_status)) &
    (data['Marital_Status'].isin(marital_status)) &
    (data['Education_Level'].isin(education_level))
]

# Display filtered dataset summary
st.subheader("Dataset Overview (Filtered)")
st.write(f"Total Applicants: {filtered_data.shape[0]}")
st.write(filtered_data)

# Applicant Distribution
st.subheader("1. Applicant Distribution")

# Age Distribution
st.write("### Age Distribution")
fig_age = px.histogram(filtered_data, x='Age', nbins=10, title='Age Distribution', labels={'x': 'Age', 'y': 'Count'})
st.plotly_chart(fig_age)

# Income Distribution
st.write("### Income Distribution")
fig_income = px.histogram(filtered_data, x='Income', nbins=10, title='Income Distribution', labels={'x': 'Income', 'y': 'Count'})
st.plotly_chart(fig_income)

# Loan Amount Analysis
st.subheader("2. Loan Amount Analysis")

# Average Loan Amount by Employment Status
st.write("### Average Loan Amount by Employment Status")
loan_employment = filtered_data.groupby('Employment_Status')['Loan_Amount'].mean().reset_index()
fig_loan_employment = px.bar(
    loan_employment, 
    x='Employment_Status', 
    y='Loan_Amount', 
    title='Average Loan Amount by Employment Status',
    labels={'Loan_Amount': 'Average Loan Amount', 'Employment_Status': 'Employment Status'}
)
st.plotly_chart(fig_loan_employment)

# Default Analysis
st.subheader("3. Default Analysis")

# Default Rate by Credit Score
st.write("### Default Rate by Credit Score")
default_rate = filtered_data.groupby('Credit_Score')['Defaulted'].mean().reset_index()
fig_default_rate = px.line(
    default_rate, 
    x='Credit_Score', 
    y='Defaulted', 
    title='Default Rate by Credit Score',
    labels={'Defaulted': 'Default Rate', 'Credit_Score': 'Credit Score'}
)
st.plotly_chart(fig_default_rate)

# Risk Profile Segmentation
st.subheader("4. Risk Profile Segmentation")

# Proportion of Applicants by Risk Category
st.write("### Risk Category Proportions")
risk_counts = filtered_data['Risk_Category'].value_counts().reset_index()
risk_counts.columns = ['Risk_Category', 'Count']
fig_risk = px.pie(
    risk_counts, 
    values='Count', 
    names='Risk_Category', 
    title='Proportion of Applicants by Risk Category'
)
st.plotly_chart(fig_risk)

# Download Processed Data
st.subheader("Download Processed Data")
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
