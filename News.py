import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import json

class TechNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.base_url = "https://flipboard.com/section/teknoloji-a0isdrb4bs8bb7n1"
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe",options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        i = 500
        while i <= 2500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []

        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        liste = []
        print("Veriler belirleniyor.")
        page = requests.get(self.base_url, headers=self.user_id)
        source = page.content
        soup = BeautifulSoup(source, 'html.parser')
        datas = soup.find("ul",class_ ="item-list")
        for data in datas:
            links = data.h1.a
            self.NewsLink = "https://flipboard.com" + links['href']
            if self.NewsLink in self.current_doc:
                print("Veriler zaten mevcut!")
            else:
                self.NewsTitle = data.find("h1",class_ ="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p",class_="post__excerpt").text
                self.SourceWebSite = data.div.address.a.text
                self.PostsDate = data.div.time.text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.NewsLink,
                }

                liste.append(my_data)
        if len(liste) >= 1:
            self.save(liste)
        else:
            pass

    def save(self, data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data:
            js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)



class SportNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.base_url ="https://flipboard.com/section/spor-d7ilibva0mpg02ec"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe",options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        i = 500
        while i <= 2500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []

        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass


    def VeriBelirle(self):
        liste = []
        print("Veriler belirleniyor.")
        page = requests.get(self.base_url, headers=self.user_id)
        source = page.content
        soup = BeautifulSoup(source, 'html.parser')
        datas = soup.find("ul", class_="item-list")
        for data in datas:
            links = data.h1.a
            self.NewsLink = "https://flipboard.com" + links['href']
            if self.NewsLink in self.current_doc:
                print("Veriler zaten mevcut!")
            else:

                self.NewsTitle = data.find("h1", class_="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p", class_="post__excerpt").text
                self.SourceWebSite = data.div.address.a.text
                self.PostsDate = data.div.time.text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.NewsLink,
                }

                liste.append(my_data)
            #self.my_json["TechNews"].append(my_data)
        if len(liste) >= 1:
            self.save(liste)
        else:
            pass
    def save(self,data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data:
            js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)




b = TechNews()
b.VeriBelirle()
a = SportNews()
a.VeriBelirle()