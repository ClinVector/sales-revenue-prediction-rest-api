import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Revenue Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_Weight             = st.number_input("Weight of each product")
Product_Allocated_Area     = st.number_input("Ratio of the allocated display area of each product to the total display area")
Product_Sugar_Content      = st.selectbox("Sugar content in each product", ["Low Sugar", "No Sugar", "Regular"])
Product_MRP                = st.number_input("Maximum retail price of each product")
Store_Age_Years            = st.number_input("Store age in years")
Store_Size                 = st.selectbox("Size of the store depending on sq.", ["High", "Medium", "Small"])
Store_Location_City_Type   = st.selectbox("Type of city in store is located", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type                 = st.selectbox("Type of store depending on the products that are being sold", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_MRP': Product_MRP,
    'Store_Age_Years': Store_Age_Years,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/revenue", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sale Revenue (in dollars)']
        st.success(f"Predicted Sale Revenue (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/revbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
