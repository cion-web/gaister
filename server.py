# coding: utf-8

import socket
import select

def send_to(sock,msg):
    try:
        sock.send(msg.encode())
        return True
    except:
        sock.close()
        return False

def broadcast(socklist,msg):
    for sock in socklist:
        if not send_to(sock,msg):
            socklist.remove(sock)

HOST='127.0.0.1'
PORT=50000
BACKLOG=10
BUFSIZE=4096

server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('socket is created')

try:
    server_sock.bind((HOST,PORT))
    print('socket bind')
    server_sock.listen(BACKLOG)
    print('socket listen')
    sock_list=[server_sock]
    client_sock_table={}
    while True:
        r_ready_sockets,w_ready_sockets,e_ready_sockets=select.select(sock_list,[],[])
        for sock in r_ready_sockets:
            if sock==server_sock:
                conn,address=sock.accept()
                sock_list.append(conn)
                client_sock_table[address[1]]=conn
                sock_list.remove(server_sock)
                
                send_to(client_sock_table[address[1]],str(address[1]))
                index=sock_list.index(client_sock_table[address[1]])
                if index%2==1:
                    send_to(sock_list[index-1],str(address[1]))
                    for key,val in client_sock_table.items():
                        if val==sock_list[index-1]:
                            port=key
                            break
                    send_to(sock_list[index],str(port))

                sock_list.append(server_sock)
                print(str(address)+'is connected')
            else:
                try:
                    b_msg=sock.recv(BUFSIZE)
                    msg=b_msg.decode('utf-8')
                    if len(msg)==0:
                        sock.close()
                        sock_list.remove(sock)
                    else:
                        sender_port=None
                        for key,val in client_sock_table.items():
                            if val==sock:
                                sender_port=key
                                break
                        if sender_port is not None:
                            sock_list.remove(server_sock)

                            index=sock_list.index(client_sock_table[sender_port])
                            if index%2==0:
                                if sock_list[index+1] is not None:
                                    sock=sock_list[index+1]
                            else:
                                sock=sock_list[index-1]

                            broadcast([sock,sock_list[index]],str(sender_port)+","+msg)

                            sock_list.append(server_sock)
                except:
                    sock.close()
                    sock_list.remove(sock)
                    sock_list.remove(server_sock)
                    broadcast(sock_list,'someone disconnected')
                    sock_list.append(server_sock)
except Exception as e:
    print('exception!')
    print(e)
    server_sock.close()
