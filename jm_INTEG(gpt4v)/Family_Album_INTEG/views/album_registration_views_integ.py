from flask import Blueprint,request,jsonify
# import base64
from Family_Album_INTEG.models.images_analysis.image_processor import Image_Processor
from PIL import Image
import re
# import googletrans
import pymysql
from config import DBConfig
import datetime
import numpy as np
import json
from Family_Album_INTEG.cloud.s3 import S3
import random
import copy

bp = Blueprint('album_registration_integ',__name__,url_prefix='/album_registration_integ')

# DB
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

# 1. 메타데이터 추출 - Python 코드
# 2. 인물 추출 - Face Recognition
# 3. 배경/물체 추출 - LLaVa
# 4. 요약 문장 생성 - LLaVa

 # 이미지 분석 객체
image_processor = Image_Processor()

#####################
# Model Loading (Ver2)
#####################
# tokenizer, model, llava_image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug = image_processor.load_llava_model()
parser , prompt , chat_model = image_processor.load_gpt4v_model()

# 번역 객체
# translator = googletrans.Translator()
# Local Save Root
save_root_family = 'data(Family_Album)/family/'

# AWS
with open('resource/secret.json', 'r') as json_file:
    data = json.load(json_file)

region_name = data['region_name']
aws_access_key_id = data['aws_access_key_id']
aws_secret_access_key = data['aws_secret_access_key']
bucket = data['bucket']
bucket_dir = 'Family_Album_Bucket_Folder/'
family_photo_dir = 'family_photo/'

s3 = S3.connection(region_name,aws_access_key_id,aws_secret_access_key)

