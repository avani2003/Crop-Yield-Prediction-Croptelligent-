import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb

# Load data
data = pd.read_csv('crop_yield.csv')


# Streamlit app
st.title('Crop Yield Prediction')

st.write("At Croptelligent, we are deeply committed to addressing the critical challenges faced by global agriculture due to the impact of climate change. 
As the world's population continues to grow, projected to reach nearly 10 billion by 2050, the demand for food will increase substantially.")

# Input widgets
crop_options = ['Select Crop'] + data['Crop'].unique().tolist()
season_options = ['Select Season'] + data['Season'].unique().tolist()
state_options = ['Select State'] + data['State'].unique().tolist()

crop = st.selectbox('Crop', crop_options)
season = st.selectbox('Season', season_options)
state = st.selectbox('State', state_options)
production = st.number_input('Production')
annual_rainfall = st.number_input('Annual Rainfall')
fertilizer = st.number_input('Fertilizer')


# Preprocessing
categorical = ['Crop', 'Season', 'State']
label_encoders = {}
for col in categorical:
    label_encoder = LabelEncoder()
    data[col] = label_encoder.fit_transform(data[col])
    label_encoders[col] = label_encoder

scalar = StandardScaler()
features = ['Crop', 'Season', 'State', 'Production', 'Annual_Rainfall', 'Fertilizer']
data[features] = scalar.fit_transform(data[features])

# Train-test split
X = data.drop(['Yield','Crop_Year','Area','Pesticide'], axis=1)
y = data['Yield']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)

# Model training
reg = xgb.XGBRegressor()
reg.fit(X_train, y_train, verbose=100)


# Predict function
def predict_yield(crop, season, state, production, annual_rainfall, fertilizer):
    input_data = {
        'Crop': [crop],
        'Season': [season],
        'State': [state],
        'Production': [production],
        'Annual_Rainfall': [annual_rainfall],
        'Fertilizer': [fertilizer]
    }

    input_df = pd.DataFrame.from_dict(input_data)

    for col, encoder in label_encoders.items():
        input_df[col] = encoder.transform(input_df[col])

    input_df[features] = scalar.transform(input_df[features])

    prediction = reg.predict(input_df)
    return prediction[0]

# Prediction
if st.button('Predict Yield'):
    prediction = predict_yield(crop, season, state, production, annual_rainfall, fertilizer)
    st.write(f"Predicted Yield: {prediction:.3f} metric tonnes per unit area")

    clear = st.button('Clear')
    
    if clear:
        st.empty()
        crop = st.selectbox('Crop', crop_options)
        season = st.selectbox('Season', season_options)
        state = st.selectbox('State', state_options)
        production = st.number_input('Production')
        annual_rainfall = st.number_input('Annual Rainfall')
        fertilizer = st.number_input('Fertilizer')
