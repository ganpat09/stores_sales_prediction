import streamlit as st
import joblib
import pandas as pd
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



model_path = os.path.join(current_path,"prediction_service","model.pkl")
with open(model_path, 'rb') as handle:
    model = joblib.load(handle)


item_Identifier = st.text_input(label="Item Identifier")
item_Weight = st.text_input(label="Item Weight")

item_Fat_Content = st.selectbox("Item Fat Content",('Low Fat', 'Regular'))
item_Visibility = st.text_input(label="Item Visibility")
item_Type = st.selectbox("Item Type", (
    'Fruits and Vegetables', 
    'Snack Foods', 
    'Household', 
    'Frozen Foods', 
    'Dairy', 
    'Canned', 
    'Baking Goods', 
    'Health and Hygiene', 
    'Soft Drinks', 
    'Meat', 
    'Breads', 
    'Hard Drinks', 
    'Others', 
    'Starchy Foods', 
    'Breakfast', 
    'Seafood') )

item_MRP = st.text_input(label="Item MRP")
outlet_Identifier = st.text_input(label="Outlet Identifier")
outlet_Establishment_Year = st.text_input(label="Outlet Establishment Year")
outlet_Size = st.selectbox("Outlet Size",("Medium","Small","High" ))
outlet_Location_Type = st.selectbox("Outlet Location Type",(
     'Tier 3',  
     'Tier 2',  
     'Tier 1'  ))
outlet_Type = st.selectbox("Outlet Type",(
   'Supermarket Type1',    
    'Grocery Store',        
    'Supermarket Type3',     
    'Supermarket Type2')
)


if st.button('Submit'):
   data = {
   'Item_Identifier'            :  item_Identifier ,
   'Item_Weight'                :  float(item_Weight),
   'Item_Fat_Content'           :  item_Fat_Content ,
   'Item_Visibility'            :  float(item_Visibility),
   'Item_Type'                  :  item_Type ,
   'Item_MRP'                   :  float(item_MRP),
   'Outlet_Identifier'          :  outlet_Identifier, 
   'Outlet_Establishment_Year'  :  int(outlet_Establishment_Year) ,
   'Outlet_Size'                :  outlet_Size,
   'Outlet_Location_Type'       :  outlet_Location_Type,
   'Outlet_Type'                :  outlet_Type,
   }
   df = pd.DataFrame(data=data,index=[0])
   result = model.predict(df)
   st.write("result = {0}".format(result))



















