import aiohttp
import asyncio
from io import BytesIO
from ai import audio,video
import cv2
import numpy as np


video=False
url=''

    
async def audio_stream(url):
    URL=url+"audio"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                audio_data = BytesIO()
                async for chunk in response.content.iter_chunked(1024):
                    audio_data.write(chunk)
                    
                    if audio_data.tell() > 4096:
                        audio_data.seek(0)
                        with audio_data:
                            try:
                                audio_detect=await audio.detect(audio_data)
                                if audio_detect:
                                    await video_stream(url)
                                    audio_data = BytesIO()
                            except:
                                print("Something err")
                        audio_data.seek(0)
                        audio_data.truncate(0)
            else:
                return {"error": "Could not retrieve stream"}
            

async def video_stream(url):
    URL=url+"video"
    frame_count = 0  
    frames = []  
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                bytes_stream = b''
                async for chunk in response.content.iter_chunked(1024):
                    bytes_stream += chunk
                    a = bytes_stream.find(b'\xff\xd8')  
                    b = bytes_stream.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes_stream[a:b + 2]
                        bytes_stream = bytes_stream[b + 2:]
                        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        if img is not None:
                            frames.append(img)  
                            frame_count += 1
                            if frame_count == 30:
                                asyncio.create_task(video.detect(frames))
                                frames.clear()
                                frame_count = 0

                            if cv2.waitKey(1) == 27: 
                                break
            else:
                return {"error": "Could not retrieve stream"}