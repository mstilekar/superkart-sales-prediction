
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
superkart_api = Flask("superkart_sales_api")
CORS(superkart_api)

# Load the trained model pipeline (preprocessing + model)
model = joblib.load("superkart_model.joblib")
MODEL_INPUT_COLUMNS = [
    'Product_Weight',
    'Product_Sugar_Content',
    'Product_Allocated_Area',
    'Product_MRP',
    'Store_Size',
    'Store_Location_City_Type',
    'Store_Type',
    'Product_Id_char',
    'Store_Age_Years',
    'Product_Type_Category'
]
MODEL_NUMERIC_COLUMNS = [
    'Product_Weight',
    'Product_Allocated_Area',
    'Product_MRP',
    'Store_Age_Years'
]

# Health check route
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API"

# Prediction route
@superkart_api.post('/v1/predict')
def predict_sales():
    try:
        # Parse JSON payload
        data = request.get_json()
        print("Raw incoming data:", data)

        # Validate expected fields
        missing_fields = [field for field in MODEL_INPUT_COLUMNS if field not in data]
        if missing_fields:
            return jsonify({'error': f"Missing fields: {missing_fields}"}), 400

        # Convert and transform input
        sample = {
            'Product_Weight': float(data['Product_Weight']),
            'Product_Sugar_Content': data['Product_Sugar_Content'],
            'Product_Allocated_Area': float(data['Product_Allocated_Area']),
            'Product_MRP': float(data['Product_MRP']),
            'Store_Size': data['Store_Size'],
            'Store_Location_City_Type': data['Store_Location_City_Type'],
            'Store_Type': data['Store_Type'],
            'Product_Id_char': data['Product_Id_char'],
            'Store_Age_Years': int(data['Store_Age_Years']),
            'Product_Type_Category': data['Product_Type_Category']
        }

        input_df = pd.DataFrame([sample])
        print("Transformed input for model:\n", input_df)

        # Make prediction
        prediction = model.predict(input_df).tolist()[0]
        return jsonify({'Predicted_Sales': prediction})

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    if not request.files:
        return jsonify({'error': 'Upload a CSV file using multipart/form-data.'}), 400

    uploaded_file = next(iter(request.files.values()))
    try:
        batch_df = pd.read_csv(uploaded_file)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        return jsonify({'error': f"Could not read CSV file: {str(e)}"}), 400

    if batch_df.empty:
        return jsonify({'error': 'CSV file contains no prediction rows.'}), 400

    missing_fields = [field for field in MODEL_INPUT_COLUMNS if field not in batch_df.columns]
    if missing_fields:
        return jsonify({'error': f"Missing CSV columns: {missing_fields}"}), 400

    batch_df = batch_df[MODEL_INPUT_COLUMNS].copy()
    try:
        batch_df[MODEL_NUMERIC_COLUMNS] = batch_df[MODEL_NUMERIC_COLUMNS].apply(
            pd.to_numeric,
            errors='raise'
        )
    except (TypeError, ValueError) as e:
        return jsonify({'error': f"CSV contains invalid numeric values: {str(e)}"}), 400

    try:
        predictions = model.predict(batch_df).tolist()
        return jsonify({'Predicted_Sales': predictions})
    except Exception as e:
        print("Error during batch prediction:", str(e))
        return jsonify({'error': f"Batch prediction failed: {str(e)}"}), 500

# Run the app (for local testing only)
if __name__ == '__main__':
    superkart_api.run(debug=True)
