import streamlit as st
import streamlit.components.v1 as com
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import networkx as nx


from nodes import *
from Calculation import *
from chainViz import *

st.set_page_config(page_title="Machine replacement optimization")
st.sidebar.image("bewi_logo.png",use_column_width=True)
st.sidebar.write("Protecing people and goods for a better everyday")

st.title("Machine replacement optimization")

col1, col2, col3, col4 = st.columns(4)

with col1:
    start = st.number_input("Current age of the Machine",step=1,value=3)

with col2:
    max_age = st.number_input("Maximum machine age",step=1,value=6)

with col3:
    n = st.number_input("Number of decision years",step=1,value=5)

with col4:
    I = st.number_input("Cost of new machine",step=10000,value=100000)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    data = st.file_uploader("Upload data",type=["xlsx"])

with col2:
    if not data:
        df = pd.read_excel(r"C:\Users\Line\OneDrive\Dokumenter\Master Business Analytics\MSc Business Analytics\01 - Master Thesis\Data_and_model\Interface\Example datasett.xlsx")
        st.write("sample dataset")
        st.dataframe(df)
    else: 
        df = pd.read_excel(data)
        st.dataframe(df)


st.markdown("---")

btn = st.button("Optimize")
if btn:
    node = nodes(n,start,max_age)
    networkVisualisation = networkViz(node,max_age,n)
    
    st.markdown("---")
    st.markdown("## Network Visualisation")
    st.write(networkVisualisation)


    
    df_solution, chain = calucations(node,df,n,I,max_age)
    st.markdown("---")
    st.markdown("## Tabular solution")
    st.dataframe(df_solution)
    st.markdown(chain)
    
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")
    
    csv = convert_df(df_solution)

    st.download_button("Press to download",csv,"file.csv","text/csv",key="download-csv")


    st.markdown("---")
    st.markdown("## Decision chain")
    st.pyplot(ChainViz(chain))
    st.markdown("NB! if one of the decisions are 'R or K' there are more than one solution")
else:
    pass










