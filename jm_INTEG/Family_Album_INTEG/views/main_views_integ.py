from flask import Flask
from flask import Blueprint
import pymysql
from config import DBConfig


bp = Blueprint('main_integ',__name__,url_prefix='/')

# conn = pymysql.connect(host='localhost', user='root', password='1234', db='family_album', charset='utf8')
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

@bp.route('/home')
def hello_woori():

    try:
        # INSERT
        with conn.cursor() as cursor:
            query = """
                SELECT * FROM user_tb
                """
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)

        conn.commit()

        # # SELECT
        # with conn.cursor() as cursor:
        #     query = "select * FROM user_tb"
        #     cursor.execute(query)
        
    finally:
        conn.close()

    return 'Welcome to Woori-Family-Island'
