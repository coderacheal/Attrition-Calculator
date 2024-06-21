import streamlit as st
import os
import pandas as pd


st.set_page_config(
    page_title='History Page',
    page_icon='🕰️',
    layout='wide'
)

def display_historic_predictions():

    csv_path = './data/history.csv'
    csv_exists = os.path.exists(csv_path)

    if csv_exists:
        history = pd.read_csv(csv_path)
        st.dataframe(history)



if __name__ == '__main__':
    st.title('History Page')
    display_historic_predictions()