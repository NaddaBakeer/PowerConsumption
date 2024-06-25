import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
import math
import os

# Define your logo URL
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Procter_%26_Gamble_logo.svg/1200px-Procter_%26_Gamble_logo.svg.png"

# Load the model
try:
    model = joblib.load('model.joblib')
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Define correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "123"

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to display logo and title before logging in
def display_logo_and_title_before_login():
    st.markdown(
        f"""
        <style>
            .logo-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: auto;
                margin-bottom: 30px;
            }}
            .logo-image {{
                max-height: 200px;
                max-width: 100%;
            }}
            .moto {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: auto;
                flex-direction: column;
            }}
            .moto_head {{
                padding: 5px;
                text-align: center;
                font-weight: 800;
                font-size: 80pt;
                color: #003DA5ff;
                margin-bottom: 0px;
                background: linear-gradient(to bottom right, #003DA5ff, rgb(15, 69, 156));
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                -webkit-text-fill-color: transparent;
            }}
            .moto_head_sub {{
                padding: 5px;
                font-weight: 200;
                font-size: 27pt;
                color: #20ec01;
                margin-left: 5px;
            }}
        </style>
        <div class="logo-container">
            <a href="{LOGO_URL}" target="_blank">
                <img src="{LOGO_URL}" class="logo-image">
            </a>
        </div>
        <div class="moto">
            <h2 class="moto_head"><span style="color: #003DA5ff;">Power</span> Insight</h2>
            <h4 class="moto_head_sub">For more efficient energy use</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display logo and title after logging in
def display_logo_and_title_after_login():
    st.markdown(
        f"""
        <style>
            .logo-container {{
                display: flex;
                justify-content: flex-start;
                align-items: center;
                height: auto;
                margin-bottom: 7px;
            }}
            .logo-image {{
                max-height: 70px;
                max-width: 100%;
            }}
        </style>
        <div class="logo-container">
            <a href="{LOGO_URL}" target="_blank">
                <img src="{LOGO_URL}" class="logo-image">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
# Display the appropriate logo and title based on login state
if st.session_state.logged_in:
    display_logo_and_title_after_login()
else:
    display_logo_and_title_before_login()

# Display the login form
if not st.session_state.logged_in:
    st.sidebar.markdown("## Sign in")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Check if the username and password match
    if st.sidebar.button("Login" , type='primary'):
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.session_state.logged_in = True
            st.sidebar.success("Logged in as {}".format(username))
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password. Please try again.")

# If already logged in, show logged-in state
if st.session_state.logged_in:
    st.write("Welcome back, {} !".format(CORRECT_USERNAME))

    # Initialize input data list
    CSV_FILE = 'Shift Prediction.csv'
    TEMP_CSV = 'Shift.csv'
    temp_data=[]
    # Function to add a new shift
    def add_new_shift():
        if os.path.exists(TEMP_CSV):
            temp_data = pd.read_csv(TEMP_CSV)
            shift = len(temp_data) + 1
        else:
            shift = 1

        current_data = {
            'Shift': shift,
            'MSU': MSU,
            'LineNotStaffed': LineNotStaffed,
            'STNU': STNU,
            'STNUVAR': STNUVAR,
            'EO': EO,
            'Shutdown': Shutdown
        }
        new_data_df = pd.DataFrame([current_data])

        # Append to the main CSV without the header
        if os.path.exists(CSV_FILE):
            new_data_df.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            new_data_df.to_csv(CSV_FILE, mode='w', header=True, index=False)

        # Update the temporary CSV
        if os.path.exists(TEMP_CSV):
            temp_data = pd.read_csv(TEMP_CSV).tail(2)  # Keep the last 2 shifts
            temp_data = pd.concat([temp_data, new_data_df])
            temp_data.to_csv(TEMP_CSV, index=False)
        else:
            new_data_df.to_csv(TEMP_CSV, header=True, index=False)
        
        st.success("Shift {} added successfully!".format(shift), icon="✅")

    # Default input fields for a single shift
    MSU = st.number_input("MSU")
    LineNotStaffed = st.slider("Line Not Staffed", 0, 10)
    STNU = st.slider("STNU", 0, 10)
    STNUVAR = st.slider("STNU VAR", 0, 10)
    EO = st.slider("EO NON SHIPPABLE", 0, 10)
    Shutdown = st.radio("Shutdown", ['Yes', 'No'], index=0, key="shutdown_1")

    # Convert Shutdown to numerical value
    Shutdown = 1 if Shutdown == 'Yes' else 0

    # Button to add a new shift
    if st.button('Add Shift'):
        add_new_shift()

    # Button to predict KW for all shifts
    if st.button('Predict', type='primary'):
        if os.path.exists(TEMP_CSV):
            # Read shift data from temporary CSV
            input_data = pd.read_csv(TEMP_CSV)

            # Predict KW for each shift
            predictions = model.predict(input_data[['Shift', 'Shutdown', 'MSU', 'LineNotStaffed', 'STNU', 'STNUVAR', 'EO']])

            # Apply sqrt transformation
            predictions = [math.sqrt(pred) for pred in predictions]

            # Display results in a table
            results_df = pd.DataFrame({
                'Shift': input_data['Shift'],
                'Forecasted KW': predictions
            })
            st.write("## Forecasted KW for Each Shift")
            st.write(results_df)
        else:
            st.warning("No shifts added yet. Please add shifts before predicting.")
