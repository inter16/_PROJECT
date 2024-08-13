# import aiohttp
# import asyncio
# from io import BytesIO
# from ai import audio
# import cv2


# video=False
# url=''

    
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

#                         audio_detect=audio.detect(audio_data)
#                         with audio_data:
#                             try:
#                                 audio_detect=audio.detect(audio_data)
#                                 if audio_detect:
#                                     await video_stream(url)
#                                     audio_data = BytesIO()
#                             except:
#                                 print("Something err")
#                         audio_data.seek(0)
#                         audio_data.truncate(0)
#             else:
#                 return {"error": "Could not retrieve stream"}
            

# async def video_stream(url):
#     print("Video stream started...")
#     frame_count = 0  # 프레임 수를 추적하는 변수
#     frames = []  # 30프레임을 저장할 리스트

#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 bytes_stream = b''
#                 async for chunk in response.content.iter_chunked(1024):
#                     bytes_stream += chunk
                    
#                     # 프레임 데이터를 디코딩할 수 있는지 확인
#                     a = bytes_stream.find(b'\xff\xd8')  # JPEG 이미지 시작 바이트
#                     b = bytes_stream.find(b'\xff\xd9')  # JPEG 이미지 끝 바이트
#                     if a != -1 and b != -1:
#                         jpg = bytes_stream[a:b + 2]
#                         bytes_stream = bytes_stream[b + 2:]
                        
#                         # 프레임 디코딩 및 처리
#                         img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        
#                         if img is not None:
#                             frames.append(img)  # 프레임을 리스트에 추가
#                             frame_count += 1  # 프레임 수 증가
#                             print(f"Frame {frame_count} received and stored.")
                            
#                             # 30프레임이 쌓이면 감지 작업 실행
#                             if frame_count == 30:
#                                 perform_detection(frames)
#                                 frames.clear()  # 프레임 리스트 초기화
#                                 frame_count = 0  # 프레임 카운트 초기화
                            
#                             # 이미지 처리 로직
#                             cv2.imshow("Stream", img)
#                             if cv2.waitKey(1) == 27:  # ESC 키를 누르면 종료
#                                 break
#             else:
#                 print("Could not retrieve image stream")