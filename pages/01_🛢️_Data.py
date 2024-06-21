import streamlit as st
import pandas as pd


st.set_page_config(
    page_title='Data Page',
    page_icon='🛢️',
    layout='wide'
)


def show_datafram():
    data = pd.read_csv('./data/attrition.csv')
    df = st.dataframe(data)
    return df


if st.session_state['authentication_status']:
    st.title('IBM Attrition Database 🛢️')
    st.selectbox('', placeholder='Select  column type', options=['All columns', 'Numerical Columns', 'Categorical Columns'])
    show_datafram()
elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app from the home page')

