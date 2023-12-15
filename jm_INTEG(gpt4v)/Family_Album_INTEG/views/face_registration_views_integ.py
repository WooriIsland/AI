from flask import Blueprint,request
from flask import jsonify
from Family_Album_INTEG.models.face_recognition import face_recognition
import pymysql
from config import DBConfig
# import base64
# import boto3
import json
from Family_Album_INTEG.cloud.s3 import S3
import random

bp = Blueprint('face_registration_integ',__name__,url_prefix='/face_registration_integ')

# DB
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)
# Local Save Root
save_root_indivisuals = 'data(Family_Album)/face_registration/indivisuals/'

# AWS
with open('resource/secret.json', 'r') as json_file:
    data = json.load(json_file)

region_name = data['region_name']
aws_access_key_id = data['aws_access_key_id']
aws_secret_access_key = data['aws_secret_access_key']
bucket = data['bucket']
bucket_dir = 'Family_Album_Bucket_Folder/'
face_data_dir = 'face_data/'

s3 = S3.connection(region_name,aws_access_key_id,aws_secret_access_key)

# 가족 구성원별 이미지 데이터 받기/안면 데이터 저장
# ex) 어머니-이미지, 아버지-이미지, 딸-이미지...  
@bp.route('/upload_data',methods=['GET','POST'])
def get_face_img():
    
    if request.method=='POST':

            # 0에서 9 사이의 난수 10개 생성하고 문자열로 변환
        random_numbers = [str(random.randint(0, 9)) for _ in range(10)]
        random_string = ''.join(random_numbers)

        print("체크 request.form : ", request.form)

        island_unique_number = request.form['island_unique_number'] # '1111'
        print("체크 island_unique_number : ", island_unique_number)
        print("체크 Type :",type(island_unique_number))
        # island_unique_number = int(island_unique_number)

        user_id = request.form['user_id'] # '1','2','3'...
        print("체크 user_id : ", user_id)
        print("체크 Type :",type(user_id))

        user_nickname = request.form['user_nickname'] # 'daddy123'
        print("체크 user_nickname : ", user_nickname)
        print("체크 Type :",type(user_nickname))

        # requerst.files로 안들어오면 안받아진 것임
        print("체크 request.files : ", request.files)
        face_image = request.files['face_image']
        file_name = face_image.filename.lower()
        # 확장자로 .png 확장자 거를 수도 있음
        print("체크 f : ",face_image)
        print("체크 f.filename : ", face_image.filename)
        print("체크 Type :",type(face_image))
        # facial_image = base64.b64encode(facial_image.read()).decode('utf-8')
        # print("체크 facial_image_base64 : ",facial_image)

        ####################
        #Save Image to Local
        #################### 
        save_name = save_root_indivisuals+island_unique_number+'_'+user_id+'_'+user_nickname+'.jpg'
        print(save_name)
        face_image.save(save_name)

        img = face_recognition.load_image_file(face_image)
        face_encoding = face_recognition.face_encodings(img)[0]
        # print("encoding : " ,encoding)

        face_encoding = str(face_encoding.tolist())

        # base64 Encoding
        # face_image = base64.b64encode(face_image.read()).decode('utf-8')
        # print("file_name.split()[0]",file_name.split(".")[0])
        # S3
        print("bucket_dir+file_name : ",bucket_dir+face_data_dir+random_string+'_'+file_name)
        put_object_result = S3.put_object(s3,bucket,save_name,bucket_dir+face_data_dir+random_string+'_'+file_name) # Save
        print("Save Face Data to S3 : ",put_object_result)
        face_image_url = S3.get_image_url(s3,bucket,bucket_dir+face_data_dir+random_string+'_'+file_name)
        print("Face Image URL : ",face_image_url)

        try:
            # INSERT
            with conn.cursor() as cursor:

                # print("user_id type ******", type(user_id))
                
                query = """INSERT INTO user_tb (user_id,island_unique_number) 
                            VALUES (%s,%s)"""
                cursor.execute(query,(user_id,island_unique_number))

                # print("INSERT user_tb Complete*********************************************")
                query = """INSERT INTO facial_data_tb (user_id,user_nickname,face_encoding,face_image) 
                            VALUES (%s,%s,%s,%s)"""
                cursor.execute(query,(user_id,user_nickname,face_encoding,face_image_url))
                
                # data = cursor.fetchall()
                # print(data)

            conn.commit()
    
        except Exception as e:
            print("user_tb INSERT Exception ! :",e)
            print("facial_data_tb INSERT Exception ! :",e)
            return 'Exception!' + e
        
        # finally:
        #     conn.close()

        print('Complete Face Registration (POST)')
        
        # Unity에 안면 데이터 저장 완료 응답
        res_json = {
                        'data':
                                {
                                    'island_unique_number' : island_unique_number,
                                    'user_id' : user_id,
                                    'user_nickname' : user_nickname,
                                    'message' : '얼굴 등록 완료!',
                                    'description' : 'Complete Register Facial data'
                                }
                    }
        return jsonify(res_json)

    elif request.method=='GET':
        
        return 'Complete Face Registration (GET)'