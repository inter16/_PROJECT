
import aiohttp
import asyncio
from io import BytesIO


# async def audio_stream(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 # 청크 단위로 데이터를 받아와서 처리
#                 audio_data = BytesIO()
#                 async for chunk in response.content.iter_chunked(1024):
#                     audio_data.write(chunk)
                    
#                     # 청크가 충분히 커지면 이를 처리
#                     if audio_data.tell() > 4096:
#                         audio_data.seek(0)
#                         with sr.AudioFile(audio_data) as source:
#                             audio = recognizer.record(source)
#                             try:
#                                 text = recognizer.recognize_google(audio)
#                                 print(f"Recognized text: {text}")
#                                 audio_data = BytesIO()  # 버퍼 초기화
#                             except sr.UnknownValueError:
#                                 print("Could not understand audio")
#                             except sr.RequestError as e:
#                                 print(f"Could not request results; {e}")
#                         audio_data.seek(0)
#                         audio_data.truncate(0)
#             else:
#                 return {"error": "Could not retrieve stream"}

# @app.get("/process-stream")
# async def process_stream():
#     url = "http://<라즈베리파이_IP>:8000/stream"
#     recognizer = sr.Recognizer()

#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 # 청크 단위로 데이터를 받아와서 처리
#                 audio_data = BytesIO()
#                 async for chunk in response.content.iter_chunked(1024):
#                     audio_data.write(chunk)
                    
#                     # 청크가 충분히 커지면 이를 처리
#                     if audio_data.tell() > 4096:
#                         audio_data.seek(0)
#                         with sr.AudioFile(audio_data) as source:
#                             audio = recognizer.record(source)
#                             try:
#                                 text = recognizer.recognize_google(audio)
#                                 print(f"Recognized text: {text}")
#                                 audio_data = BytesIO()  # 버퍼 초기화
#                             except sr.UnknownValueError:
#                                 print("Could not understand audio")
#                             except sr.RequestError as e:
#                                 print(f"Could not request results; {e}")
#                         audio_data.seek(0)
#                         audio_data.truncate(0)
#             else:
#                 return {"error": "Could not retrieve stream"}

