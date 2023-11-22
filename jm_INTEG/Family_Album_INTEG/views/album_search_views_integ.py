from flask import Blueprint,request,jsonify
import pymysql
from config import DBConfig
import re

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
                query = """SELECT photo_id,photo_image,photo_datetime,photo_location,`character`,summary
                           FROM family_photo_tb
                           WHERE island_unique_number = %s
                           AND (`character` LIKE %s or tags LIKE %s or summary LIKE %s or summary_strip LIKE %s or photo_location LIKE %s)
                           ORDER BY photo_datetime ASC"""
                cursor.execute(query, (island_unique_number, f'%{search_keyword}%', f'%{search_keyword}%', f'%{search_keyword}%', f'%{search_keyword}%', f'%{search_keyword}%'))
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
            data['photo_datetime'] = str(family_photo_data[2]).split(" ")[0]

            photo_location = str(family_photo_data[3])

            print("photo_location : ",photo_location)

            if photo_location!='경기도 수지구':
                photo_location_list = str(photo_location).replace(" ","").split(",")
                if photo_location_list[-1]=='대한민국':
                    get_gu = False
                    for location in photo_location_list[::-1]:
                        if location[-1]=='구':
                            photo_location =  location + " "
                            get_gu = True
                            continue
                        if get_gu:
                            photo_location += location
                            break

                #############################
                ### 11_22 foreign address ###
                #############################

                # else:
                #     registration_photo_location_list = str(photo_location).replace(" ","").split(",")
                #     registration_photo_location = registration_photo_location_list[-1] + " " + registration_photo_location_list[0]

                else:
                    registration_photo_location_list = str(photo_location).replace(" ","").split(",")

                    korean_strings = []
                    for x in registration_photo_location_list:
                        # 정규표현식을 사용하여 한글 문자열 추출
                        korean_match = re.search('[가-힣]+', x)

                        if korean_match:
                            korean_strings.append(korean_match.group())
                    
                    if korean_strings[0] != korean_strings[-1]:
                        photo_location = korean_strings[-1] + " " + korean_strings[0]
                    else:
                        photo_location = korean_strings[-1]
            
            data['photo_location'] = photo_location
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

            searched_family_photos.append(data)

        res_json = {'data': searched_family_photos}

        return jsonify(res_json)
    
    elif request.method=='GET':

        return 'Complete Album Inquiry (GET)'