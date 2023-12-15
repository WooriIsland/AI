import argparse
import torch

from Family_Album_INTEG.models.LLaVA.llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from Family_Album_INTEG.models.LLaVA.llava.conversation import conv_templates, SeparatorStyle
from Family_Album_INTEG.models.LLaVA.llava.model.builder import load_pretrained_model
from Family_Album_INTEG.models.LLaVA.llava.utils import disable_torch_init
from Family_Album_INTEG.models.LLaVA.llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

from PIL import Image

import requests
from PIL import Image
from io import BytesIO
from transformers import TextStreamer

from collections import deque


# def load_image(image_file):
#     if image_file.startswith('http://') or image_file.startswith('https://'):
#         response = requests.get(image_file)
#         image = Image.open(BytesIO(response.content)).convert('RGB')
#     else:
#         image = Image.open(image_file).convert('RGB')
#     return image

def load_image(image_file):

    image = Image.open(image_file).convert('RGB')
    
    return image

def load_custom_model():
    # Model
    disable_torch_init()

    model_path = 'liuhaotian/llava-v1.5-13b'
    model_base = None
    # image_file = 'LLaVA/family(travel)/F0011_GM_F_D_71-46-13_01_travel.jpg'
    device = 'cuda'
    conv_mode_custom = None

    temperature = 0.3 ## 11_17 (alpha) 0.4 , 11_17 (test) 0.1
    max_new_tokens = 50 # 40 => 50, 256, 512, 1024
    load_8bit = False
    load_4bit = False
    debug = False
    image_aspect_ratio = 'pad'

    model_name = get_model_name_from_path(model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, model_base, model_name, load_8bit, load_4bit, device=device)

    if 'llama-2' in model_name.lower():
        conv_mode = "llava_llama_2"
    elif "v1" in model_name.lower():
        conv_mode = "llava_v1"
    elif "mpt" in model_name.lower():
        conv_mode = "mpt"
    else:
        conv_mode = "llava_v0"

    if conv_mode_custom is not None and conv_mode != conv_mode_custom:
        print('[WARNING] the auto inferred conversation mode is {}, while `--conv-mode` is {}, using {}'.format(conv_mode, conv_mode_custom, conv_mode_custom))
    else:
        conv_mode_custom = conv_mode

    conv = conv_templates[conv_mode_custom].copy()
    if "mpt" in model_name.lower():
        roles = ('user', 'assistant')
    else:
        roles = conv.roles

    # print("Complete Model Loading!")
    return tokenizer, model, image_processor, context_len,image_aspect_ratio,roles,conv,temperature,max_new_tokens,debug

