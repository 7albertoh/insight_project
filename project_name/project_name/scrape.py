import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from idlelib.iomenu import encoding

#copy chromedriver into python folder
driver = webdriver.Chrome()
time.sleep(3)
driver.get("https://www.goodreads.com/shelf/show/self-help?page=2")
time.sleep(3)
soup = bs(driver.page_source,'html.parser')
# 
# soup = bs(open('out1.html',encoding="utf-8"),'html.parser')
# titles = soup.find_all('a', class_='bookTitle')
# authors = soup.find_all('a', class_='authorName')
# gray_text = soup.find_all('span',class_='greyText smallText')
# if not len(titles) == len(authors) == len(gray_text):
#     print('issue')
# 
# out_csv = []
# for i in range(0,len(titles)):
#     booktitlei = str(titles[i].string.encode("utf-8")).replace(",",";") # book title
#     bookrefi = str(titles[i]['href'].encode("utf-8")).replace(",",";")
#     authornamei = str(authors[i].string.encode("utf-8")).replace(",",";")
#     numreviewsi = str(gray_text[i].string.encode("utf-8")).replace(",","")
#     out_csv.append(booktitlei + ", " + bookrefi + ", " + authornamei + ", " + numreviewsi)
# 
# with open("out.csv",'w') as f1:
#     f1.write('book_title, book_reference, author_names, avg_rating_num_ratings_year_published \n')
#     [f1.write(i+"\n") for i in out_csv]

# with open('out1.html','w',encoding='utf-8') as file:
#     file.write(str(soup))
    








# with open('self-help' + '.csv', 'w') as csvfile:
#     fieldnames = ['title', 'author']
#     csv_write = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     books_save = 0
# 
#     for title, author in zip(titles, authors):
# 
#         try:
#             ## single book page
#             book_page = requests.get("https://www.goodreads.com" + title['href'])
#             soup = bs(book_page.content, 'html.parser')
#             # get image id
#             image = soup.find('img', id='coverImage')
# 
#             title_name = title.get_text()
# 
#             save_dir = image_dir + "/" + title_name
#             urllib.request.urlretrieve(image['src'], save_dir)
# 
#             csv_write.writerow({'title': title_name, 'author': author.get_text()})
#             books_save += 1
#             ## error handelling for long file names
#         except OSError as exc:
#             if exc.errno == 36:
#                 print(exc)