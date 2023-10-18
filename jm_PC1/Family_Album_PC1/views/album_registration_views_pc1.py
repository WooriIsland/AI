from flask import Blueprint
from flask import request
from Family_Album_PC1.models.image_processor_pc1 import Image_Processor_PC1
import copy
import os
# from Family_Album_PC1.models.LLaVA.llava.serve.cli import load_custom_model,load_image,inference_image


bp = Blueprint('album_registration_pc1',__name__,url_prefix='/album_registration_pc1')

# 1. 여러 가족사진 이미지 요청
# 2. 가족 사진별 배경/물체 단어 태그
# 3. 가족 사진별 한문장 요약

image_processor_pc1 = Image_Processor_PC1()
os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1'

@bp.route('/images_analysis_pc1',methods=['GET','POST'])
def images_analysis_task_pc1():
    if request.method=='POST':

        family_id = request.form['family_id']

        files = request.files.getlist("image")

        for idx,file in enumerate(files):

            tokenizer, model, image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug = image_processor_pc1.load_llava_model()
            
            tokenizer_tmp = copy.deepcopy(tokenizer)
            image_processor_tmp = copy.deepcopy(image_processor)

            print("------ file",idx+1," inference ------")
            inference_outputs = image_processor_pc1.llava_inference_image(
                                tokenizer_tmp,
                                model,
                                image_processor_tmp,
                                context_len,
                                image_aspect_ratio,
                                roles,
                                conv,
                                temperature,
                                max_new_tokens,
                                debug,
                                file)

            print(" inference_outputs : ", inference_outputs)
            
        return 'Complete Album Registration PC1 (POST)'
    
    elif request.method=='GET':

        return 'Complete Album Registration PC1 (GET)'