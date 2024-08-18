from datetime import datetime

# test_user1={
#     "id":"01066666666",
#     "password":"thisishashedobject1",
#     "name":"test acount 1",
#     "sensors":["111111111111","222222222222"],
#     "loc":"11"
# }
# test_user2={
#     "id":"01077777777",
#     "password":"thisishashedobject2",
#     "name":"test acount 2",
#     "sensors":["333333333333","444444444444"],
#     "loc":"11"
# }
# test_sensor1={
#     "id":"111111111111",
#     "user":"01066666666",
#     "name":"test sensor 1"
# }
# test_sensor2={
#     "id":"222222222222",
#     "user":"01066666666",
#     "name":"test sensor 2"
# }
# test_sensor3={
#     "id":"333333333333",
#     "user":"01077777777",
#     "name":"test sensor 3"
# }
# test_sensor4={
#     "id":"444444444444",
#     "user":"01077777777",
#     "name":"test sensor 4"
# }

log1=[
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T00:20:54.907000"),"status":0},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T00:50:54.907000"),"status":2},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T04:20:54.907000"),"status":2},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T07:20:54.907000"),"status":2},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T07:20:55.907000"),"status":3},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T07:26:54.907000"),"status":4},
        {"sn":"111111111111","date":datetime.fromisoformat("2024-08-17T16:20:54.907000"),"status":1},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T00:22:54.907000"),"status":0},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T00:48:54.907000"),"status":2},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T04:21:54.907000"),"status":2},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:19:54.907000"),"status":2},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:19:55.907000"),"status":3},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:27:54.907000"),"status":4},
        {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T16:19:54.907000"),"status":1}
    ]
log1=sorted(log1, key=lambda x : x["date"])
# log2=[
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T00:22:54.907000"),"status":0},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T00:48:54.907000"),"status":2},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T04:21:54.907000"),"status":2},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:19:54.907000"),"status":2},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:19:55.907000"),"status":3},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T07:27:54.907000"),"status":4},
#         {"sn":"222222222222","date":datetime.fromisoformat("2024-08-17T16:19:54.907000"),"status":1}
#     ]




