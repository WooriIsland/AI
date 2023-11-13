from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from Family_Album_INTEG.models.face_recognition import face_recognition
from Family_Album_INTEG.models.rembg.rembg.bg import remove
from Family_Album_INTEG.models.LLaVA.llava.serve import cli
from Family_Album_INTEG.models.LLaVA.llava.serve.cli import load_custom_model,inference_image
import numpy as np
from geopy.geocoders import Nominatim

class Image_Processor():

    def __init__(self):
        pass

    # 촬영 날짜/시간, 위도/경도 추출
    def get_metadata(self,img):

        img = Image.open(img)

        date_time = ''
        latitude,longitude = 0,0
        location=''

        try:
            # with Image.open(image_path) as img:
            # 이미지의 Exif 데이터 읽기
            exif_data = img._getexif()

            # print(exif_data)
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
                    print(f"촬영 날짜 및 시간: {date_time}")
                    pass
                # GPS 정보 출력
                if gps_info:
                    latitude = gps_info.get('GPSLatitude', None)
                    longitude = gps_info.get('GPSLongitude', None)
                    # print("latitude : ",latitude)
                    # print("longitude : ",longitude)
                    if latitude and longitude:
                        print("#### get_metadata ####")
                        print("latitude:",latitude)
                        print("longitude:",longitude)
                        print("#### get_metadata ####")
                        # lat = f"{latitude[0]}° {latitude[1]}' {latitude[2]}'' {gps_info['GPSLatitudeRef']}"
                        # lon = f"{longitude[0]}° {longitude[1]}' {longitude[2]}'' {gps_info['GPSLongitudeRef']}"
                        # lat = f"{latitude[0]}° {latitude[1]}' {latitude[2]}'' {gps_info['GPSLatitudeRef']}"
                        geolocator = Nominatim(user_agent="coordinateconverter")
                        latitude = round(float(latitude[0])+float(latitude[1])/60+float(latitude[2])/3600,6)
                        # lon = f"{longitude[0]}° {longitude[1]}' {longitude[2]}'' {gps_info['GPSLongitudeRef']}"
                        longitude = round(float(longitude[0])+float(longitude[1])/60+float(longitude[2])/3600,6)

                        print("latitude:",latitude)
                        print("longitude:",longitude)
                        location = geolocator.reverse(str(latitude)+", "+str(longitude))
                        location = location.address
                        print(f"촬영 위치 (GPS): 위도 {latitude}, 경도 {longitude}")
                        if 'nan' in str(latitude):
                            print("lat : ",latitude)
                            print("lon : ",longitude)
                            latitude = 0
                            longitude = 0
                    else:
                        print("촬영 위치 (GPS) 정보 없음")
                        pass
            else:
                print("이미지에 Exif 메타데이터가 없습니다.")

        except Exception as e:
            print(f"메타데이터를 추출하는 동안 오류가 발생했습니다: {e}")

        return date_time,latitude,longitude,location
    
    def extract_character(self,img):
        height, width, channels = 640, 640, 3
        black_image = Image.fromarray(np.zeros((height, width, channels), dtype=np.uint8))
        # black_image = Image.open(black_image)

        # 인물 이미지 (PIL Image로 읽기 및 크기 조정)
        person_image = Image.open(img)

        person_image = person_image.resize((640, 640))

        # 인물 마스킹 이미지 (PIL Image로 읽기 및 크기 조정)
        mask_image = remove(person_image,only_mask=True).convert("L") 
        mask_image = mask_image.point(lambda p: p > 128 and 255)  # 0 또는 255로 수정
        mask_image = mask_image.resize((640, 640))

        # 배경 이미지와 마스킹된 인물 이미지를 결합하여 새로운 이미지 생성 (PIL Image로)
        result = Image.composite(person_image, black_image, mask_image)

        return result


    def face_recognition(self,img,face_encoding_dict):
    # def extract_member(img,member_id,member_encoding):

        # print("face_registration_db.values() : ", np.array(face_registration_db.values()))
        # print("face_registration_db.keys() : ",face_registration_db.keys())

        characters = []
        nicknames = []
        encodings = []

        for id,encoding in face_encoding_dict.items():
            nicknames.append(id)
            encodings.append(encoding)

        unknown_image = face_recognition.load_image_file(img)
        face_locations = face_recognition.face_locations(unknown_image)
        # print("face_locations : ",face_locations)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(encodings, face_encoding)

            name = "Unknown"

            face_distances = face_recognition.face_distance(encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            # print("best_match_index : ",best_match_index)

            ##############################################
            # face recoginiton probabliity 
            # print("face_distances : ",face_distances)

            if matches[best_match_index]:
                name = nicknames[best_match_index]
            characters.append(name)

        return characters
    
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
                    image_file,
                    character_origin):
        
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
                    image_file,
                    character_origin)
        
        return inference_outputs