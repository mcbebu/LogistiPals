import streamlit as st
import subprocess
import pathlib
import os

from PIL import Image
from model import *

# Setting Page Layout
# st.set_page_config(layout="wide", page_title="Ninjavan")
# col1, col2, col3 = st.columns((15 ,15, 15))

# with st.sidebar:

#     st.title("Select your filters here:")

st.title("CodeDojo '23")

st.caption("Done by: Kwang Yang, Marcus, Anders, Sourick")

st.write("NinjaLens - Computer Vision ensuring accurate parcel sizing inputs from the seller's end to increase efficacy through the seller-to-warehouse process segment, omitting the 'rejection pile' of packages, as well as disputes between sellers and NinjaVan")

def calculate(dims):
    
    closest_pair = None
    closest_distance = float('inf')

    for i in range(len(dims)):
        for j in range(i+1, len(dims)):
            distance = abs(dims[i] - dims[j])
            if distance < closest_distance:
                closest_distance = distance
                closest_pair = (dims[i], dims[j])

    avg = sum(closest_pair)/2
    dims.remove(closest_pair[0])
    dims.remove(closest_pair[1])
    st.write(avg, dims[0], dims[1])
    return avg + sum(dims)

def get_image():

    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if image_file is not None:
        res = []
        for i in image_file:
            image = Image.open(i)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            res.extend(max_dim(image))

    st.subheader("The total length is:")
    st.write(calculate(res))

get_image()

