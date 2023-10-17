from flask import Blueprint
from flask import request
from PIL import Image
import pickle
from Family_Album.models.face_recognition import face_recognition
import numpy as np

bp = Blueprint('face_registration',__name__,url_prefix='/face_registration')

save_root_single = 'data(Family_Album)/face_registration/single/'
save_root_multiple = 'data(Family_Album)/face_registration/multiple/'
save_root_db = 'data(Family_Album)/db/'

face_registration_db = {}

# 가족 구성원별 이미지 데이터 받기/안면 데이터 저장
# ex) 어머니-이미지, 아버지-이미지, 딸-이미지...  
@bp.route('/get_single_data',methods=['GET','POST'])
def get_face_img():
    
    if request.method=='POST':

        print("체크 request.form : ", request.form)
        member_id = request.form['member_id']

        # requerst.files로 안들어오면 안받아진 것임
        print("체크 request.files : ", request.files)
        f = request.files['image']

        # 확장자로 .png 확장자 거를 수도 있음
        print("체크 f : ",f)
        print("체크 f.filename : ", f.filename)

        save_name = save_root_single+member_id+'.jpg'
        f.save(save_name)

        # img = Image.open(save_name)

        img = face_recognition.load_image_file(save_name)
        encoding = face_recognition.face_encodings(img)[0]

        face_registration_db[member_id] = encoding

        with open(save_root_db+'/face_registration_db.pickle', 'wb') as f:
            pickle.dump(face_registration_db, f)

        return 'Complete Single Face Registration (POST)'

    elif request.method=='GET':
        
        return 'Complete Single Face Registration (GET)'