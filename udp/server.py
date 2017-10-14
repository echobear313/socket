import socket
import json
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')

users = [{"Hzzone": "1111"}, {"xiaoxiong": "1111"}]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 23000))
sock.listen(5)
while True:
    conn, address = sock.accept()
    msg = conn.recv(1024)
    if msg:
        logging.debug('received from client: %s' % msg)
        dic = json.loads(msg.decode())
        if dic["type"] == "login":
            account = dic["account"]
            password = dic["password"]
            user = {account: password}
            if user in users:
                print("%s 登录成功" % account)
                # sock.sendto("True".encode(), address)
                conn.sendall("True".encode())
            else:
                # sock.sendto("False".encode(), address)
                conn.sendall("False".encode())
        else:
            # sock.sendto("服务器已接受消息".encode(), address)
            conn.sendall("服务器已接受消息".encode())
        '''
        log 一下，逻辑很简单
        '''
        # print(msg)
