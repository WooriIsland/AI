from flask import Blueprint
from flask import request
from flask import jsonify
from flask import send_file
from flask import request
import pickle
from glob import glob

bp = Blueprint('album_inquiry_integ',__name__,url_prefix='/album_inquiry_integ')

# 가족 앨범 조회

save_root_db = 'data(Family_Album)/db/'

# family_1_album_registration_db = glob(save_root_db+'inquiry_family/')

album_registration_db = {}

def read_image_to_binary(image_path):
    try:
        with open(image_path, "rb") as image_file:
            binary_data = image_file.read()
            binary_data = binary_data.decode('latin-1')
            return binary_data
    except FileNotFoundError:
        return None

# 가족 앨범 조회
@bp.route('/inquiry',methods=['GET','POST'])
def inquiry_family_album():


    with open(save_root_db+'album_registration_db.pickle', 'rb') as f:
        album_registration_db = pickle.load(f)

    if request.method=='POST':

        family_id = request.get_json()['family_id']

        for i in range(len(album_registration_db[family_id])):

            print("------------------------------------------------------------------------------------------")
            print(album_registration_db[family_id][i]['filename'])
            print(album_registration_db[family_id][i]['date_time'])
            print(album_registration_db[family_id][i]['character'])
            print(album_registration_db[family_id][i]['tags'])
            print(album_registration_db[family_id][i]['summary'])

        family_json = album_registration_db[family_id]

        # imgs_name = album_registration_db[family_id].keys()

        # for img_name in imgs_name:
        #     img_path = save_root_db+'inquiry_family/'+family_id+'/'+img_name
        #     # family_json
        res_family_json = {'data': family_json}

        return jsonify(res_family_json)
    
    elif request.method=='GET':

        return 'Complete Album Inquiry (GET)'