@bp.route('/images_analysis',methods=['GET','POST'])
def images_preprocessing():

    if request.method=='POST':

        user_id = request.form['user_id'] # 2
        # print(island_unique_number)
        # print(type(island_unique_number))
        photo_images = request.files.getlist("photo_image")
        face_encoding_dict = {} # key = nickname, value = np.array[,,,]
        all_family_photo_data = [] #[(),(),()]
        all_json_res_photo_data = []

        print(photo_images)

        # user_id => island_unique_number
        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """SELECT island_unique_number
                        FROM user_tb 
                        WHERE user_id = %s"""
                cursor.execute(query,user_id)
                island_unique_numbers = cursor.fetchall()
                # print(data)
        except Exception as e:
            print("user_tb SELECT Exception! : ",e)
            return 'Exception!' + e 

        # finally:
        #     conn.close()

        # print(island_unique_numbers)
        island_unique_number = island_unique_numbers[0][0]
        # print(island_unique_number)
        
        # island_unique_number  => user_nickname, face_encoding

        try:

            # SELECT
            with conn.cursor() as cursor:
                query = """SELECT fd.user_nickname, fd.face_encoding
                        FROM facial_data_tb as fd
                        JOIN user_tb as ut ON fd.user_id = ut.user_id
                        WHERE ut.island_unique_number = %s"""
                
                cursor.execute(query,island_unique_number)
                nicknames_encodings = cursor.fetchall()
                # print(data)
            
        except Exception as e:  
            print("facial_data_tb SELECT Exception : ",e)

        # print(len(nicknames_encodings))
        # print(len(nicknames_encodings[0]))
        # print(np.array(eval(nicknames_encodings[0][1])).shape)

        # finally:
        #     conn.close()

        for nickname,encoding in nicknames_encodings:
            face_encoding_dict[nickname] = np.array(eval(encoding))

        for idx,photo_image in enumerate(photo_images):
            
            json_res_one_image_data = {}
            # origin_conv = conv.copy()

            # 0에서 9 사이의 난수 10개 생성하고 문자열로 변환
            random_numbers = [str(random.randint(0, 9)) for _ in range(10)]
            random_string = ''.join(random_numbers)

            print("------------------ ",idx+1," ------------------")
            #####################
            # Model Loading (Ver1)
            #####################
            # tokenizer, model, llava_image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug = image_processor.load_llava_model()

            # filename
            file_name = photo_image.filename.lower()

            # photo_datetime
            photo_datetime,photo_latitude,photo_longitude,photo_location = image_processor.get_metadata(photo_image)

            print("########")
            print("photo_datetime :",photo_datetime)
            print("latitude:",photo_latitude)
            print("longitude:",photo_longitude)
            print("########")

            if photo_datetime=='' or photo_datetime==None:
                photo_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if photo_latitude==''or photo_latitude==0:
                photo_latitude = 0
                photo_longitude = 0
                photo_location = '경기도 수지구'

            # character (list)
            character = image_processor.face_recognition(photo_image,face_encoding_dict)
            # character origin
            character_origin = character.copy()
            print("character : ",character)

            # for char in character:
            #     if char == 'Unknown':
            #         character.remove('Unknown')

            character_check = [x for x in character if x != 'Unknown'] 

            print("character_check : ",character_check)
            
            # character_summary = ",".join(character_check).replace(",","와 ")

            # print(" character_summary : ", character_summary)

            # inference_outputs = image_processor.llava_inference_image(
            #         tokenizer,
            #         model,
            #         llava_image_processor,
            #         context_len,
            #         image_aspect_ratio,
            #         roles,
            #         origin_conv,
            #         temperature,
            #         max_new_tokens,
            #         debug,
            #         photo_image,
            #         character_origin)

            # tags = re.sub("Places|Place|People|</s>|\\n|:|1. |\.|,,|, ,","",inference_outputs[0])
            # tags = re.sub(r':','',tags)
            # tags = re.sub("2.|3.|4.|5.|6.|7.|8.|9.|10.|11.|12.|13.|14.|15.|Backgrounds|Objects|Background|Object",",",tags)

            # summary = re.sub("summary|</s>|\\n:","",inference_outputs[1])
            # tags = translator.translate(tags,dest='ko',src='en').text

            # summary
            # summary = translator.translate(summary,dest='ko',src='en').text

            # tags = re.sub(" ","",tags)

            # tags
            # tags = list(set(tags.split(",")))
            # tags = str(tags)

            # tags = inference_outputs[1]
            # tags = re.sub("</s>","",tags)
            # tags = tags[:900]
            # tags = translator.translate(tags,dest='ko',src='en').text
            
            # summary = inference_outputs[0].split(",")[0]
            # summary = re.sub("</s>","",summary)
            # summary = translator.translate(summary,dest='ko',src='en').text.replace(".","") + " " + character_summary
            # summary_strip = summary.replace(" ","")
            
            save_name = save_root_family+photo_image.filename.split(".")[0]+'_'+str(character)+'.jpg'
            PIL_photo_image = Image.open(photo_image)
            PIL_photo_image.save(save_name)


            print("bucket_dir+file_name : ",bucket_dir+family_photo_dir+random_string+'_'+file_name)
            put_object_result = S3.put_object(s3,bucket,save_name,bucket_dir+family_photo_dir+random_string+'_'+file_name) # Save
            print("Save Face Data to S3 : ",put_object_result)
            family_photo_url = S3.get_image_url(s3,bucket,bucket_dir+family_photo_dir+random_string+'_'+file_name)
            print("Family Photo URL : ",family_photo_url)


            _input = prompt.format_prompt(question=image_processor.get_user_query(family_photo_url,str(character_origin),photo_datetime,photo_location))
            output = chat_model(_input.to_messages())
            parsed = parser.parse(output.content)
            print(output.content)
            print(parsed)
            print(re.sub(r'[^\w\s\d!,]', '',parsed.summary))

            tags = str(parsed.search_keywords)
            summary = re.sub(r'[^\w\s\d!,]', '',parsed.summary)
            summary_strip = summary.replace(" ","")
            
            one_family_photo_data = (user_id,island_unique_number,photo_datetime,photo_latitude,photo_longitude,photo_location,str(character_origin),tags,summary,summary_strip,family_photo_url,family_photo_url)
            # one_image_data = (user_id,island_unique_number,photo_datetime,character,tags,summary)


            registration_photo_datetime = str(photo_datetime).replace(":","-").split(" ")[0]
            registration_photo_location = photo_location
            print("photo_location : ",photo_location)
            print("registration_photo_location : " ,registration_photo_location)
            if registration_photo_location!='경기도 수지구':
                registration_photo_location_list = str(photo_location).replace(" ","").split(",")
                if registration_photo_location_list[-1]=='대한민국':
                    get_gu = False
                    for location in registration_photo_location_list[::-1]:
                        if location[-1]=='구':
                            registration_photo_location =  location + " "
                            get_gu = True
                            continue
                        if get_gu:
                            registration_photo_location += location
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
                        registration_photo_location = korean_strings[-1] + " " + korean_strings[0]
                    else:
                        registration_photo_location = korean_strings[-1]
            
            one_json_res_photo_data = {"photo_image":family_photo_url,"character":character_origin,"photo_location":registration_photo_location,"photo_datetime":registration_photo_datetime,"summary":summary}
            all_family_photo_data.append(one_family_photo_data)
            all_json_res_photo_data.append(one_json_res_photo_data)
            print(all_json_res_photo_data)
        # print(len(all_family_photo_data[0]))
        # print(len(all_family_photo_data))
        # print("-----------------------")
        # try:
            # INSERT

        # try :
        with conn.cursor() as cursor:
            
            # query = """INSERT INTO family_photo_tb (user_id,island_unique_number,photo_datetime,photo_latitude,photo_longitude,photo_location,`character`,tags,summary,summary_strip,photo_image,photo_thumbnail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            # cursor.executemany(query,all_family_photo_data)
            # photo_id = cursor.row
            # print("Last Inserted ID:", photo_id)

            query = """INSERT INTO family_photo_tb (user_id,island_unique_number,photo_datetime,photo_latitude,photo_longitude,photo_location,`character`,tags,summary,summary_strip,photo_image,photo_thumbnail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            photo_ids = []

            for idx,one_family_photo_data in enumerate(all_family_photo_data):
                cursor.execute(query,one_family_photo_data)
                
                # Get the last inserted ID for each iteration
                photo_id = cursor.lastrowid
                photo_ids.append(photo_id)

                all_json_res_photo_data[idx]['photo_id'] = photo_id

        print("photo_ids:", photo_ids)
        conn.commit()


        # except Exception as e:  
        #     print("family_photo_tb INSERT Exception : ",e)




        # finally:
        #     conn.close()
    
        # except Exception as e:
        #     print("family_photo_tb INSERT Exception : ",e)

        print('Complete Album Registration (POST)')

        res_json={
                    'data' : all_json_res_photo_data
                }
        
        # res_json={
        #             'data' : {
        #                         'island_unique_number' : island_unique_number,
        #                         'user_id' : user_id,
        #                         'message':'사진 저장 완료!',
        #                         'images_count':len(photo_images),
        #                         'description':'Complete Register Family data'
        #                     }
        #         }

        return jsonify(res_json)
        # return 'Complete Album Registration (POST)'
    
    elif request.method=='GET':

        return 'Complete Album Registration (GET)'
