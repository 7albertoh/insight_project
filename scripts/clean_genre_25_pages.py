import time
from pathlib import Path
import os 


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
    
def main():
    extract_from_html()

if __name__ == "__main__":
    main()




