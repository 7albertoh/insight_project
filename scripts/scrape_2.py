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

def extract_from_html():
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

     
def write_html():
    out_path = str(Path(os.getcwd()).parents[0])+'/data/html_files/'
    url_base = "https://www.goodreads.com/shelf/show/self-help?page="
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
    write_html_books()

if __name__ == "__main__":
    main()




