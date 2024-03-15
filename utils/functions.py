import base64
import io
import numpy as np
from openai import OpenAI

import cv2

from PIL import Image
import requests
from loguru import logger
from dotenv import load_dotenv
import json
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering

from time import time
base = time()

p = pyaudio.PyAudio()
cache_dir = "./models"

load_dotenv()
client = OpenAI()

logger.info('Initializing Models...')
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir=cache_dir)
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir=cache_dir).to("cuda")
logger.debug(f'Loaded Salesforce/blip-image-captioning-large in {time()-base}s')
base = time()

vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base", cache_dir=cache_dir)
vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base", cache_dir=cache_dir).to("cuda")
logger.debug(f'Loaded Salesforce/blip-vqa-base in {time()-base}s')
base = time()

class Models:
    
    @staticmethod
    async def generate_questions(context: str):
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': f'''You are an intelligent model who can frame few questions which is suitable for getting an even more detailed description from the current known information form the context specified below do not frame the questions in "REQUEST METHOD" they need to be of "ORDER TYPE"
                            Make sure that you ask questions in such a way that it always has an answer with detailed description
                            Context: {context}
                            GIVE THE OUTPUT IN PROPER JSON FORMAT WITH CORRECT , and " USAGE DO NOT MESS THIS UP AND THE QUESTIONS KEY SHOULD ONLY HOLD AN ARRAY OF STRING!! where question is an array of differenent questions
                            Limit the questions to maximum 6
                            
                        '''
                }
            ],
            stream=False
        )
        
        # logger.debug(stream.choices[0].message.content)
        return json.loads(stream.choices[0].message.content)['questions']
    
    @staticmethod
    async def describe(img: str):

        raw_image = Image.open(requests.get(img, stream=True).raw).convert('RGB')
        inputs = caption_processor(raw_image, return_tensors="pt").to("cuda")
        out = caption_model.generate(**inputs)

        return caption_processor.decode(out[0], skip_special_tokens=True)
    
    @staticmethod
    async def describe(img: bytes):

        raw_image = Image.open(io.BytesIO(img)).convert('RGB')
        inputs = caption_processor(raw_image, return_tensors="pt").to("cuda")
        out = caption_model.generate(**inputs)

        return caption_processor.decode(out[0], skip_special_tokens=True)
    
    
    @staticmethod
    async def question(img: str, questions: list[str]):

        raw_image = Image.open(requests.get(img, stream=True).raw).convert('RGB')
        # raw_image = Image.open(BytesIO(base64.b64decode(data['img_raw']))).convert('RGB')

        output = {}
        for i in questions:
            inputs = vqa_processor(raw_image, i, return_tensors="pt").to("cuda")
            out = vqa_model.generate(**inputs)
            output[i] = vqa_processor.decode(out[0], skip_special_tokens=True)


        return output
   
    @staticmethod
    async def question(img: bytes, questions: list[str]):

        raw_image = Image.open(io.BytesIO(img)).convert('RGB')

        output = {}
        for i in questions:
            inputs = vqa_processor(raw_image, i, return_tensors="pt").to("cuda")
            out = vqa_model.generate(**inputs)
            output[i] = vqa_processor.decode(out[0], skip_special_tokens=True)


        return output
    
    
    @staticmethod
    async def generate_result(qa: dict[str, str]):

        qa_joint = ','.join([f"{x}:{y}" for x,y in qa.items()])

        # logger.debug(qa_joint)

        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': f'''You are an intelligent model who can generate a complete meaningful sentence with the provided question and answer context and the sentence should make full sence of the surrounding data and keep in mind that you are describing it for a blind person so make sure that its understandable
                            Question:Answer pairs =  {qa_joint}
                        '''
                }
            ],
            stream=False
        )
        return stream.choices[0].message.content
    

    @staticmethod
    async def compute_summary(img: str):
        context = await Models.describe(img)
        logger.info('Generated context!')
        questions = await Models.generate_questions(context)
        logger.info('Generated questions!')
        qa = await Models.question(img, questions)
        logger.info('Generated qa!')
        result = await Models.generate_result(qa)
        logger.info('Generated result!')
        logger.debug('---------------------------------------------------')
        logger.info(f'Output: {result}')
        return result
    
    @staticmethod
    async def compute_summary(img: bytes):
        # print(base64.b64decode(img).decode())
        # jpg_as_np = np.frombuffer(img, dtype=np.uint8)
        # img = cv2.imdecode(jpg_as_np, flags=1)
        # cv2.imshow('frame', img)
        logger.debug('---------------------------------------------------')
        context = await Models.describe(img)
        logger.info(f'Generated context: {context}')
        questions = await Models.generate_questions(context)
        logger.info(f'Generated questions: {questions}')
        qa = await Models.question(img, questions)
        logger.info(f'Generated qa: {qa}')
        result = await Models.generate_result(qa)
        logger.info(f'Generated result: {result}')
        logger.debug('---------------------------------------------------')
        return result
