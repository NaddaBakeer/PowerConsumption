import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
import math

# Load the model
try:
    model = joblib.load('model.joblib')
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Prediction function
def predict_kw(input_data):
    prediction = model.predict(input_data)
    return prediction

# App title and introduction
st.markdown("# Power Insight")
st.write("Welcome to Power Insight app")

# Input fields
st.sidebar.markdown("## Input Parameters")
shift = st.sidebar.selectbox("Shift", (1, 2, 3))
MSU = st.sidebar.number_input("MSU")
LineNotStaffed = st.sidebar.slider("Line Not Staffed", 0, 10)
STNU = st.sidebar.slider("STNU", 0, 10)
STNUVAR = st.sidebar.slider("STNU VAR", 0, 10)
EO = st.sidebar.slider("EO NON SHIPPABLE", 0, 10)
Shutdown = st.sidebar.radio("Shutdown", ['Yes', 'No'])

# Convert Shutdown to numerical value
Shutdown = 1 if Shutdown == 'Yes' else 0

# Prepare input data as DataFrame
input_data = pd.DataFrame([[shift, Shutdown, MSU, LineNotStaffed, STNU, STNUVAR, EO]],
                          columns=['Shift', 'Shutdown', 'MSU', 'LineNotStaffed', 'STNU', 'STNUVAR', 'EO'])

# Prediction button and display
if st.sidebar.button('Predict'):
    prediction = predict_kw(input_data)
    st.sidebar.markdown(f"### Predicted KW: {math.sqrt(prediction[0]):.2f}")

# Display additional info or help
st.sidebar.markdown("### Need Help?")
st.sidebar.write("Adjust the input parameters on the left sidebar and click 'Predict' to see the predicted KW.")

# Footer or additional information
st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️ by Nadda Bakeer")

# Optional: Streamlit wide mode
# st.set_page_config(layout="wide")

# Main content (optional)
st.write("## Additional Insights")
st.write("Here you can provide additional insights or visualizations based on predictions or input data.")
