import sklearn
import pandas as pd
import streamlit as st
import joblib

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

model = joblib.load("model.pkl")
st.text_input(label="Item_Identifier")
st.text_input(label="Item_Weight")
st.text_input(label="Item_Fat_Content")
