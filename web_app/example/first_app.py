import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

st.title('My first app')

chart_data = pd.DataFrame(
     np.random.randn(20, 1),
     columns=['a'])
 
st.line_chart(chart_data)

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected:', option

default_value_goes_here=3
user_input = st.text_input("label goes here", default_value_goes_here)

