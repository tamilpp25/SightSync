from quart import Quart, request
import requests

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering

caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir="./models")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large", cache_dir="./models").to("cuda")

vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base", cache_dir="./models")
vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base", cache_dir="./models").to("cuda")

app = Quart(__name__)

@app.post("/describe")
async def describe():
    data = await request.get_json()

    raw_image = Image.open(requests.get(data['img_url'], stream=True).raw).convert('RGB')

    inputs = caption_processor(raw_image, return_tensors="pt").to("cuda")

    out = caption_model.generate(**inputs)
    print(caption_processor.decode(out[0], skip_special_tokens=True))

    return {
        'code': 0,
        'data': caption_processor.decode(out[0], skip_special_tokens=True)
    }


@app.post("/qa")
async def qa():
    data = await request.get_json()

    raw_image = Image.open(requests.get(data['img_url'], stream=True).raw).convert('RGB')

    inputs = vqa_processor(raw_image, data['q'], return_tensors="pt").to("cuda")

    out = vqa_model.generate(**inputs)
    print(vqa_processor.decode(out[0], skip_special_tokens=True))

    return {
        'code': 0,
        'data': vqa_processor.decode(out[0], skip_special_tokens=True)
    }


if __name__ == "__main__":
    app.run(port=5000)