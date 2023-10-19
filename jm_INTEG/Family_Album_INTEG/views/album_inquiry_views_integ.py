from flask import Blueprint
from flask import request
from flask import jsonify
import pickle

bp = Blueprint('album_inquiry_integ',__name__,url_prefix='/album_inquiry_integ')

# 가족 앨범 조회

save_root_db = 'data(Family_Album)/db/'

album_registration_db = {}
with open(save_root_db+'album_registration_db.pickle', 'rb') as f:
    album_registration_db = pickle.load(f)

# 가족 앨범 조회
@bp.route('/inquiry',methods=['GET','POST'])
def inquiry_family_album():

    if request.method=='POST':

        family_id = request.form['family_id']

        print(album_registration_db[family_id])

        return jsonify(album_registration_db[family_id])
    
    elif request.method=='GET':

        return 'Complete Album Inquiry (GET)'