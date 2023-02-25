import streamlit as st
import subprocess
import pathlib
import base64
import os

from PIL import Image
from rembg import remove
from model import *

st.title("NinjaLens | CodeDojo '23")
st.caption("Done by: Kwang Yang, Marcus, Anders, Sourick")
st.write("Integrating computer vision to ensure accurate parcel sizing inputs from the seller's end to increase efficacy through the seller-to-warehouse process segment, omitting the 'rejection pile' of packages, as well as disputes between sellers and NinjaVan")

# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://blog.ninjavan.co/wp-content/uploads/sites/3/2022/01/Thank-You-Ryo.png");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# add_bg_from_url() 

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('ninjavanbg.png')

def calculate(dims):
    closest_pair = None
    closest_distance = float('inf')
    for i in range(len(dims)):
        for j in range(i+1, len(dims)):
            distance = abs(dims[i] - dims[j])
            if distance < closest_distance:
                closest_distance = distance
                closest_pair = (dims[i], dims[j])

    if closest_pair:
        avg = sum(closest_pair)/2
        dims.remove(closest_pair[0])
        dims.remove(closest_pair[1])
        breakdown = st.checkbox('Show breakdown')
        if breakdown:
            st.write(avg, dims[0], dims[1])
        return avg + sum(dims)
    

def metrics(total):

    '''
    Please select your parcel size based on the following weight/dimensions (H+B+W):
    - Small (<4kg/80cm)
    - Medium (<10kg/120cm)
    - Large (<20kg/200cm)
    - Extra large (<30kg/300cm)
    '''
    if total == 0:
        return "No input detected"
    elif total <= 80:
        return "Your parcel size is small (<4kg/80cm)!"
    elif total <= 120:
        return "Your parcel size is medium (<10kg/120cm)!!"
    elif total <= 200:
        return "Your parcel size is large (<20kg/200cm)!!!"
    else:
        return "Your parcel size is extra large (<30kg/300cm)!!!!"

def get_image():

    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if image_file is not None:
        res = []
        for i in image_file:
            image = Image.open(i)
            image = remove(image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            res.extend(max_dim(image))

        total = calculate(res)
        
        if total:
            total = total * 1.15
            st.metric("Total dimension:", round(total,3))
            st.metric("Recomendation:", metrics(total))
            st.caption("*You will incur additional charges in the event that you underdeclare the size of your parcel")

get_image()
