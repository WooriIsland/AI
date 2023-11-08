from flask import Blueprint,request,jsonify
import pymysql
from config import DBConfig

bp = Blueprint('album_update_integ',__name__,url_prefix='/album_update_integ')


# DB
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

# 가족 앨범 수정
@bp.route('/update',methods=['GET','POST'])
def update_family_album():

    if request.method=='POST':

        photo_id = request.get_json()['photo_id']
        island_unique_number = request.get_json()['island_unique_number']
        new_summary = request.get_json()['new_summary']

        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """UPDATE family_photo_tb
                           SET summary = %s
                           WHERE photo_id = %s and island_unique_number = %s"""
                cursor.execute(query,(new_summary,photo_id,island_unique_number))
                # family_photos_data = cursor.fetchall()
                # print(family_photos_data)
            conn.commit()

        except Exception as e:
            print("family_photo_tb UPADTE Exception! : ",e)
            return 'Exception!' + e 
        
        # finally:
        #     conn.close()


        res_json={
                    'data' : {
                                'photo_id' : photo_id,
                                'island_unique_number' : island_unique_number,
                                'message':'사진 수정 완료!',
                                'description':'Complete Update Family data'
                            }
                }


        return jsonify(res_json)
    
    elif request.method=='GET':

        return 'Complete Album Update (GET)'