from flask import Blueprint,request,jsonify
import base64
from Family_Album_INTEG.models.images_analysis.image_processor import Image_Processor
from PIL import Image
import re
import googletrans
import pymysql
from config import DBConfig
import datetime
import numpy as np

bp = Blueprint('album_registration_integ',__name__,url_prefix='/album_registration_integ')

# DB
conn = pymysql.connect(host=DBConfig.MYSQL_HOST, user=DBConfig.MYSQL_USER, password=DBConfig.MYSQL_PASSWORD, db=DBConfig.MYSQL_DB, charset=DBConfig.MYSQL_CHARSET)

# 1. 메타데이터 추출 - Python 코드
# 2. 인물 추출 - Face Recognition
# 3. 배경/물체 추출 - LLaVa
# 4. 요약 문장 생성 - LLaVa

 # 이미지 분석 객체
image_processor = Image_Processor()
# 번역 객체
translator = googletrans.Translator()
# Local Save Root
save_root_family = 'data(Family_Album)/family/'

@bp.route('/images_analysis',methods=['GET','POST'])
def images_preprocessing():

    if request.method=='POST':

        user_id = request.form['user_id'] # 2
        # print(island_unique_number)
        # print(type(island_unique_number))
        photo_images = request.files.getlist("photo_image")
        face_encoding_dict = {} # key = nickname, value = np.array[,,,]
        all_family_photo_data = [] #[(),(),()]

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

        for nickname,encoding in nicknames_encodings:
            face_encoding_dict[nickname] = np.array(eval(encoding))

        for idx,photo_image in enumerate(photo_images):
            
            print("------------------ ",idx+1," ------------------")
            
            tokenizer, model, llava_image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug = image_processor.load_llava_model()

            # photo_datetime
            photo_datetime,photo_latitude,photo_longitude = image_processor.get_metadata(photo_image)
            if photo_datetime=='':
                photo_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # character (list)
            character = image_processor.face_recognition(photo_image,face_encoding_dict)
            character = str(character)

            inference_outputs = image_processor.llava_inference_image(
                    tokenizer,
                    model,
                    llava_image_processor,
                    context_len,
                    image_aspect_ratio,
                    roles,
                    conv,
                    temperature,
                    max_new_tokens,
                    debug,
                    photo_image)

            tags = re.sub("Places|Place|People|</s>|\\n|:|1. |\.|,,|, ,","",inference_outputs[0])
            tags = re.sub(r':','',tags)
            tags = re.sub("2.|3.|4.|5.|6.|7.|8.|9.|10.|11.|12.|13.|14.|15.|Backgrounds|Objects|Background|Object",",",tags)

            summary = re.sub("summary|</s>|\\n:","",inference_outputs[1])

            tags = translator.translate(tags,dest='ko',src='en').text

            # summary
            summary = translator.translate(summary,dest='ko',src='en').text

            tags = re.sub(" ","",tags)

            # tags
            tags = list(set(tags.split(",")))
            tags = str(tags)
            
            save_name = save_root_family+photo_image.filename.split(".")[0]+'_'+str(character)+'.jpg'
            PIL_photo_image = Image.open(photo_image)
            PIL_photo_image.save(save_name)

            photo_image.seek(0)
            # photo_image
            photo_image= base64.b64encode(photo_image.read()).decode('utf-8')
            # photo_thumbnail
            photo_thumbnail = base64.b64encode(PIL_photo_image.resize((320,320)).tobytes()).decode('utf-8')

            # print(" filename : ",photo_image.filename)
            # print("user_id : ",user_id, "type : ",type(user_id))
            # print("island_unique_number : ",island_unique_number, "type : ",type(island_unique_number))
            # print("photo_datetime : ", photo_datetime, "type : ",type(photo_datetime))
            # print("character :", character, "type : ",type(character))
            # print("tags :",tags, "type : ",type(tags))
            # print("summary :",summary, "type : ",type(summary))
            # print(type(photo_image))
            # print(type(photo_thumbnail))

            print(len(photo_image))
            print(len(photo_thumbnail))
            
            one_image_data = (user_id,island_unique_number,photo_datetime,character,tags,summary,photo_image,photo_thumbnail)
            # one_image_data = (user_id,island_unique_number,photo_datetime,character,tags,summary)
            all_family_photo_data.append(one_image_data)

        # print(len(all_family_photo_data[0]))
        # print(len(all_family_photo_data))
        # print("-----------------------")
        # try:
            # INSERT
        with conn.cursor() as cursor:
            
            query = """INSERT INTO family_photo_tb (user_id,island_unique_number,photo_datetime,`character`,tags,summary,photo_image,photo_thumbnail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.executemany(query,all_family_photo_data)

        conn.commit()
    
        # except Exception as e:
        #     print("family_photo_tb INSERT Exception : ",e)

        print('Complete Album Registration (POST)')

        res_json={
                    'message':'저장 완료!',
                    'images_count':len(photo_images),
                    'description':'Complete Register Family data'
                    }

        return jsonify(res_json)
        # return 'Complete Album Registration (POST)'
    
    elif request.method=='GET':

        return 'Complete Album Registration (GET)'
