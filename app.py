import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Import the model
pipe = pd.read_pickle(r"pipe.pkl")
df = pd.read_pickle(r"df.pkl")

# Set page configuration
st.set_page_config(
    page_title="LappyMatiks",
    page_icon="💻",
    layout="wide"
)


# Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Set the background color of the entire page */
        body {
            background-color: #1E3A5F; /* Deep Blue */
            color: Black;
        }

        /* Styling for the main content area */
        .main {
            background-color: #F5F5DC; /* Beige */
            color: Black; /* Text color */
            padding: 20px; /* Add padding inside the main container */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Light shadow effect */
        }

        /* Styling for the title */
        .stTitle {
            color: #2C2C2C; /* Dark Blue-Black */
            font-weight: bold; /* Make text bold */
        }

        /* Styling for the sidebar */
        .stSidebar {
            background-color: #F5F5DC; /* Beige */
            padding: 20px; /* Add padding inside the sidebar */
            border-radius: 10px; /* Rounded corners */
        }

        /* Styling for the buttons */
        .stButton>button {
            background-color: #1E3A5F; /* Dark Blue */
            color: #F5F5DC; /* Beige text color */
            border-radius: 8px; /* Rounded button corners */
            font-size: 16px; /* Increase button text size */
            font-weight: bold; /* Make button text bold */
            padding: 10px 20px; /* Add padding inside buttons */
        }

        /* Change button color on hover */
        .stButton>button:hover {
            background-color: #162A47; /* Slightly darker blue */
        }

        /* Styling for the success message */
        .stSuccess {
            color: black !important;  /* Make text black */
            background-color: #D4E6F1 !important; /* Light blue background */
            padding: 10px; /* Add padding */
            border-radius: 5px; /* Rounded corners */
            font-weight: bold; /* Make text bold */
        }

        /* Styling for horizontal lines */
        hr {
            border: 1px solid #2C2C2C; /* Dark Blue-Black */
        }

        /* Set all form labels (parameter names like Brand, SSD, HDD, etc.) to black */
        label {
            color: black !important; /* Make all form labels black */
            font-weight: bold; /* Make labels bold */
        }

        /* Styling for warning messages (e.g., 'Please fill in either HDD or SSD value.') */
         .stWarning {
            color: black !important; /* Make warning text black */
            font-weight: bold; /* Make text bold */
        }
        /* Styling for the footer message (e.g., 'Suhani@2024. All rights reserved.') */
        .stFooter {
            color: black !important; /* Make footer text black */
            font-weight: bold; /* Make text bold */
            text-align: center; /* Center align footer text */
            margin-top: 20px; /* Add spacing above the footer */
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Page Header
st.markdown("<h1 class='stTitle'>LappyMatiks</h1>", unsafe_allow_html=True)
st.write("Welcome to the Laptop Price Predictor. Input the details of the laptop configuration and predict its price!")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "Why guess when you can predict?  Enter your specs and get an instant estimate !! "
)
st.sidebar.markdown("## Made by:")
st.sidebar.markdown("- **Name:** 👩‍💻 Suhani Pandey")
st.sidebar.markdown("- **College:** 📍 IIIT Allahabad")
st.sidebar.markdown("- **🎓 Enrollment No: IEC2022041")

# Input Form
with st.form("laptop_form"):
    col1, col2 = st.columns(2)

    company = col1.selectbox('Brand', df['Company'].unique())
    type = col2.selectbox('Type', df['TypeName'].unique())
    ram = col1.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    weight = col2.number_input('Weight (kg)', min_value=0.1, max_value=10.0, step=0.1, value=2.0)
    touchscreen = col1.selectbox('Touchscreen', ['No', 'Yes'])
    ips = col2.selectbox('IPS', ['No', 'Yes'])
    screen_size = col1.number_input('Screen Size (inches)', min_value=10, max_value=21, value=15)
    resolution = col2.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
                                                      '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
    cpu = col1.selectbox('CPU', df['Cpu brand'].unique())
    hdd = col2.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
    ssd = col1.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])
    gpu = col2.selectbox('GPU', df['Gpu brand'].unique())
    os = col1.selectbox('OS', df['os'].unique())

    # Predict Button
    predict_button = col2.form_submit_button('Predict Price')

# Prediction logic
if predict_button:
    if hdd == 0 and ssd == 0:
        st.markdown("<span class='stWarning'>⚠️ Please fill in either HDD or SSD value.</span>", unsafe_allow_html=True)
    else:
        touchscreen = 1 if touchscreen == 'Yes' else 0
        ips = 1 if ips == 'Yes' else 0
        X_res, Y_res = map(int, resolution.split('x'))
        ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size
        query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]).reshape(1, -1)
        predicted_price = int(np.exp(pipe.predict(query)[0]))

        # Display Prediction with Dark Blue Text
        st.markdown(
            f"<div class='stSuccess'>💰 The predicted price of this configuration is ₹ {predicted_price}</div>",
            unsafe_allow_html=True
        )

        # User feedback
        satisfaction = st.selectbox("Are you satisfied with the predicted price?", ["Yes", "No"])
        if satisfaction == "Yes":
            st.markdown("<span class='stSuccess'>✅ Thank you for your feedback!</span>", unsafe_allow_html=True)
        else:
            st.experimental_rerun()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='stFooter'>Suhani@2024. All rights reserved. | This web app is created for educational purposes.</div>", unsafe_allow_html=True)

