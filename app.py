import streamlit as st
from streamlit_option_menu import option_menu
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create the Streamlit app
with st.sidebar:
    selected = option_menu('Crop Recommendation System',
                            ['Crops Recommendation'],
                            icons=['activity'],
                            default_index=0)

if selected == 'Crops Recommendation':
    st.title('Croptelligent')
    st.write("**Empower your farming decisions with our app that leverages advanced predictive models using historical climate and crop data to forecast yields and manage risks, helping you optimize planting schedules and mitigate environmental impacts.**")
    
    # Create input fields for user to enter features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        N = st.text_input('Type of Crop')
    with col2:
        P = st.text_input('Season')
    with col1:
        state = st.text_input('State')
    with col2:
        production = st.text_input('Production')
    with col1:
        rainfall = st.text_input('Annual Rainfall')
    with col2:
        fertilizer = st.text_input('Fertilizer Name')
    with col1:
        y = st.text_input('Fertilizer Name')
            
    if st.button('Submit'):
        try:
            input_features = {
                "Type of Crop": str,
                "Season": str,
                "State": str,
                "Production": str,
                "Annual Ranfall": float(rainfall),
                "Fertilizer Name": str
            }
            
            print("Input features:", input_features)
            
            if float(temperature) > 40:
                st.warning("⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️")
                
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                farmer_phone_number = '+918567098852'
                message = f"Attention: ⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️"
                client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=farmer_phone_number)
            
            try:
                response = requests.post(FLASK_API_URL, json=input_features)
                if response.status_code == 200:
                    result = response.json()
                    crop = result.get("prediction")
                    # fertilizer_recommendation = result.get("fertilizer_recommendation")
                    
                    st.write(
                        f'<div style="background-color: black; padding: 15px; margin-bottom: 20px; border-radius: 5px; color: white; font-size: 20px;">'
                        f'Soil is fit to grow {crop}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    farmer_phone_number = '+918567098852'
                    message = f"Soil is suitable for growing {crop}.\n\nThank you for using our crop recommendation system."
                    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=farmer_phone_number)
                else:
                    st.error("Failed to get prediction from the server.")
            except requests.exceptions.ConnectionError:
                st.error("Error: Unable to connect to the server. Please make sure the server is running.")
        except ValueError:
            st.error("Invalid input. Please provide valid values for all features.")
