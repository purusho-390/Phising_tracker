import streamlit as st
from urllib.parse import urlparse
from tensorflow import keras
import re

# Feature extraction functions
def fd_length(url):
    try:
        return len(urlparse(url).path.split('/')[1])
    except IndexError:
        return 0

def digit_count(url):
    return sum(1 for char in url if char.isnumeric())

def letter_count(url):
    return sum(1 for char in url if char.isalpha())

def no_of_dir(url):
    return urlparse(url).path.count('/')

def having_ip_address(url):
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    return -1 if ip_pattern.search(url) else 1

def hostname_length(url):
    return len(urlparse(url).netloc)

def url_length(url):
    return len(urlparse(url).path)

def get_counts(url):
    count_features = ['-', '@', '?', '%', '.', '=', 'http', 'https', 'www']
    return [url.count(char) for char in count_features]

# Feature extraction function
def extract_features(url):
    url_features = [
        hostname_length(url),
        url_length(url),
        fd_length(url),
        *get_counts(url),
        digit_count(url),
        letter_count(url),
        no_of_dir(url),
        having_ip_address(url)
    ]
    return url_features

# Model prediction function
def get_prediction(url):
    model_path = "/content/drive/MyDrive/Phising_ML/Url_model.h5"
    model = keras.models.load_model(model_path)

    url_features = extract_features(url)
    prediction = model.predict([url_features])

    probability = round(prediction[0][0] * 100, 3)
    
    if probability < 10:
        result = "The website is more safe."
    elif probability < 25:
        result = "The website is quite safe."
    elif probability < 50:
        result = "The website is having some malicious activity."
    else:
        result = "Restricted!!! Malicious website detected."

    return probability, result

# Streamlit app
st.title("URL Maliciousness Prediction")

url_input = st.text_input("Enter URL:")
submit_button = st.button("Submit")
reset_button = st.button("Reset")

if submit_button:
    if url_input:
        probability, result = get_prediction(url_input)
        st.write(f"Prediction: There is {probability}% chance the URL is malicious!")
        st.write(result)
    else:
        st.write("Please enter a URL.")

if reset_button:
    url_input = ""

# Footer
st.markdown(
    """
    <style>
    .footer {
        position:fixed,
        margin-top:200px,
        bottom: 0;
        width: 100%;
        color:black
        background-color: #f4f4f4;
        padding: 250px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
        Copyrights reserved by @xyz
    </div>
    """,
    unsafe_allow_html=True
)