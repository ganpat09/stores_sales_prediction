import streamlit as st
import joblib
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
st.text(os.listdir())
model = joblib.load("prediction_service/model.pkl")
st.text_input(label="Item_Identifier")
st.text_input(label="Item_Weight")
st.text_input(label="Item_Fat_Content")
