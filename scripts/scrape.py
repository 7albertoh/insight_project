import requests
import time
from bs4 import BeautifulSoup as bs
from pathlib import Path
import os 
import pandas as pd

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

def extract_from_html_book_page():
    data_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    
    html_book_data = []
    for i in range(0,1249):
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
            td['kindle_price'] = soup.find_all(href="javascript:void(0)")[0].text.split()[-1].replace("$","")
        except:
            td['kindle_price'] = ""
            print('kindle_price issue')
            
        genre_dicti = {}
        for tagi in td['genres']:
            tagi = tagi['title'].split()
            genre_dicti['genre_'+tagi[6][1:-1]] = tagi[0]
        
        html_book_data.append([td['title'],td['isbn'],td['reviewCount'],td['kindle_price'],genre_dicti])

    ### process genres 
    all_genres = set()
    for booki in html_book_data:
        all_genres = all_genres.union(set(booki[4].keys()))
    all_genres = list(all_genres)
    all_genres.sort()

    # process output data to include genres
    out_data = []
    for rowi in html_book_data:
        genres_counti = []
        for keyi in all_genres:
            genres_counti.append(rowi[4].get(keyi,'0'))
        temp_rowi = rowi[0:4]
        temp_rowi.extend(genres_counti)

        out_data.append(temp_rowi)
    
    # create output columns
    columns_out = ['book_title', 'book_isbn', 'book_review_count','kindle_price']
    columns_out.extend(all_genres)
    
    df1 = pd.DataFrame(out_data, columns=columns_out)
    df2 = pd.read_csv(str(Path(os.getcwd()).parents[0])+'/data/genre_25_pages.csv',skipinitialspace=True)
    df2 = df2.drop(columns=['book_title'])

    df1 = df2.head(n=len(df1.index)).join(df1)
    df1.to_csv(str(Path(os.getcwd()).parents[0])+'/data/books_25_pages.csv',index=False)
    
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
        
def main():
    # TODO: add more features like distribution of ratings, number of books published by author, publisher, date of first review
    extract_from_html_book_page()

if __name__ == "__main__":
    main()




