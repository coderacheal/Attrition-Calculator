import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)

st.title("Predict Attrition!")


st.cache_resource()
def load_forest_pipeline():
    pipeline = joblib.load('./models/forest_pipeline.joblib')
    return pipeline


st.cache_resource()
def load_svc_pipeline():
    pipeline = joblib.load('./models/svc_pipeline.joblib')
    return pipeline



st.cache_resource(show_spinner='Models Loading...')
def select_model():
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox('Select a model', options=['Random Forest', 'SVC'], key='selected_model')
    with col2:
        pass

    if st.session_state['selected_model'] == 'Random Forest':
        pipeline = load_forest_pipeline()
    else:
        pipeline  = load_svc_pipeline()

    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder


def make_prediction(pipeline, encoder):
    age = st.session_state['age']
    department = st.session_state['department']
    distancefromhome = st.session_state['distancefromhome']
    education = st.session_state['education']
    education_field = st.session_state['education_field']
    environment_satisfaction = st.session_state['environment_satisfaction']
    job_satisfaction = st.session_state['job_satisfaction']
    marital_status = st.session_state['marital_status']
    monthly_income = st.session_state['monthly_income']
    number_of_companies_worked = st.session_state['number_of_companies_worked']
    work_life_balance = st.session_state['work_life_balance']
    years_at_company = st.session_state['years_at_company']

    # Create the row
    data = [[age, department, distancefromhome, education, education_field, environment_satisfaction, job_satisfaction, marital_status, monthly_income, number_of_companies_worked, work_life_balance, years_at_company]]

    # ccreate the columns
    columns = ['Age', 'Department', 'DistanceFromHome', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'JobSatisfaction', 'MaritalStatus', 'MonthlyIncome', 'NumCompaniesWorked','WorkLifeBalance', 'YearsAtCompany']

    # Make the dataframe
    df = pd.DataFrame(data, columns=columns)

    # Making a prediction and probablity
    pred = pipeline.predict(df)
    pred_int = int(pred[0])

    prediction = encoder.inverse_transform([pred_int])
    probability = pipeline.predict_proba(df)

    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction, probability


if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'probability' not in st.session_state:
    st.session_state['probability'] = None



def display_form():
    
    pipeline, encoder = select_model()

    with st.form('input-features'):

        col1, col2 = st.columns(2)

        with col1:
            st.write('#### Personal Info 👩🏿')
            st.number_input('Enter your age', key='age', min_value=18, max_value=60, step=1)
            st.selectbox('Select your marital status', options=['Single', 'Married', 'Divorced'], key='marital_status')
            st.number_input('What is you distance from home', key='distancefromhome', max_value=25, min_value=1)
            st.number_input('Enter your salary per month', key='monthly_income', min_value=1000, step=100)
            st.number_input('Enter your education in years: (1-High School, 2- College, 3-Bachelor, 4-Master, 5-PhD)', key='education', min_value=1, max_value=5, step=1)
            st.number_input('How many companies have you worked for?', min_value=1, max_value=20, step=1, key='number_of_companies_worked')

        with col2:
            st.write('#### Work Info 💼')
            st.selectbox('Select your department', options=['Sales', 'Research & Development', 'Human Resources'], key='department')
            st.selectbox('Enter what field of Education you have', options=['Life Sciences', 'Other', 'Medical', 'Marketing','Technical Degree','Human Resources'], key='education_field')
            st.number_input('Rate your satisfaction with the environement', max_value=4, min_value=1, step=1, key='environment_satisfaction')
            st.number_input('Rate your job satisfaction', max_value=4, min_value=1, step=1, key='job_satisfaction')
            st.number_input('Rate your work-life balance', max_value=4, step=1, key='work_life_balance', min_value=1)
            st.number_input('How many years have you worked in this company', key='years_at_company', min_value=1, step=1)
        
        st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))



if __name__ == '__main__':
    display_form()

    final_prediction = st.session_state['prediction'][0]
    probablity_of_yes = st.session_state['probability'][0][1]
    probablity_of_no = st.session_state['probability'][0][0]

    if not final_prediction:
        st.write('### Predictions shows here!')
        st.divider()
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'### Prediction: {final_prediction}')
        with col2:
            if final_prediction == 'No':
                st.write(f'### Probability: {round(probablity_of_no, 2)}')
            else:
                st.write(f'### Probability: {round(probablity_of_yes, 2)}')

    st.divider()

    st.write(st.session_state)

