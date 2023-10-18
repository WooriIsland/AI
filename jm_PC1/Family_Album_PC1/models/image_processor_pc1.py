from Family_Album_PC1.models.LLaVA.llava.serve import cli
from Family_Album_PC1.models.LLaVA.llava.serve.cli import load_custom_model,inference_image

class Image_Processor_PC1():

    def __init__(self):
        pass

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
            




    