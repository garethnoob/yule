import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    df = df[df['Made'] > 0]  # Filter rows where 'Made' is greater than 0
    return df

file = st.file_uploader('choose a file', type=['xlsx', 'xlsm'])

if file is not None:
    df = read_excel(file)
    
    
    if 'Made' in df.columns and 'Planned' in df.columns:
        grouped_weeks = df.groupby(by=['WeekNumber'])[['Planned', 'Made']].sum().reset_index()
        grouped_weeks['ctp'] = round((grouped_weeks['Made'] / grouped_weeks['Planned'] )*100,2) # Calculate the ctp column
        grouped_weeks[' '] = ['✅' if ctp >= 100 else '❌' for ctp in grouped_weeks['ctp']]  # Add a column with checkmarks or crosses
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric(label='Total Planned', value=f"{grouped_weeks['Planned'].sum():,.0f}")
        with col2:
            st.metric(label='Total Made', value=f"{grouped_weeks['Made'].sum():,.0f}")
        with col3:
            total_ctp = (grouped_weeks['Made'].sum() / grouped_weeks['Planned'].sum()) * 100
            st.metric(label='Total CTP', value=f"{total_ctp:.2f}%")

        with st.expander('Data'):
            st.dataframe(grouped_weeks, use_container_width=True)
        

        chart = alt.Chart(grouped_weeks).transform_fold(
            ['Planned', 'Made'],
            as_=['Type', 'Value']
        ).mark_bar().encode(
            x=alt.X('WeekNumber:O', title='Week Number', axis=alt.Axis(labelAngle=45)),
            xOffset=alt.XOffset('Type:N', sort=['Planned', 'Made']),
            y=alt.Y('Value:Q', title='Count'),
            color=alt.Color('Type:N', sort=['Planned', 'Made']),
        )

        st.altair_chart(chart, use_container_width=True)
        
    else:
        st.error("The uploaded file does not contain the required columns 'Made' and 'Planned'.")