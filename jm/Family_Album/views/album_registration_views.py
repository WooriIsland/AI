from flask import Blueprint
from flask import request
from Family_Album.models.images_analysis.image_processor import Image_Processor
from PIL import Image
import pickle

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
with open(save_root_db+'album_registration_db.pickle', 'rb') as f:
    album_registration_db = pickle.load(f)
face_registration_db = {}
with open(save_root_db+'/face_registration_db.pickle', 'rb') as f:
    face_registration_db = pickle.load(f)

@bp.route('/images_analysis',methods=['POST'])
def images_preprocessing():

    if request.method=='POST':

        family_id = request.form['family_id']
        # print('family_id : ',family_id)
        album_registration_db[family_id] = []

        files = request.files.getlist("image")
        miss_cnt = 0

        for file in files:
            file_data = {}

            file_data = image_processor.get_metadata(file)
            file_data = image_processor.face_recognition(file_data,file,face_registration_db[family_id])

            album_registration_db[family_id].append(file_data)

            print(file.filename)
            save_name = save_root_family+file.filename.split(".")[0]+f'_{file_data["character"]}.jpg'

            if str(file_data["character"])=='[]':
                miss_cnt += 1
                
            # print("save name : ",save_name)
            save_file = Image.open(file)
            save_file.save(save_name)

        with open(save_root_db+'album_registration_db.pickle', 'wb') as f:
            pickle.dump(album_registration_db,f)

        print("miss_cnt : ",miss_cnt)
        print(album_registration_db)
        return 'Complete Album Registration (POST)'
    
    elif request.method=='GET':

        return 'Complete Album Registration (GET)'
