import streamlit as st
import time
st.title('Startup Dashboard')
st.header('I am learning streamlit app')
st.subheader('loving it ')
st.write('This is plane text ')
st.markdown("""
### My favourite food 
- North Indian food
- Plain Thali 
""")
st.code("""
def square(num):
   return  num**2
x=square(5)
""")
st.latex('x^2 +y^2+2=0')
# Display element

import pandas as pd
df=pd.DataFrame({
    'name':['Sumit','Amit','Ankit'],
    'cgpa':[7,8,9],
    'package':[13,4,22]
})
st.dataframe(df)
st.metric('Revenue','Rs 3L','3%')
st.json({
    'name':['Sumit','Amit','Ankit'],
    'cgpa':[7,8,9],
    'package':[13,4,22]
})
# Display media
st.image('Screenshot 2025-10-02 184730.png')
st.video('vid.mp4')
# Creating layouts
st.sidebar.title('Menu')
col1,col2=st.columns(2)
with col1:st.image('Screenshot 2025-10-02 184730.png')
with col2:st.image('Screenshot 2025-10-02 184730.png')
st.error('Login Failed')
st.success('Login Successful')
# progressbar=st.progress(0)
# for i in range(1,100):
#     time.sleep(0.1)
#     progressbar.progress(i)
email=st.text_input('Enter your email')
password=st.text_input('Enter your password')
gender=st.selectbox('Select gender',['Male','Female','others'])
st.write(gender)
bt=st.button('Submit')
if bt:
    if email=='dubeyvimlendu@gmail.com'and password=='dubey@123':
        st.balloons()
    else:
        st.error('Login Failed')
# file uploading function
file=st.file_uploader('Upload file')
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())



