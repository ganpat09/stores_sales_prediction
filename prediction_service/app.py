import streamlit as st
import pickle
from pathlib import Path
import os
"""
# Welcome to Streamlit!

   Item_Identifier            :  object 
   Item_Weight                :  float
   Item_Fat_Content           :  object 
   Item_Visibility            :  float
   Item_Type                  :  object 
   Item_MRP                   :  float
   Outlet_Identifier          :  object 
   Outlet_Establishment_Year  :  int 
   Outlet_Size                :  object 
   Outlet_Location_Type       :  object 
   Outlet_Type                :  object 
   Item_Outlet_Sales          :  float

"""
current_path = os.getcwd()

st.text(current_path)
st.text(os.listdir(current_path))

# getting the current path

model_path = os.path.join(current_path,"prediction_service","model.pkl")
with open(model_path, 'rb') as handle:
    model = pickle.load(handle)


st.text_input(label="Item_Identifier")
st.text_input(label="Item_Weight")
st.text_input(label="Item_Fat_Content")
