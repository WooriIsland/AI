from flask import Blueprint
from flask import request
from flask import jsonify
from PIL import Image
import pickle
from Family_Album_INTEG.models.face_recognition import face_recognition
import numpy as np

bp = Blueprint('face_registration_integ',__name__,url_prefix='/face_registration_integ')

save_root_indivisuals = 'data(Family_Album)/face_registration/indivisuals/'
save_root_db = 'data(Family_Album)/db/'

face_registration_db = {}
with open(save_root_db+'face_registration_db.pickle', 'rb') as f:
    face_registration_db = pickle.load(f)

# 가족 구성원별 이미지 데이터 받기/안면 데이터 저장
# ex) 어머니-이미지, 아버지-이미지, 딸-이미지...  
@bp.route('/upload_data',methods=['GET','POST'])
def get_face_img():
    
    if request.method=='POST':

        print("체크 request.form : ", request.form)

        # family_id 임의로 고정
        family_id = request.form['family_id'] # 'family_1'
        member_id = request.form['member_id'] # 'daughter1', 'father', 'grandmother'...

        if family_id not in face_registration_db.keys():
            face_registration_db[family_id] = {}

        # requerst.files로 안들어오면 안받아진 것임
        print("체크 request.files : ", request.files)
        f = request.files['image']

        # 확장자로 .png 확장자 거를 수도 있음
        print("체크 f : ",f)
        print("체크 f.filename : ", f.filename)

        save_name = save_root_indivisuals+member_id+'.jpg'
        print(save_name)
        f.save(save_name)

        img = face_recognition.load_image_file(save_name)
        encoding = face_recognition.face_encodings(img)[0]

        face_registration_db[family_id][member_id] = encoding
        print(face_registration_db)

        # DB에 저장
        with open(save_root_db+'face_registration_db.pickle', 'wb') as f:
            pickle.dump(face_registration_db, f)

        print('Complete Face Registration (POST)')
        
        # 서버에 안면 데이터 저장 완료 응답
        res_json = {
                        'description':'서버에 안면 데이터 저장 완료 응답',
                        'family_id':family_id,
                        'member_id':member_id
                                                    }
        return jsonify(res_json)

    elif request.method=='GET':
        
        return 'Complete Face Registration (GET)'