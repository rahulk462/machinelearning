import streamlit as st
import pandas as pd
import json
import base64
import numpy as np
import joblib

@st.cache_resource
def load_model():
    # Load the trained model
    model_filename = 'marathon_time_predictor_model.joblib'
    loaded_model = joblib.load(model_filename)
    return loaded_model

# Load the trained model
loaded_model = load_model()

# Function to map user-friendly labels to encoded values
def encode_inputs(cross_training, gender, age_under_40):
    cross_training_mapping = {
        'No cross-training': 5,
        'Cyclist 13 hours': 0,
        'Cyclist 1 hour': 1,
        'Cyclist 3 hours': 2,
        'Cyclist 4 hours': 3,
        'Cyclist 5 hours': 4
    }

    gender_mapping = {
        'Male': 1,
        'Female': 0
    }

    age_under_40_mapping = {
        'Yes': 1,
        'No': 0
    }

    return (
        cross_training_mapping[cross_training],
        gender_mapping[gender],
        age_under_40_mapping[age_under_40]
    )

 
def set_custom_font_and_color():
    custom_font = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    * {
        font-family: 'Roboto', sans-serif;
        color: #000000;  /* Set default font color to black */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000;  /* Set heading color to black */
    }
    .stButton button {
        color: #FFFFFF;  /* Set button text color to white */
        background-color: #4CAF50;  /* Set button background color */
    }
    
    
    </style>
    """
    st.markdown(custom_font, unsafe_allow_html=True)


def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
                unsafe_allow_html=True)

      

def main():
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "About"])

    if page == "Home":
        #set_custom_font_and_color()
        #set_background("stockphoto3.jpg")

        st.title("Marathon Reader")
        st.write(
            "When running for a marathon, nothing is more important than the quality of training in advance. Many top marathon athletes work to have highly sophisticated training plans where they work to refine many aspects such as weekly kilometers and amount of cross training"
        )
        st.write("This web app works to give you advice on your training plan")
        with st.form(key='registration_form'):
            name = st.text_input('Name')
            kpw = st.number_input('KPW', min_value=0, max_value=200, value=18)
            cross_training = st.selectbox('Cross Training? ', ['No cross-training', 'Cyclist 13 hours',
                                                              'Cyclist 1 hour',
                                                              'Cyclist 3 hours',
                                                              'Cyclist 4 hours',
                                                              'Cyclist 5 hours'])
            speed = st.number_input('Speed',
                                    min_value=0.0,
                                    max_value=200.0,
                                    value=18.0,
                                    format="%.2f")
            wall = st.number_input('Wall',
                                   min_value=0.0,
                                   max_value=3.0,
                                   value=1.0,
                                   format="%.2f")
            sex = st.selectbox('Sex ', ['Male', 'Female'])
            age_under_40 = st.selectbox('Age under forty? ', ['Yes', 'No'])
            submit_button = st.form_submit_button(label='submit')
        encoded_cross_training, encoded_gender, encoded_age_under_40 = encode_inputs(cross_training, sex, age_under_40)

        # Create the feature DataFrame for prediction
        feature_data = pd.DataFrame({
            'km4week': [kpw],
            'sp4week': [speed],
            'CrossTraining': [encoded_cross_training],
            'Wall21': [wall],
            'Gender': [encoded_gender],
            'Age_Under_40': [encoded_age_under_40]
        })

        if submit_button:
           
            st.success(f"Registration successful for {name}!")
            st.write(
                f"Details:\nName: {name}\nWall: {wall}\nSpeed: {speed}\nKPW: {kpw}\nSex: {sex}"
            )
            predicted_time = loaded_model.predict(feature_data)[0]

            # Display the prediction
            st.success(f"Predicted marathon time: {predicted_time:.2f} hours")
            

    elif page == "About":
        st.title("About Us")
        st.write(
            "My name is Rahul, and I run track for millburn and have run distance for 4 years now. I love to run and code, so I made this webapp"

            
        )
        st.write(
            "My motivation to create the webapp is to help inexpereinced runners get a sense for how fast they are going to run, and where to improve"
        )

        st.image("me.png")




if __name__ == "__main__":
    main()
    