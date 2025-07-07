import streamlit as st

st.title('Sign in')
st.caption('Please enter your username and password.')
st.divider()

@st.dialog('Alert')
def login_validation(usr,passw):
    if usr =='' or passw=='':
        st.error('Please enter your username or password')
    else:
        st.success('Login successful.')

with st.form('sign_in'):
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    submit_btn = st.form_submit_button(label="Submit",
                                       type="primary",
                                       use_container_width=True)
    
    google_btn = st.form_submit_button(label="Continue with Google",
                                       type="secondary",                                       
                                       use_container_width=True,
                                       icon=":material/g_mobiledata:",)

    col1, col2 = st.columns(2)

    with col1:
        remember_box = st.checkbox('Remember me')

    with col2:
        forgot_pass = st.html('<p><a href="">Forgot password?</a></p>')

if submit_btn:
    login_validation(username, password)
