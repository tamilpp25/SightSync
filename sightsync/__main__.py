from io import BytesIO
from quart import Quart, request
import traceback

from time import time
from loguru import logger

import base64
from utils.functions import Models

app = Quart(__name__)
base = time()

@app.post("/describe")
async def describe():
    try:
        
        data = await request.get_json()
        output = await Models.describe(data['img_url'])

        return {
            'code': 0,
            'data': output
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }


@app.post("/qa")
async def qa():
    try:

        data = await request.get_json()
        output = await Models.question(data['img_url'], [data['q']])

        return {
            'code': 0,
            'data': output
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }


@app.post("/summary")
async def summary():
    try:

        data = await request.get_json()
        output = await Models.compute_summary(data['img_url'])

        return {
            'code': 0,
            'data': output
        }
    
    except Exception as E:
        traceback.print_exc()
        return {
            'code': -1,
            'err': E
        }



if __name__ == "__main__":
    logger.debug(f'Backend running on http://127.0.0.1:5000')
    app.run(port=5000)