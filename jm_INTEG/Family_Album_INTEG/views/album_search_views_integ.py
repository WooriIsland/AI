from flask import Blueprint,request,jsonify
import pymysql
from config import DBConfig

bp = Blueprint('album_search_integ',__name__,url_prefix='/album_search_integ')

# 가족 앨범 조회
@bp.route('/search',methods=['GET','POST'])
def search_family_album():


    # DB
    conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

    if request.method=='POST':

        island_unique_number = request.get_json()['island_unique_number']
        search_keyword = request.get_json()['search_keyword']
        searched_family_photos = []

        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """SELECT photo_id,photo_image,photo_datetime,photo_latitude,photo_longitude,`character`,summary
                           FROM family_photo_tb
                           WHERE island_unique_number = %s
                           AND (`character` LIKE %s or tags LIKE %s or summary LIKE %s)
                           ORDER BY photo_datetime ASC"""
                cursor.execute(query, (island_unique_number, f'%{search_keyword}%', f'%{search_keyword}%', f'%{search_keyword}%'))
                family_photos_data = cursor.fetchall()
                # print(family_photos_data)
        except Exception as e:
            print("family_photo SELECT(search) Exception! : ",e)
            return 'Exception!' + e 

        # finally:
        #     conn.close()
        
        print(" Searched Family Photos Total Count : ",len(family_photos_data))
        for idx,family_photo_data in enumerate(family_photos_data):
            print(" ----------- ", idx, " ----------")
            data = {}
            data['photo_id'] = family_photo_data[0]
            data['photo_image'] = family_photo_data[1]
            # print("photo_datetime : ",str(family_photo_data[1]))
            data['photo_datetime'] = str(family_photo_data[2])
            # print("photo_latitude : ",float(family_photo_data[2]))
            data['photo_latitude'] = float(family_photo_data[3])
            # print("photo_longitude : ",float(family_photo_data[3]))
            data['photo_longitude'] = float(family_photo_data[4])
            # print("character : ",eval(family_photo_data[4]))
            # print("character : ",type(eval((family_photo_data[4]))))
            data['character'] = eval(family_photo_data[5])     
            # print("summary : ",type(family_photo_data[5]))
            data['summary'] = family_photo_data[6]     
            
            print(data)

            searched_family_photos.append(data)

        res_json = {'data': searched_family_photos}

        return jsonify(res_json)
    
    elif request.method=='GET':

        return 'Complete Album Inquiry (GET)'