def inference_image(tokenizer,
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
    
    # prompts = ['Please list up to 10 nouns that appear in this picture and mean the background without duplication. Adjectives and verbs should be excluded.',
    #            'Please summarize the picture in a sentence centered on the place and background. For example, simply describe it like "a family photo taken in front of a beach" or "a family photo taken in a park surrounded by trees."']

    character_str = ','.join(character_origin)
    print("character_str : ",character_str)
    # prompts = ['You play the role of giving information about weather, countries, cities, surrounding objects, buildings, costumes, facial expressions, and postures that appear in pictures taken with your family or friends. Please list the weather, country, city, surrounding objects, buildings, costumes, facial expressions, posture, etc. in 30 words. Make sure to list them in words instead of sentences. Examples of word listing are "clear, cloudy, Paris, Asian, Europe, sea, tree, bench, park, stadium, colosseum, sandals, jeans, red shirt, laugh, surprise, wink," and so on. Like this, make sure to list the picture in 30 words.',
    #            'You are summarizing the pictures you took with your family or friends in one sentence. The characters (family members) in the picture are {}. Please summarize in 1 sentence based on the weather, surrounding objects, buildings, costumes, facial expressions, posture and characters you just told me. For example, summarize in one sentence: "Dad and Grandma sitting on the beach on a sunny day," "All the family eating out at a fine restaurant," "Mom and Son sitting in the park on a clear day," "Daughters eating cake on their birthday," "Dad and daughter taking a commemorative photo in front of the Eiffel Tower," and "All the family taking a picture at the night market." Be sure to summarize it in the form of "characters in a certain environment" as an example.'.format(character_str)]

    # prompts = ["You are the role of telling me about the background and objects that appear in the input photo. Please list in words objects such as weather, sea, mountains, festivals, stadiums, performance halls, outdoor, indoor, weather, architecture, country, background, hats, glasses, tops, bottoms, shoes, watches, bags, facial expressions, and poses that appear in the picture. Don't tell me in a sentence, but tell me in the form of a list. Examples of word listing are 'clear, cloudy, China, Paris, Asian, Europe, soccer field, sea, park, stadium, Colosseum, trees, benches, fountains, sandals, jeans, red shirt, laughter, surprise, wink,' and so on. Like this, make sure to list the picture in 30 words. At this time, never list overlapping words. Now, list the words.",
    #            'You are the role of summarizing the pictures you took with your family or friends in one sentence. Please summarize in 1 sentence based on the background and objects in the picture you just told me. For example, sum up in one sentence: "A picture taken at sunset beach," "A picture taken while eating out at a fine restaurant!" "At the park on a nice day!" "A picture taken with a happy expression on my birthday," "The day I took a picture in front of the Eiffel Tower," and "A shot at the night market." Be sure to tell me in the same format as the example.']


    # prompts = ["You are the role of telling me about the background and objects that appear in the input photo. Please list in words objects such as weather, sea, mountains, festivals, stadiums, performance halls, outdoor, indoor, weather, architecture, country, background, hats, glasses, tops, bottoms, shoes, watches, bags, facial expressions, etc. that appear in the picture. Don't tell me in a sentence, but tell me in the form of a list. Examples of word listing are: 'Clear, cloudy, China, Paris, Asian, Europe, soccer field, sea, park, stadium, Colosseum, tree, bench, fountain, sandals, jeans, red shirt, laughter, surprise, wink.' Like this, make sure to list the picture in 30 words. At this time, never list overlapping words. Now, list the words.",
    #            "You are the role of summarizing the pictures taken with your family in one sentence. The background of the photos are mainly restaurants, cafes, restaurants, hotels, beaches, downtowns, rivers, trails, overseas trips, weddings, graduations, amusement parks, and aquariums. Describe the background shown in the picture and summarize it in 1 sentence. For example, 'a picture taken at sunset beach,' 'a picture taken when eating out at a high-end restaurant!' 'A nice day at the park!' 'A picture of a couple at an amusement park!' 'A picture of the family gathered in front of the mirror,' 'A picture taken at a hotel buffet,' 'A picture taken at a bright day's walkway,' 'A selfie taken at a pretty store,' 'A selfie taken at a birthday with an exciting expression,' 'A picture taken at a rainy day,' 'A picture of a couple taken at a beautiful cafe,' 'A picture taken at an aquarium.' 'A picture with family at the entrance of the library.' 'A picture taken at the memorial tower.' Summarize it in one sentence like 'a picture at a crowded night market'. Be sure to say it in a concise format like an example. Please omit the information about the person in the picture."]

    # prompts = [
    #            "Summarize the place and its setting in one sentence with up to 10 words. Be sure to exclude descriptions of people in the photo, such as 'man' or 'woman'. For example, 'at an amusement park on a sunny day' or 'at a crowded night market'. Be sure to use the same format as the example.",
    #            "Summarize it again, leaving out the words for 'man','woman' and 'people.'",
    #             "You are the role of telling me about the background and objects that appear in the input photo. Please list in words objects such as weather, sea, mountains, festivals, stadiums, performance halls, outdoor, indoor, weather, architecture, country, background, hats, glasses, tops, bottoms, shoes, watches, bags, facial expressions, etc. that appear in the picture. Don't tell me in a sentence, but tell me in the form of a list. Examples of word listing are: 'Clear, cloudy, China, Paris, Asian, Europe, soccer field, sea, park, stadium, Colosseum, tree, bench, fountain, sandals, jeans, red shirt, laughter, surprise, wink.' Like this, make sure to list the picture in 20 words. At this time, never list overlapping words. Now, list the words."
    #            ]

    # 11_12
    # prompts = [
    #            "Summarize the place, setting or object in one concise sentence of up to 10 words. For example,'At a cherry blossom festival', 'on a soccer field', 'in a forest full of maple trees','in a cozy cafe','in a park on a snowy day','on a sunny beach','at an amusement park on a sunny day', 'in a crowded night market', 'in front of the Eiffel Tower in France', 'in a cafe with pretty coffee cups', 'in front of a grand hotel building', 'in front of a zoo lion', 'inside a baseball stadium', 'in a city park surrounded by trees', 'in a dimly lit restaurant.','in front of a giant waterfall', 'in front of the Statue of Liberty', 'in a sandwich cafe', 'in a crowded movie theater', 'on a boardwalk on a warm day', 'in a quaint clothing store', 'in an atmospheric restaurant', 'in a quiet library', 'in a bookstore surrounded by books', etc. Be sure to use the same format as the example.",
    #             "List the background, objects, clothing, etc. that appear in the given photo in 20 words. The list must be 20 words."
    #            ]

    # prompts = [
    #            "Summarize the place, setting or object in one concise sentence of up to 10 words. For example,'At a cherry blossom festival', 'on a soccer field', 'in a forest full of maple trees','in a cozy cafe','in a park on a snowy day','on a sunny beach','at an amusement park on a sunny day', 'in a crowded night market', 'in front of the Eiffel Tower in France', 'in a cafe with pretty coffee cups', 'in front of a grand hotel building', 'in front of a zoo lion', 'inside a baseball stadium', 'in a city park surrounded by trees', 'in a dimly lit restaurant.','in front of a giant waterfall', 'in front of the Statue of Liberty', 'in a sandwich cafe', 'in a crowded movie theater', 'on a boardwalk on a warm day', 'in a quaint clothing store', 'in an atmospheric restaurant', 'in a quiet library', 'in a bookstore surrounded by books', etc. Be sure to use the same format as the example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #            ]

    # prompts = [
    #            "Summarize the place, setting or object in one concise sentence of up to 10 words.For example, say 'at an atmospheric restaurant' or 'in front of a cool beach'. Make sure to say 'in the ~' in the same format as the example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #            ]
    
    # prompts = [
    #            "Summarize the place, setting or object in one concise sentence of up to 10 words.",
    #             "Please revise it based on the location or background and summarize it again.For example,'At a cherry blossom festival', 'on a soccer field', 'in a forest full of maple trees','in a cozy cafe','in a park on a snowy day','on a sunny beach','at an amusement park on a sunny day', 'in a crowded night market', 'in front of the Eiffel Tower in France', 'in a cafe with pretty coffee cups', 'in front of a grand hotel building', 'in front of a zoo lion', 'inside a baseball stadium', 'in a city park surrounded by trees', 'in a dimly lit restaurant.','in front of a giant waterfall', 'in front of the Statue of Liberty', 'in a sandwich cafe', 'in a crowded movie theater', 'on a boardwalk on a warm day', 'in a quaint clothing store', 'in an atmospheric restaurant', 'in a quiet library', 'in a bookstore surrounded by books', etc. Be sure to answer in a form similar to the example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #            ]

    # prompts = [
    #            "Summarize the place, setting or object in one concise sentence of up to 10 words.",
    #             "Please revise it based on the location or background and summarize it again. For example, 'On a sunny day, in a forest park'. Be sure to say it in the form of an example. Make sure to express it with a phrase that starts with the word 'in the'. ",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #            ]
    
    # 11_17 test , with 0.1
    # prompts = [
    #            "Please describe the picture in detail. Make sure you say no more than 50 words",
    #             "Just tell me about the place or the environment. Make sure to express it with a phrase that starts with the word 'in the'. For example, in a forested park on a sunny day. Be sure to say it in the form of an example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #            ]
    
    # 11_18 test (not bad), with 0.3
    # prompts = [
    #         "Please describe the picture in detail. Make sure you say no more than 50 words",
    #         "Just tell me about the place. Make sure to express it with a phrase that starts with the word 'In the ~ , ' or 'At the ~ ,'. For example, 'In a forested park on a sunny day', 'In a mountain with a panoramic view of the forest','At a restaurant with a warm atmosphere'. Be sure to say it in the form of an example.",
    #         "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #         ]

    # prompts = [
    #             "Just tell me about the place. Make sure to express it with a phrase that starts with the word 'In the ~ '. For example, 'At a cozy cafe with subtle lighting', 'In a mountain with a panoramic view of the forest','In front of the cool beach','At a restaurant with a warm atmosphere'. Be sure to say it in the form of an example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #             ]

    # prompts = [
    #             "Just tell me about the place. Make sure to express it with a phrase that starts with the word 'In ~ , ~ '. For example, 'In a rippling blue ocean on a sunny day, ~ '. Be sure to say it in the form of an example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #             ]

    # 11_18 (best) , 0.4
    # prompts = [
    #             "Just tell me about the place. Make sure to express it with a phrase that starts with the word 'In ~ , ~ '. For example, 'In a mountain with a panoramic view of the forest, ~ '. Be sure to say it in the form of an example.",
    #             "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
    #             ]
    
    prompts = [
                "Just tell me about the place. Make sure to express it with a phrase that starts with the word 'In ~ , ~ '. For example, 'In a mountain with a panoramic view of the forest, ~ ', 'On a busy Japanese street, ~' . Be sure to say it in the form of an example.",
                "List only 20 words for representative objects that appear in the given photo.  The same object should be said only once. Be sure to list them in a maximum of 20 words. "
                ]
    prompts= deque(prompts)
    
    # 추론 return 값
    inference_outputs = []

    image = load_image(image_file)
    # Similar operation in model_worker.py
    # print("------ Complete Image Loading ------")

    image_tensor = process_images([image], image_processor, image_aspect_ratio)
    # print("------ Complete Image Processing ------")

    if type(image_tensor) is list:
        image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
    else:
        image_tensor = image_tensor.to(model.device, dtype=torch.float16)

    # print("------ Before Prompts ------")

    ans_cnt = 0

    while prompts:
        
        prompt = prompts.popleft()

        try:
            inp = prompt
        except EOFError:
            inp = ""
        if not inp:
            print("exit...")
            break
        
        if ans_cnt!=0:
            print(f"{roles[1]}: ", end="")
        ans_cnt += 1

        if image is not None:
            # first message
            if model.config.mm_use_im_start_end:
                inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
            else:
                inp = DEFAULT_IMAGE_TOKEN + '\n' + inp
            conv.append_message(conv.roles[0], inp)
            image = None
        else:
            # later messages
            conv.append_message(conv.roles[0], inp)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
        stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
        streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

        # print("------ Before Inference Mode ------")

        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=image_tensor,
                do_sample=True,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                streamer=streamer,
                use_cache=True,
                stopping_criteria=[stopping_criteria])

        outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
        conv.messages[-1][-1] = outputs

        if ans_cnt!=0:
            inference_outputs.append(conv.messages[-1][-1])

        if debug:
            print("\n", {"prompt": prompt, "outputs": outputs}, "\n")

    return inference_outputs
