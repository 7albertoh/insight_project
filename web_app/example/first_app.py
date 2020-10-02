import streamlit as st
import numpy as np
import pandas as pd
import random
import statsmodels.api as sm
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from num2words import num2words
import nltk
import pickle

random.seed(123)
np.random.seed(123)

nltk.download('punkt')
nltk.download('stopwords')

def convert_lower_case(data):
    return np.char.lower(data)
def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text
def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data
def remove_apostrophe(data):
    return np.char.replace(data, "'", "")
def stemming(data):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text
def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text
def remove_obvious(data):
    return_data = str(data).replace("book","").replace("self","").replace("help","").replace("author","").replace("peopl","person").replace("bestsel","").replace("reader","")
    return return_data 

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    data = remove_obvious(data)
    return data


filename_model = '../../data/topic_model_tfidf_nmf.pickle'
nmf_model = pickle.load(open(filename_model, 'rb'))
filename_model = '../../data/topic_model_tfidf.pickle'
tfidf_model = pickle.load(open(filename_model, 'rb'))
ols_results = sm.load('../../data/ols.pickle')

st.title('Publish or perish: data-driven choice of book keywords for publishing on Amazon')

main_category = st.selectbox("Select the main category of the book: ", ["",'self-help'])
book_title = st.text_input('Enter the title of the book:')
book_description = st.text_input('Enter the description of the book:')
# book_labels = st.text_input('Enter the labels of the book:')
input_text = book_title +' '+book_description

processed_input_text = preprocess(input_text)


df_coeff_topics = pd.read_csv('../../data/books_25_pages_author_info_description_genres_topics_top_words_ols_coeff.csv')
df_coeff_topics = df_coeff_topics.rename(columns = lambda x: x.strip())

#import models
filename_model = '../../data/topic_model_tfidf_nmf.pickle'
nmf_model = pickle.load(open(filename_model, 'rb'))
filename_model = '../../data/topic_model_tfidf.pickle'
tfidf_model = pickle.load(open(filename_model, 'rb'))

# transform text to features for linear regression
num_topics = 10
X_tfidf = tfidf_model.transform([processed_input_text])
X_nmf = nmf_model.transform(X_tfidf)
df_x_nmf = pd.DataFrame(X_nmf,columns = ['topic_'+str(i) for i in range(0,num_topics)]) 
# convert into useful dataframe
df_x_nmf_tp = df_x_nmf.transpose().reset_index()
df_x_nmf_tp = df_x_nmf_tp.rename(columns={'index':'topic',0:'probability'})
df_x_nmf_tp['topic'] = list(range(0,len(df_x_nmf_tp['topic'].values)))

# df_x_nmf_tp
# probability cutoff for topic model
cutoff_prob = 0.1
topics_list = df_x_nmf_tp[df_x_nmf_tp['probability'] > cutoff_prob]['topic'].values
#words of topics that have probability > cutoff_prob
df_topics_high_prob = df_coeff_topics[df_coeff_topics['topic'].isin(topics_list)]
# output top words
# df_topics_high_prob

conf_level = 0.05
conf_low = df_topics_high_prob[df_topics_high_prob['p-val']<conf_level]['conf_int_low'].values
conf_high = df_topics_high_prob[df_topics_high_prob['p-val']<conf_level]['conf_int_high'].values
words_top = df_topics_high_prob[df_topics_high_prob['p-val']<conf_level]['top_words'].values
# " ".join(words_top.split())

set_out = set(preprocess(" ".join(words_top)).split())
set_in  = set(processed_input_text.split())
set_missing = set_out.difference(set_in)

for i in range(0,len(words_top)):
    'Including the words ('+', '.join(words_top[i].split())+ ') is associated with having between '+str(int(round(conf_low[i],0)))+' and '+str(int(round(conf_high[i],0)))+' more reviews per month.'



if set_missing:
    ### map stems back
    map_stems = {'studi': 'study', 'stori':'story','inspir':'inspire','happi':'happy','posit':'positive','creat':'create','busi':'business','emot':'emotion','advic':'advice','medit':'meditate','famili':'family'}
    keywords_mapped = []
    for stri in set_missing:
        keywords_mapped.append(map_stems.get(stri,stri))
    keywords_missing = ", ".join(keywords_mapped)
    
    'Good news! You already have ' +str(len(set_out)-len(set_missing))+' of these keywords in your book title and description. You have '+str(len(set_missing))+' to go! Add: '+ keywords_missing

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



