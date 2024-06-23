import streamlit as st 
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Load the model
try:
    model = joblib.load('model1.joblib')
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

def predict_kw(input_data):
    # Predict the KW using the loaded model
    prediction = model.predict(input_data)
    return prediction

st.markdown("# Power Consumption Prediction")

st.write("Welcome to the power consumption prediction app")

# Input fields
shift = st.selectbox("Shift", (1, 2, 3))
MSU = st.number_input("MSU")

st.write("Line Status")
LineNotStaffed = st.slider("Line Not Staffed", 0, 10)
STNU = st.slider("STNU", 0, 10)
STNUVAR = st.slider("STNU VAR", 0, 10)
EO = st.slider("EO NON SHIPPABLE", 0, 10)
Shutdown = st.radio("Shutdown", ['Yes', 'No'], horizontal=True)

# Convert Shutdown to numerical value
Shutdown = 1 if Shutdown == 'Yes' else 0

# Prepare input data as DataFrame
input_data = pd.DataFrame([[shift, MSU, LineNotStaffed, STNU, STNUVAR, EO, Shutdown]],
                          columns=['Shift', 'MSU', 'LineNotStaffed', 'STNU', 'STNUVAR', 'EO', 'Shutdown'])

if st.button('Predict'):
    prediction = predict_kw(input_data)
    st.write(f"Predicted KW: {prediction[0]}")
