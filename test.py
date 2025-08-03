import streamlit as st
import pandas as pd


@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    df = df[df['Made'] > 0]  # Filter rows where 'Made' is greater than 0
    return df

file = st.file_uploader('choose a file', type=['xlsx', 'xlsm'])

if file is not None:
    df = read_excel(file, engine="openpyxl")
    
    
    if 'Made' in df.columns and 'Planned' in df.columns:
        grouped_weeks = df.groupby(by=['WeekNumber'])[['Planned', 'Made']].sum().reset_index()
        grouped_weeks['ctp'] = round((grouped_weeks['Made'] / grouped_weeks['Planned'] )*100,2) # Calculate the ctp column
        grouped_weeks[' '] = ['✅' if ctp >= 100 else '❌' for ctp in grouped_weeks['ctp']]  # Add a column with checkmarks or crosses
        st.dataframe(grouped_weeks, use_container_width=True)
        st.bar_chart(data=grouped_weeks, x='WeekNumber', y=['Planned', 'Made'], stack=False)
    else:
        st.error("The uploaded file does not contain the required columns 'Made' and 'Planned'.")