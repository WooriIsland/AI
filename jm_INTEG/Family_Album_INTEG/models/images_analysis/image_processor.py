from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from Family_Album_INTEG.models.face_recognition import face_recognition
from Family_Album_INTEG.models.LLaVA.llava.serve import cli
from Family_Album_INTEG.models.LLaVA.llava.serve.cli import load_custom_model,inference_image
import numpy as np

class Image_Processor():

    def __init__(self):
        pass

    # 촬영 날짜/시간, 위도/경도 추출
    def get_metadata(self,img):
        img_data = {}
        img_data['filename'] = img.filename

        img = Image.open(img)

        date_time = None
        lat,lon = None,None

        try:
            # with Image.open(image_path) as img:
            # 이미지의 Exif 데이터 읽기
            exif_data = img._getexif()

            if exif_data:
                date_time = None
                gps_info = None

                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)

                    # 촬영 날짜 및 시간 추출 (DateTimeOriginal 또는 DateTime 태그 사용)
                    if tag_name == 'DateTimeOriginal' or tag_name == 'DateTime':
                        date_time = value

                    # GPS 정보 추출
                    if tag_name == 'GPSInfo':
                        gps_info = {}
                        for gps_tag, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                            gps_info[gps_tag_name] = gps_value

                # 촬영 날짜 및 시간 출력
                if date_time:
                    # print(f"촬영 날짜 및 시간: {date_time}")
                    pass
                # GPS 정보 출력
                if gps_info:
                    latitude = gps_info.get('GPSLatitude', None)
                    longitude = gps_info.get('GPSLongitude', None)
                    if latitude and longitude:
                        lat = f"{latitude[0]}° {latitude[1]}' {latitude[2]}'' {gps_info['GPSLatitudeRef']}"
                        lon = f"{longitude[0]}° {longitude[1]}' {longitude[2]}'' {gps_info['GPSLongitudeRef']}"
                        # print(f"촬영 위치 (GPS): 위도 {lat}, 경도 {lon}")
                    else:
                        # print("촬영 위치 (GPS) 정보 없음")
                        pass
            else:
                print("이미지에 Exif 메타데이터가 없습니다.")

        except Exception as e:
            print(f"메타데이터를 추출하는 동안 오류가 발생했습니다: {e}")

        img_data['date_time'] = date_time
        img_data['latitude'] = lat
        img_data['longitude'] = lon 

        return img_data
    

    def face_recognition(self,file_data,img,face_registration_db):
    # def extract_member(img,member_id,member_encoding):

        # print("face_registration_db.values() : ", np.array(face_registration_db.values()))
        # print("face_registration_db.keys() : ",face_registration_db.keys())

        members = []
        member_id = []
        member_encoding = []

        for id,encoding in face_registration_db.items():
            member_id.append(id)
            member_encoding.append(encoding)

        unknown_image = face_recognition.load_image_file(img)
        face_locations = face_recognition.face_locations(unknown_image)
        # print("face_locations : ",face_locations)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(member_encoding, face_encoding)

            name = "Unknown"

            face_distances = face_recognition.face_distance(member_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            # print("best_match_index : ",best_match_index)
            if matches[best_match_index]:
                name = member_id[best_match_index]
            members.append(name)

        file_data['character'] = members

        return file_data
    
    def load_llava_model(self):

        tokenizer, model, image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug = load_custom_model()

        return tokenizer, model, image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug
    
    def llava_inference_image(self,
                    tokenizer,
                    model,
                    image_processor,
                    context_len,
                    image_aspect_ratio,
                    roles,
                    conv,
                    temperature,
                    max_new_tokens,
                    debug,
                    image_file):
        
        inference_outputs = inference_image(tokenizer,
                    model,
                    image_processor,
                    context_len,
                    image_aspect_ratio,
                    roles,
                    conv,
                    temperature,
                    max_new_tokens,
                    debug,
                    image_file)
        
        return inference_outputs