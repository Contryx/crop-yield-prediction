import streamlit as st


def set_background(image_url):
    """
    background image
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_background("https://images.nationalgeographic.org/image/upload/v1638892233/EducationHub/photos/crops-growing-in-thailand.jpg") 




import streamlit as st
import joblib
import pandas as pd

mlp_model = joblib.load("mlp_model.pkl")
dt_model = joblib.load("decision_tree.pkl")

# labels, reduce spacing, and add white boxes
st.markdown(
    """
    <style>
        .title {
            color: black !important;
            font-size: 26px !important;
            font-weight: bold !important;
            text-align: center;
        }

        /* label styling
        .stNumberInput label, .stSelectbox label {
            font-size: 14px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 2px 5px !important; 
            border-radius: 3px !important; 
            display: inline-block;
            margin-bottom: -2px !important; 
        }

        /*gap between inputs */
        div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
            margin-top: -2px !important; 
        }

        /*improve button visibility */
        div.stButton > button {
            font-size: 18px !important;
            padding: 12px 24px;
            font-weight: bold !important;
            background-color: white !important;
            border-radius: 8px;
            border: none;
        }
        .result-box {
            font-size: 20px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-top: 15px;
            border: 2px solid black;
        }
        .warning-box {
            font-size: 16px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid red;
            color: black !important;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">Crop Yield Prediction</h1>', unsafe_allow_html=True)

#user Inputs
average_rain_fall_mm_per_year = st.number_input("**Avg Rainfall (mm/year):**", min_value=0.0, value=0.0)
avg_temp = st.number_input("**Avg Temperature (°C):**", min_value=-10.0, value=0.0)
pesticides_tonnes = st.number_input("**Pesticides (tonnes):**", min_value=0.0, value=0.0)
area = st.selectbox("**Location:**", ["India", "Europe"])

#crop type
item_options = ["Maize", "Potatoes", "Rice, paddy", "Sorghum", "Wheat"]
item = st.selectbox("**Crop Type:**", item_options)

#input Data
input_data = pd.DataFrame({
    'average_rain_fall_mm_per_year': [average_rain_fall_mm_per_year],
    'avg_temp': [avg_temp],
    'pesticides_tonnes': [pesticides_tonnes],
    'Area': [area],
    'Item': [item]
})

#prediction
if st.button("Predict Yield"):
    if average_rain_fall_mm_per_year == 0 and avg_temp == 0 and pesticides_tonnes == 0:
        st.markdown(
            '<div class="warning-box">⚠️ Please enter valid values for rainfall, temperature, and pesticides to get a prediction.</div>',
            unsafe_allow_html=True
        )
    else:
        try:
            model = dt_model if area == "India" else mlp_model

            input_data = pd.DataFrame({
                'average_rain_fall_mm_per_year': [average_rain_fall_mm_per_year],
                'avg_temp': [avg_temp],
                'pesticides_tonnes': [pesticides_tonnes],
                'Area': [str(area)],
                'Item': [str(item)]
            })

            prediction = model.predict(input_data)[0]

            st.markdown(
                f'<div class="result-box"><b>Predicted Yield for {area} ({item}):</b> <br> <span style="font-size:22px;">{prediction:.2f} hg/ha</span></div>',
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error making prediction: {e}")
