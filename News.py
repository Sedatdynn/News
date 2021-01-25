import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import json
from dbconnection import connect
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class TechNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.base_url = "https://flipboard.com/section/teknoloji-a0isdrb4bs8bb7n1"
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe",options=options)
        #elf.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
        self.browser.get(self.base_url)
        time.sleep(3)

        self.db = connect()


        i = 500

        try:
            self.browser.switch_to.frame(self.browser.find_element_by_id("sp_message_iframe_398445"))
            time.sleep(1)
            self.browser.find_element_by_xpath("/html/body/div/div[3]/div[3]/div[2]/button").click()
            self.browser.switch_to.default_content()

        except: pass

        while i <= 1500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(2)
            i += 700

        time.sleep(1)

        self.html_data = self.browser.page_source
        self.browser.quit()


        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.PostsDate = False
        self.CurrentDate = False
        self.SourceLink = False
        self.current_doc = []
        self.scrapped_datas = []

        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        #with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
        with open(r"Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        print("Veriler belirleniyor.")

        soup = BeautifulSoup(self.html_data, 'html.parser')
        datas = soup.find("ul",class_ ="item-list item-list--grid")
        for data in datas:
            links = data.h1.a

            self.VeriCek("https://flipboard.com" + links['href'])


        if len(self.scrapped_datas) >= 1:
            self.save(self.scrapped_datas)

    def VeriCek(self, url):
        print("Veriler Çekiliyor")
        try:
            page = requests.get(url, headers=self.user_id, verify=False)
            source = page.content
            soup = BeautifulSoup(source, 'html.parser')

            data = soup.find("div", class_="post post--card post--article-view")
            self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']



            if self.SourceLink in self.current_doc:
                print("Veriler json dosyasında  mevcut!")
            else:
                self.NewsTitle = data.find("h1",class_ ="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p",class_="post__excerpt").text
                self.SourceWebSite = data.find('a', class_='post-attribution__author internal-link').text
                self.SourceLink = data.find('a',class_='button--base button--secondary outbound-link')['href']
                self.PostsDate = data.find('time', class_='post-attribution__time').text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.SourceLink,
                    'News Category': 'Teknoloji',
                }

                self.scrapped_datas.append(my_data)

        except: pass


    def save(self, data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)

        for i in data:
            js_file["TechNews"].append(i)

        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)

        print("Veriler json dosyasına eklendi.")
        self.save_to_db()

    def save_to_db(self):
        with open(r'Technews.json', 'r', encoding='utf-8') as file:
            to_db = json.load(file)


        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        db_datas = []
        row = cursor.fetchall()
        for item in row:
            db_datas.append(item[1])

        for i in to_db['TechNews']:
            if i['News Title'] in db_datas:
                print("bu veri veri tabanında mevcut.")
            else:
                insert_data = (
                    "INSERT INTO all_news(NewsTitle, NewsContent, NewsSource, NewsLink, NewsDate, NewsRegisDate, NewsCategory)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                js_datas = (f'{i["News Title"]}', i['News Content'], i['News Source'], i['News Link'], i['News Date'], i['Current Date'],i['News Category'])

                cursor.execute(insert_data, js_datas)

                self.db.commit()

        self.db.close()
        print("Veriler veri tabanına aktarıldı.")


class SportNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.base_url ="https://flipboard.com/section/spor-d7ilibva0mpg02ec"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe",options=options)
        #self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        try:
            self.browser.switch_to.frame(self.browser.find_element_by_id("sp_message_iframe_398445"))
            time.sleep(1)
            self.browser.find_element_by_xpath("/html/body/div/div[3]/div[3]/div[2]/button").click()
            self.browser.switch_to.default_content()

        except: pass

        i = 500
        while i <= 1500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.db = connect()
        self.html_data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []
        self.scrapped_datas = []
        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        #with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
        with open(r"Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        print("Veriler belirleniyor.")
        soup = BeautifulSoup(self.html_data, 'html.parser')
        datas = soup.find("ul",class_ ="item-list item-list--grid")
        for data in datas:
            links = data.h1.a

            self.VeriCek("https://flipboard.com" + links['href'])


        if len(self.scrapped_datas) >= 1:
            self.save(self.scrapped_datas)

    def VeriCek(self, url):
        print("Veriler çekiliyor.")
        try:
            page = requests.get(url, headers=self.user_id, verify=False)
            source = page.content
            soup = BeautifulSoup(source, 'html.parser')

            data = soup.find("div", class_="post post--card post--article-view")
            self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
            if self.SourceLink in self.current_doc:
                print("Veriler json dosyasında  mevcut!")
            else:
                self.NewsTitle = data.find("h1", class_="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p", class_="post__excerpt").text
                self.SourceWebSite = data.find('a', class_='post-attribution__author internal-link').text
                self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
                self.PostsDate = data.find('time', class_='post-attribution__time').text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.SourceLink,
                    'News Category': 'Spor',
                }

                self.scrapped_datas.append(my_data)

        except:
            time.sleep(3); pass

    def save(self,data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data:js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)

        print("Veriler json dosyasına eklendi.")
        self.save_to_db()

    def save_to_db(self):
        with open(r'Technews.json', 'r', encoding='utf-8') as file:
            to_db = json.load(file)


        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        db_datas = []
        row = cursor.fetchall()
        for item in row:
            db_datas.append(item[1])

        for i in to_db['TechNews']:
            if i['News Title'] in db_datas:
                print("bu veri veri tabanında mevcut.")
            else:
                insert_data = (
                    "INSERT INTO all_news(NewsTitle, NewsContent, NewsSource, NewsLink, NewsDate, NewsRegisDate, NewsCategory)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                js_datas = (f'{i["News Title"]}', i['News Content'], i['News Source'], i['News Link'], i['News Date'], i['Current Date'],i['News Category'])

                cursor.execute(insert_data, js_datas)

                self.db.commit()

        self.db.close()
        print("Veriler veri tabanına aktarıldı.")

class EcoNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.base_url = "https://flipboard.com/section/ekonomi-2j5aogjl2t55j3ss"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe", options=options)
        # self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        try:
            self.browser.switch_to.frame(self.browser.find_element_by_id("sp_message_iframe_398445"))
            time.sleep(1)
            self.browser.find_element_by_xpath("/html/body/div/div[3]/div[3]/div[2]/button").click()
            self.browser.switch_to.default_content()

        except:
            pass

        i = 500
        while i <= 1500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.db = connect()
        self.html_data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []
        self.scrapped_datas = []
        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        #with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
        with open(r"Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        print("Veriler belirleniyor.")

        soup = BeautifulSoup(self.html_data, 'html.parser')
        datas = soup.find("ul",class_ ="item-list item-list--grid")
        for data in datas:
            links = data.h1.a

            self.VeriCek("https://flipboard.com" + links['href'])


        if len(self.scrapped_datas) >= 1:
            self.save(self.scrapped_datas)

    def VeriCek(self, url):
        print("Veriler Çekiliyor")

        try:
            page = requests.get(url, headers=self.user_id, verify=False)
            source = page.content
            soup = BeautifulSoup(source, 'html.parser')

            data = soup.find("div", class_="post post--card post--article-view")
            self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
            if self.SourceLink in self.current_doc:
                print("Veriler json dosyasında  mevcut!")
            else:
                self.NewsTitle = data.find("h1", class_="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p", class_="post__excerpt").text
                self.SourceWebSite = data.find('a', class_='post-attribution__author internal-link').text
                self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
                self.PostsDate = data.find('time', class_='post-attribution__time').text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.SourceLink,
                    'News Category': 'Ekonomi',
                }

                self.scrapped_datas.append(my_data)

        except:
            time.sleep(3); pass

    def save(self, data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data: js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)

        print("Veriler json dosyasına eklendi.")
        self.save_to_db()

    def save_to_db(self):
        with open(r'Technews.json', 'r', encoding='utf-8') as file:
            to_db = json.load(file)

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        db_datas = []
        row = cursor.fetchall()
        for item in row:
            db_datas.append(item[1])

        for i in to_db['TechNews']:
            if i['News Title'] in db_datas:
                print("bu veri veri tabanında mevcut.")
            else:
                insert_data = (
                    "INSERT INTO all_news(NewsTitle, NewsContent, NewsSource, NewsLink, NewsDate, NewsRegisDate, NewsCategory)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                js_datas = (f'{i["News Title"]}', i['News Content'], i['News Source'], i['News Link'], i['News Date'],
                            i['Current Date'], i['News Category'])

                cursor.execute(insert_data, js_datas)

                self.db.commit()

        self.db.close()
        print("Veriler veri tabanına aktarıldı.")


class HealthNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.base_url = "https://flipboard.com/section/sa-l-k-q9p4fs08v5kbhg6g"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe", options=options)
        # self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        try:
            self.browser.switch_to.frame(self.browser.find_element_by_id("sp_message_iframe_398445"))
            time.sleep(1)
            self.browser.find_element_by_xpath("/html/body/div/div[3]/div[3]/div[2]/button").click()
            self.browser.switch_to.default_content()

        except:
            pass

        i = 500
        while i <= 1500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.db = connect()
        self.html_data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []
        self.scrapped_datas = []
        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        #with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
        with open(r"Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        print("Veriler belirleniyor.")

        soup = BeautifulSoup(self.html_data, 'html.parser')
        datas = soup.find("ul",class_ ="item-list item-list--grid")
        for data in datas:
            links = data.h1.a

            self.VeriCek("https://flipboard.com" + links['href'])


        if len(self.scrapped_datas) >= 1:
            self.save(self.scrapped_datas)

    def VeriCek(self, url):
        print("Veriler Çekiliyor")

        try:
            page = requests.get(url, headers=self.user_id, verify=False)
            source = page.content
            soup = BeautifulSoup(source, 'html.parser')

            data = soup.find("div", class_="post post--card post--article-view")
            self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
            if self.SourceLink in self.current_doc:
                print("Veriler json dosyasında  mevcut!")
            else:
                self.NewsTitle = data.find("h1", class_="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p", class_="post__excerpt").text
                self.SourceWebSite = data.find('a', class_='post-attribution__author internal-link').text
                self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
                self.PostsDate = data.find('time', class_='post-attribution__time').text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.SourceLink,
                    'News Category': 'Sağlık',
                }

                self.scrapped_datas.append(my_data)

        except:
            time.sleep(3); pass

    def save(self, data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data: js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)

        print("Veriler json dosyasına eklendi.")
        self.save_to_db()

    def save_to_db(self):
        with open(r'Technews.json', 'r', encoding='utf-8') as file:
            to_db = json.load(file)

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        db_datas = []
        row = cursor.fetchall()
        for item in row:
            db_datas.append(item[1])

        for i in to_db['TechNews']:
            if i['News Title'] in db_datas:
                print("bu veri veri tabanında mevcut.")
            else:
                insert_data = (
                    "INSERT INTO all_news(NewsTitle, NewsContent, NewsSource, NewsLink, NewsDate, NewsRegisDate, NewsCategory)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                js_datas = (f'{i["News Title"]}', i['News Content'], i['News Source'], i['News Link'], i['News Date'],
                            i['Current Date'], i['News Category'])

                cursor.execute(insert_data, js_datas)

                self.db.commit()

        self.db.close()
        print("Veriler veri tabanına aktarıldı.")




class GameNews:
    def __init__(self):
        self.user_id = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        self.base_url = "https://flipboard.com/@gamercomtr"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Desktop\chromedriver.exe", options=options)
        # self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
        self.browser.get(self.base_url)
        time.sleep(2)

        try:
            self.browser.switch_to.frame(self.browser.find_element_by_id("sp_message_iframe_398445"))
            time.sleep(1)
            self.browser.find_element_by_xpath("/html/body/div/div[3]/div[3]/div[2]/button").click()
            self.browser.switch_to.default_content()

        except:
            pass

        i = 500
        while i <= 1500:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(3)
            i += 500

        time.sleep(1)

        self.db = connect()
        self.html_data = self.browser.page_source
        self.browser.quit()
        self.NewsTitle = False
        self.NewsShortContent = False
        self.SourceWebSite = False
        self.NewsAvatar = False
        self.NewsLink = False
        self.PostsDate = False
        self.CurrentDate = False
        self.current_doc = []
        self.scrapped_datas = []
        self.my_json = {
            "TechNews": []
        }

        self.count = 0
        #with open(r"C:\Users\ASUS\Technews.json", "r", encoding="utf-8") as file:
        with open(r"Technews.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data["TechNews"]:
            try:
                self.current_doc.append(item["News Link"])
            except:
                pass

    def VeriBelirle(self):
        print("Veriler belirleniyor.")

        soup = BeautifulSoup(self.html_data, 'html.parser')
        datas = soup.find("ul",class_ ="item-list item-list--grid")
        for data in datas:
            links = data.h1.a

            self.VeriCek("https://flipboard.com" + links['href'])


        if len(self.scrapped_datas) >= 1:
            self.save(self.scrapped_datas)

    def VeriCek(self, url):
        print("Veriler Çekiliyor")

        try:
            page = requests.get(url, headers=self.user_id, verify=False)
            source = page.content
            soup = BeautifulSoup(source, 'html.parser')

            data = soup.find("div", class_="post post--card post--article-view")
            self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
            if self.SourceLink in self.current_doc:
                print("Veriler json dosyasında  mevcut!")
            else:
                self.NewsTitle = data.find("h1", class_="post__title article-text--title--large").text
                self.NewsShortContent = data.find("p", class_="post__excerpt").text
                self.SourceWebSite = data.find('a', class_='post-attribution__author internal-link').text
                self.SourceLink = data.find('a', class_='button--base button--secondary outbound-link')['href']
                self.PostsDate = data.find('time', class_='post-attribution__time').text
                self.CurrentDate = datetime.now()

                my_data = {
                    "Current Date": str(self.CurrentDate),
                    'News Date': self.PostsDate,
                    'News Title': self.NewsTitle,
                    'News Content': self.NewsShortContent,
                    'News Source': self.SourceWebSite,
                    'News Link': self.SourceLink,
                    'News Category': 'Oyun',
                }

                self.scrapped_datas.append(my_data)

        except:
            time.sleep(3); pass

    def save(self, data):
        with open("Technews.json", "r", encoding="utf-8") as file:
            js_file = json.load(file)
        for i in data: js_file["TechNews"].append(i)
        with open("Technews.json", "w", encoding="utf-8") as file2:
            json.dump(js_file, file2, indent=2, ensure_ascii=False)

        print("Veriler json dosyasına eklendi.")
        self.save_to_db()

    def save_to_db(self):
        with open(r'Technews.json', 'r', encoding='utf-8') as file:
            to_db = json.load(file)

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        db_datas = []
        row = cursor.fetchall()
        for item in row:
            db_datas.append(item[1])

        for i in to_db['TechNews']:
            if i['News Title'] in db_datas:
                print("bu veri veri tabanında mevcut.")
            else:
                insert_data = (
                    "INSERT INTO all_news(NewsTitle, NewsContent, NewsSource, NewsLink, NewsDate, NewsRegisDate, NewsCategory)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                js_datas = (f'{i["News Title"]}', i['News Content'], i['News Source'], i['News Link'], i['News Date'],
                            i['Current Date'], i['News Category'])

                cursor.execute(insert_data, js_datas)

                self.db.commit()

        self.db.close()
        print("Veriler veri tabanına aktarıldı.")





b = GameNews()
b.VeriBelirle()

