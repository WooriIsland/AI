from flask import Blueprint
from flask import request
from Family_Album.models.images_analysis.image_processor import Image_Processor

bp = Blueprint('album_registration',__name__,url_prefix='/album_registration')

# 1. 메타데이터 추출 - Python 코드
# 2. 인물 추출 - Face Recognition
# 3. 배경/물체 추출 - LLaVa
# 4. 요약 문장 생성 - LLaVa

 # 이미지 분석 객체
image_processor = Image_Processor()

save_root_family = 'data(Family_Album)/family/'
save_root_db = 'data(Family_Album)/db/'

album_registration_db = {}

@bp.route('/images_analysis',methods=['POST'])
def images_preprocessing():

    if request.method=='POST':

        family_id = request.form['family_id']
        print('family_id : ',family_id)
        album_registration_db[family_id] = {}

        files = request.files.getlist("image")

        for file in files:
            # print(file.filename)
            album_registration_db[family_id]['filename'] = file.filename

            save_name = save_root_family+file.filename
            # print(save_name)
            file.save(save_name)

            date_time, (lat,lon) = image_processor.get_metadata(save_name)
            album_registration_db[family_id]['date_time'] = date_time
            album_registration_db[family_id]['lat_lon'] = (lat,lon)

        print(album_registration_db)
        return 'Complete Album Registration (POST)'
    
    elif request.method=='GET':

        return 'Complete Album Registration (GET)'
