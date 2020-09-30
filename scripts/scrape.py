import requests
import time
from bs4 import BeautifulSoup as bs
from pathlib import Path
import os 
import pandas as pd
import numpy as np
import re
import random
random.seed(123)
np.random.seed(123)

    #from selenium import webdriver
    #from idlelib.iomenu import encoding
    
    #copy chromedriver into python folder
    # driver = webdriver.Chrome()
    # time.sleep(3)
    # driver.get("https://www.goodreads.com/shelf/show/self-help?page=1")
    # time.sleep(3)
    # soup = bs(driver.page_source,'html.parser')
    
    # soup = bs(open('out1.html',encoding="utf-8"),'html.parser')

def extract_from_html_genre_page():
    data_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    out_csv = []
    for i in range(0,25):
        soup = bs(open(data_path+str(i+1)+'.html',encoding="utf-8"),'html.parser')
        
        titles = soup.find_all('a', class_='bookTitle')
        authors = soup.find_all('a', class_='authorName')
        gray_text = soup.find_all('span',class_='greyText smallText')
        
        if not len(titles) == len(authors) == len(gray_text):
            print('issue')
            
        for i in range(0,len(titles)):
            booktitlei = str(titles[i].string.encode("utf-8")).replace(",",";")[2:-1] # book title
            bookrefi = str(titles[i]['href'].encode("utf-8")).replace(",",";")[2:-1]
            authornamei = str(authors[i].string.encode("utf-8")).replace(",",";")[2:-1]
            ratings_yeari = str(gray_text[i].string).replace('\n','').replace(",","").split()
            avg_ratingi = ratings_yeari[2]
            num_ratingsi = ratings_yeari[4]
            yeari = ratings_yeari[8] if len(ratings_yeari) == 9 else ""

            out_csv.append(booktitlei + "," + bookrefi + "," + authornamei + "," + avg_ratingi + "," +num_ratingsi + "," + yeari)
            
    with open(str(Path(os.getcwd()).parents[0])+"/data/genre_25_pages.csv",'w') as f1:
        f1.write('book_title, book_reference, author_names, avg_rating, num_ratings, year_published \n')
        [f1.write(i+"\n") for i in out_csv]
        
def extract_from_html_author_page():
    data_path = str(Path(os.getcwd()).parents[0])+'/data/'
    df1 = pd.read_csv(data_path+'/books_25_pages.csv',skipinitialspace=True)
    
    authors_set = set(df1['author_link'].values)
    
    html_author_data = {}

    for author_link_i in authors_set:
        if str(author_link_i) == 'nan': continue
        
        author_i = author_link_i.split('.')[-1]
        print(author_i)
        file_path_i = data_path+"/html_files/authors_2020_09_24_no_login/author_"+author_i+'.html'
        
        if not Path(file_path_i).exists():
            print(file_path_i,"does not exist!")
            continue 
        
        soup = bs(open(file_path_i,encoding="utf-8"),'html.parser')
        dict1 = {}        
        try:
            dict1['author_link']=soup.select_one("meta[property='og:url']")['content'].strip()
        except:
            dict1['author_link'] = ""
            print('author_link issue')
        try:
            dict1['author_unique_works'] = get_num_distinct_works(file_path_i)
        except:
            dict1['author_unique_works'] = ""
            print('author_unique_works issue')
#         try:
#             dict1['author_num_posts'] = soup.select_all()
#         except:
#             dict1['author_num_posts'] = ""
#             print('author_num_posts issue')
#         try:
#             dict1['author_num_ratings'] = soup.select_all()
#         except:
#             dict1['author_num_ratings'] = ""
#             print('author_num_ratings issue')
#         try:
#             dict1['author_num_reviews'] = soup.select_all()
#         except:
#             dict1['author_num_reviews'] = ""
#             print('author_num_reviews issue')
#         try:
#             dict1['author_num_books_in_bookshelves'] = soup.select_all()
#         except:
#             dict1['author_num_books_in_bookshelves'] = ""
#             print('author_num_books_in_bookshelves issue')
            
        html_author_data[dict1['author_link']]= dict1['author_unique_works']
    
        
    columns_out = ['author_link', 'author_unique_works']
    
    df1 = pd.read_csv(str(Path(os.getcwd()).parents[0])+'/data/books_25_pages_description.csv',skipinitialspace=True)
    
    df1['author_num_unique_books'] = df1.apply(lambda row: html_author_data.get(row['author_link'],""),axis=1)

    df1.to_csv(str(Path(os.getcwd()).parents[0])+'/data/books_25_pages_author_info_description.csv',index=False)
    

def get_num_distinct_works(author_file_path):
    pattern = re.compile("distinct works")
    for i, line in enumerate(open(author_file_path,encoding='utf-8')):
        for match in re.finditer(pattern, line):
            print(line)
            return(line.split('>')[1].split()[0].replace(",",""))

