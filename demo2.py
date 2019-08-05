# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("ws://192.168.28.158", 50503))
# s.send(b'{"Type":0,"UserID":100000001,"Token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJHcmVlbiIsImF1dGgiOiJ0cmFkZSIsImV4cCI6MTU2MjI5MjI4MCwiaWF0IjoxNTYyMjkxMDgwLCJpc3MiOiJHcmVlbiIsInN1YiI6MTAwMDAwMDAxfQ.BCk4RVZxwIyNoFRmiCPCaIEl15Fv4q1-DpBiVJk4u54","Data":{"Source":1,"Action":1}}')
# sz = s.recv(1024)
# print(sz)
# s.close()
