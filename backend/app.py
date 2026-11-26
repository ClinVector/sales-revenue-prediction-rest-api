# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
rental_price_predictor_api = Flask("SuperKart Sales Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("sales_rev_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sales_rev_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Revenue Prediction API!"

# Define an endpoint for single property prediction (POST request)
@sales_rev_predictor_api.post('/v1/revenue')
def predict_sales_rev():
    """
    This function handles POST requests to the '/v1/revenue' endpoint.
    It expects a JSON payload containing SuperKart Store products details and returns
    the predicted sales revenue as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales_rev = model.predict(input_data)[0]

    # Calculate actual rev
    # predicted_rev = np.exp(predicted_sales_rev)

    # Convert predicted_sales_rev to Python float
    predicted_sales_rev = round(float(predicted_sales_rev), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Sale Revenue (in dollars)': predicted_sales_rev})


# Define an endpoint for batch prediction (POST request)
@sales_rev_predictor_api.post('/v1/revbatch')
def predict_sales_rev_batch():
    """
    This function handles POST requests to the '/v1/revbatch' endpoint.
    It expects a CSV file containing product details for multiple stores
    and returns the predicted sales revenue as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_sale_rev = model.predict(input_data).tolist()

    # Calculate actual prices
    # predicted_prices = [round(float(np.exp(log_price)), 2) for log_price in predicted_log_prices]

    # Create a dictionary of predictions with property IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(property_ids, predicted_sale_rev))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_rev_predictor_api.run(debug=True)
