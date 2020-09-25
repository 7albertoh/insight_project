import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import random
import statsmodels.api as sm
import time

random.seed(123)
np.random.seed(123)

st.title('My first app')

# chart_data = pd.DataFrame(
#      np.random.randn(20, 1),
#      columns=['a'])
#  
# st.line_chart(chart_data)

# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])
# 
# 'You selected:', option

default_value_goes_here=3
user_input = st.text_input("label goes here", default_value_goes_here)

'hello',user_input

df1 = pd.read_csv('../../data/books_25_pages_clean0.csv',skipinitialspace=True)
num_half = int(len(df1.index)/2)
df_train = df1.sample(frac=1).head(n=num_half)
features = ['kindle_price','author_num_unique_books']
features.extend(list(df1.columns[250:-2]))
X_train = df_train[features]
y_train = df_train['reviews_per_month_since_published']
ols = sm.OLS(y_train,X_train)
ols_result = ols.fit()
#
df_coeff = pd.DataFrame(ols_result.params).reset_index()
df_coeff = df_coeff.rename(columns={0:'importance','index':'genre'})
 
df_coeff = df_coeff.sort_values(by=['importance'],ascending=False).head()

st.dataframe(df_coeff)


