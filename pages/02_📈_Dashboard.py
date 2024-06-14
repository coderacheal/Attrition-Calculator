import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)

df = pd.read_csv('./data/attrition.csv')

def eda_dashboard():

    st.markdown('### Exploratory Data Analysis')

    col1, col2 = st.columns(2)

    with col1:
        scatter_plot = px.scatter(df, x='Age', y='MonthlyIncome', title='Age to Monthly Distribution',
                                  color='Attrition', color_discrete_map={'Yes': 'red', 'No': 'skyblue'})
        st.plotly_chart(scatter_plot)

    with col2:
        pass

    age_histogram = px.histogram(df, x='Age')
    st.plotly_chart(age_histogram)





def kpi_dashboard():
    st.markdown('### Key Performance Indicators')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="background-color: #CCE5FF; border-radius: 10px; width: 80%; margin-top: 20px;" >
                <h3 style="margin-left: 30px">Quick Stats About Dataset</h3>
                <hr>
                <h5 style="margin-left: 30px"> Attrition Rate: {(df['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100):.2f}%.</h5>
                <hr>
                <h5 style="margin-left: 30px">Average Monthly Income: ${df['MonthlyIncome'].mean():.2f}</h5>
                <hr>
                <h5 style="margin-left: 30px">Data Size: {df.size}</h5>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        pass


if __name__ == '__main__':

    st.title("Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        pass
    with col2:
        st.selectbox('Select the type of Dashboard', options=['EDA', 'KPI'], key='selected_dashboard_type')

    if st.session_state['selected_dashboard_type'] == 'EDA':
        eda_dashboard()
    else:
        kpi_dashboard()