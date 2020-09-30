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

st.title('Publish or perish: data-driven choice of book keywords and categories for Kindle Direct Publishing')

book_title = st.text_input('Enter the title of the book:')
book_description = st.text_input('Enter the description of the book:')
book_labels = st.text_input('Enter the labels of the book:')



# df1 = pd.read_csv('../../data/books_25_pages_clean0.csv',skipinitialspace=True)
# num_half = int(len(df1.index)/2)
# df_train = df1.sample(frac=1).head(n=num_half)
# features = ['kindle_price','author_num_unique_books','genre_audiobook_percent','genre_business_percent','genre_mental-health_percent','genre_personal-development_percent','genre_philosophy_percent','genre_productivity_percent','genre_psychology_percent','genre_science_percent','genre_spirituality_percent','genre_self-help_percent']
# X_train = df_train[features]
# y_train = df_train['reviews_per_month_since_published']
# ols = sm.OLS(y_train,X_train)
# ols_result = ols.fit()
# 
# df_coeff = pd.DataFrame(ols_result.params).reset_index()
# df_coeff = df_coeff.rename(columns={0:'importance','index':'label'})
#  
# df_coeff = df_coeff.sort_values(by=['importance'],ascending=False).reset_index(drop=True)
# df_coeff['importance'] = df_coeff.apply(lambda row: row['importance']/10,axis=1)
# new_values = []
# for vali in df_coeff['label'].values: 
#     if 'genre' in vali: new_values.append(vali.split("genre_")[1].split("_percent")[0])
#     else: new_values.append(vali)
#     
# df_coeff['label'] = new_values
# 
# 
# 
# main_category = st.selectbox("Main category: ", ['self-help','science-fiction'])
# 
# dict_include = {
#     'self-help':["science","philosophy","mental-health","personal-development"],
#     'science-fiction':['a','b']
#     }
# dict_exclude = {
#     'self-help':["business","psychology"],
#     'science-fiction':['c','d']
#     }
# include_words = st.multiselect("Include:", dict_include[main_category])
# exclude_words = st.multiselect("Exclude:", dict_exclude[main_category])



























# st.dataframe(df_coeff)

# scale_bar = 10.0
# # Add a slider to the sidebar:
# side_bars = []
# side_bars.append(st.sidebar.slider(
#     'Importance of tag: science',
#     0.0, scale_bar
# ))
# side_bars.append(st.sidebar.slider(
#     'Importance of tag: audiobook',
#     0.0, scale_bar
# ))
# side_bars.append(st.sidebar.slider(
#     'Importance of tag: philosophy',
#     0.0, scale_bar
# ))
# side_bars.append(st.sidebar.slider(
#     'Importance of tag: mental-health',
#     0.0, scale_bar
# ))
# side_bars.append(st.sidebar.slider(
#     'Importance of tag: personal-development',
#     0.0, scale_bar
# ))

# sum_s = np.sum(side_bars)
# target_importance = []
# importance_values = df_coeff['importance'].values[0:5]
# for valuei in importance_values:
#     target_importance.append(scale_bar*valuei/np.sum(importance_values))
# 
# labels_df = df_coeff['label'].values[0:5]
# for indexi in range(0,5):
#     change = 'increase' if target_importance[indexi]-side_bars[indexi] < 0 else 'decrease'
#     'If you '+change+' the importance of the label "'+labels_df[indexi]+'" by ' +str(abs(round(target_importance[indexi]-side_bars[indexi],1))) + ' you can get ' + str(round(importance_values[indexi],1)) + ' more reviews per month'