def extract_from_html_book_page():
    data_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    
    html_book_data = []
    for i in range(0,1249): #1249): #,1249):
        soup = bs(open(data_path+"/books_2020_09_23_no_login/book_"+str(i+1)+'.html',encoding="utf-8"),'html.parser')
        
        td = {}
        
        print(i)
        
        try:
            td['title']=soup.select_one("meta[property='og:title']")['content']
        except:
            td['title'] = ""
            print('title issue')
        try:
            td['isbn']=soup.select_one("meta[property='books:isbn']")['content']
        except:
            td['isbn'] = ""
            print('isbn issue')
        try:
            td['reviewCount'] = soup.find_all(itemprop="reviewCount")[0].text.split()[0].replace(",","")  
        except:
            td['reviewCount'] = ""
            print('reviewCount issue')
        try:
            td['genres'] = soup.find_all(class_='actionLinkLite greyText bookPageGenreLink')
        except:
            td['genres'] = ""
            print('genres issue')
        try:
            td['author'] = soup.select_one("meta[property='books:author']")['content']
        except:
            td['author'] = ""
            print('author issue')
        try:
            td['kindle_price'] = soup.find_all(href="javascript:void(0)")[0].text.split()[-1].replace("$","")
        except:
            td['kindle_price'] = ""
            print('kindle_price issue')
        try:             
            for texti in str(soup.find_all(id="descriptionContainer")[0]).splitlines():
                if "freeText" in texti:
                    td['book_description'] = cleanhtml(texti)
                    if "display:none" in texti:
    #                     td['book_description'] = texti.split("display:none")[1].split("</span>")[0][2::]
                        td['book_description'] = cleanhtml(texti)
            if not td['book_description']:
                td['book_description'] = ""
        except:
            td['book_description'] = ""
            print('description issue')       

        genre_dicti = {}
        for tagi in td['genres']:
            tagi = tagi['title'].split()
            genre_dicti['genre_'+tagi[6][1:-1]] = tagi[0]
        html_book_data.append([td['title'],td['isbn'],td['reviewCount'],td['kindle_price'],td['author'],td['book_description'],genre_dicti])

    indexlast = 6

    ### process genres 
    all_genres = set()
    for booki in html_book_data:
        all_genres = all_genres.union(set(booki[indexlast].keys()))
    all_genres = list(all_genres)
    all_genres.sort()
    
    # process output data to include genres
    out_data = []
    for rowi in html_book_data:
        genres_counti = []
        for keyi in all_genres:
            genres_counti.append(rowi[indexlast].get(keyi,'0'))
        temp_rowi = rowi[0:indexlast]
        temp_rowi.extend(genres_counti)

        out_data.append(temp_rowi)
    
    # create output columns
    columns_out = ['book_title', 'book_isbn', 'book_review_count','kindle_price','author_link','book_description']
    columns_out.extend(all_genres)
    
    df1 = pd.DataFrame(out_data, columns=columns_out)
    df2 = pd.read_csv(str(Path(os.getcwd()).parents[0])+'/data/genre_25_pages.csv',skipinitialspace=True)
    df2 = df2.drop(columns=['book_title'])

    df1 = df2.head(n=len(df1.index)).join(df1)
    df1.to_csv(str(Path(os.getcwd()).parents[0])+'/data/books_25_pages_description.csv',index=False)
    
def write_html_genre(genre):
    out_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    url_base = "https://www.goodreads.com/shelf/show/"+genre+"?page="
    for i in range(0,1):
        print(i)
        pagei = requests.get(url_base+str(i+1))
        time.sleep(5)
        if pagei.status_code != 200:
            print("problem!"+str(i+1))
            quit()
        
        with open(out_path+'/'+str(i+1)+'.html','w',encoding='utf-8') as file:
            file.write(pagei.text)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
            
def write_html_books():
    out_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    data_path = str(Path(os.getcwd()).parents[0])+'/data/genre_25_pages.csv'
    url_base = "https://www.goodreads.com"
    df1 = pd.read_csv(data_path,skipinitialspace=True)
    
    i = 0
    for refi in df1['book_reference'].values:
        print(i,refi)
        refi = refi.strip()
        pagei = requests.get(url_base+refi)
        time.sleep(5)
        if pagei.status_code != 200:
            print("problem!"+str(i+1))
            quit()
        
        with open(out_path+'/book_'+str(i+1)+'.html','w',encoding='utf-8') as file:
            file.write(pagei.text)
            
        i += 1

def write_html_authors():
    out_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/authors_2020_09_24_no_login/'
    data_path = str(Path(os.getcwd()).parents[0])+'/data/books_25_pages.csv'
    df1 = pd.read_csv(data_path,skipinitialspace=True)
    
    authors_set = set(df1['author_link'].values)
    
    i = 0
    for refi in authors_set:
        if str(refi) == 'nan': 
            print(i,refi)
            i += 1
            continue
        refi = refi.strip()
        author_name_i = refi.split(".")[-1]
        pagei = requests.get(refi)
        time.sleep(5)
        if pagei.status_code != 200:
            print("problem!"+str(i,refi))
            i += 1
            continue
        with open(out_path+'/author_'+author_name_i+'.html','w',encoding='utf-8') as file:
            file.write(pagei.text)
            
        print(i,refi)

        i += 1
        
def main():
    # TODO: 
        # use data from various sources
        # add more features like distribution of book ratings, number of books published by author, publisher, date of first review
        # create new features with PCA, t-SNE, k-means...
        extract_from_html_author_page()
    
if __name__ == "__main__":
    main()




