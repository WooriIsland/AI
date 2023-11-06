from flask import Blueprint,request,jsonify
import pickle
import pymysql
from config import DBConfig

bp = Blueprint('album_inquiry_integ',__name__,url_prefix='/album_inquiry_integ')

# 가족 앨범 조회
@bp.route('/inquiry',methods=['GET','POST'])
def inquiry_family_album():

    # DB
    conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

    # with open(save_root_db+'album_registration_db.pickle', 'rb') as f:
    #     album_registration_db = pickle.load(f)

    if request.method=='POST':

        island_unique_number = request.get_json()['island_unique_number']
        family_photos = []

        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """SELECT photo_id,photo_image,photo_datetime,photo_location,`character`,summary
                           FROM family_photo_tb
                           WHERE island_unique_number = %s
                           ORDER BY photo_datetime ASC"""
                cursor.execute(query,(island_unique_number,))
                family_photos_data = cursor.fetchall()
                # print(family_photos_data)
        except Exception as e:
            print("user_tb SELECT Exception! : ",e)
            return 'Exception!' + e 
        
        # finally:
        #     conn.close()
        
        print(" Family Photos Total Count : ",len(family_photos_data))
        for idx,family_photo_data in enumerate(family_photos_data):
            print(" ----------- ", idx, " ----------")
            data = {}
            data['photo_id'] = family_photo_data[0]
            data['photo_image'] = family_photo_data[1]
            # print("photo_datetime : ",str(family_photo_data[1]))
            data['photo_datetime'] = str(family_photo_data[2])

            data['photo_location'] = str(family_photo_data[3])

            # print("photo_latitude : ",float(family_photo_data[2]))
            # data['photo_latitude'] = float(family_photo_data[3])
            # print("photo_longitude : ",float(family_photo_data[3]))
            # data['photo_longitude'] = float(family_photo_data[4])

            # print("character : ",eval(family_photo_data[4]))
            # print("character : ",type(eval((family_photo_data[4]))))
            data['character'] = eval(family_photo_data[4])     
            # print("summary : ",type(family_photo_data[5]))
            data['summary'] = family_photo_data[5]     
            
            print(data)

            family_photos.append(data)

        res_json = {'data': family_photos}

        return jsonify(res_json)
    
    elif request.method=='GET':

        return 'Complete Album Inquiry (GET)'