import mysql.connector

def connect():
    my_db = mysql.connector.connect(
        user='root',
        password='199811563',
        host='127.0.0.1',
        database='flip_news'



    )
    return my_db

