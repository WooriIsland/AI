from flask import Blueprint,request,jsonify
import pymysql
from config import DBConfig

bp = Blueprint('album_delete_integ',__name__,url_prefix='/album_delete_integ')


# DB
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

# 가족 앨범 수정
@bp.route('/delete',methods=['GET','POST'])
def delete_family_album():

    if request.method=='POST':

        photo_id = request.get_json()['photo_id']
        island_unique_number = request.get_json()['island_unique_number']

        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """DELETE FROM family_photo_tb
                           WHERE photo_id = %s and island_unique_number = %s"""
                cursor.execute(query,(photo_id,island_unique_number))
                # family_photos_data = cursor.fetchall()
                # print(family_photos_data)
            conn.commit()

        except Exception as e:
            print("family_photo_tb DELETE Exception! : ",e)
            return 'Exception!' + e
         
        # finally:
        #     conn.close()
        
        res_json={
                    'data' : {
                                'photo_id' : photo_id,
                                'island_unique_number' : island_unique_number,
                                'message':'사진 삭제 완료!',
                                'description':'Complete Delete Family data'
                            }
                }

        return jsonify(res_json)
    
    elif request.method=='GET':

        return 'Complete Album Delete (GET)'