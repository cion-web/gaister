# codeing=utf-8
import tkinter as tk
import math
import socket,select
import threading
from gaister import Gaister

def send_msg(ev=None):
    if len(entered_txt.get())<=0:
        return
    elif len(game.player)<2:
        print_text('対戦相手を探しています')
        etr.delete(0,tk.END)
        return
    elif ',' in entered_txt.get() :
        print_text('「,」は使用できません')
        etr.delete(0,tk.END)
        return

    sock.send(entered_txt.get().encode())
    etr.delete(0,tk.END)

def receive_msg(msg):
    if text_w is None:
        return
    print_text(msg)

def stock_msg(msg):
    stocked_msg.append(msg)

def print_text(msg):
    text_w.configure(state=tk.NORMAL)
    text_w.insert(tk.END,msg+"\n")
    text_w.configure(state=tk.DISABLED)
    text_w.see(tk.END)

def convert_msg(msg):
    nmsg=msg.split(',')
    if len(nmsg)==5:
        for i in range(4):
            nmsg[i+1]=5-int(nmsg[i+1])
    return nmsg

def check_msg():
    while len(stocked_msg)>0:
        msg=convert_msg(stocked_msg.pop(0))
        if len(game.player)<2:
            game.player.append(msg[0])
            if len(game.player)==2:
                print_text('対戦を開始します')
				
        elif len(msg)==2:
            if msg[0]==game.player[0]:
                player='自分'
            else:
                player='相手'
            receive_msg(player+':'+msg[1])
			
        elif msg[0]==game.player[1]:
            game.selection=[msg[1],msg[2]]
            if game.swap(msg[3],msg[4]) is True:
                if not game.judge_victory()==0:
                    if game.judge_victory()==1:
                        print_text('あなたの勝ちです')
                    elif game.judge_victory()==-1:
                        print_text('あなたの負けです')
                    game.set_board()
                    game.set_counter()
                game.turn=True
            print_canvas()
    root.after(200,check_msg)

def reset_canvas():
    for i in range(6):
        for j in range(6):
            canvas.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40,fill='white')

def click(event):
    if len(game.player)<2:
        print_text('対戦相手を探しています')
        return
    if game.turn is False:
        print_text('相手のターンです')
        return
    countgoast=[game.counter[3],game.counter[4]]
    x=math.floor(event.y/40)
    y=math.floor(event.x/40)
    if game.selection==[-1,-1]:
        if game.select(x,y) is True:
            canvas.create_rectangle(y*40,x*40,(y+1)*40,(x+1)*40,outline='red')
    else:
        msg=str(game.selection[0])+','+str(game.selection[1])+','+str(x)+','+str(y)
        sock.send(msg.encode())
        if game.swap(x,y) is True:
            if countgoast[0]>game.counter[3]:
                print_text('相手の青お化けを取りました')
            elif countgoast[1]>game.counter[4]:
                print_text('相手の赤お化けを取りました')
            if not game.judge_victory()==0:
                if game.judge_victory()==1:
                    print_text('あなたの勝ちです')
                elif game.judge_victory()==-1:
                    print_text('あなたの負けです')
                game.set_board()
                game.set_counter()
            game.turn=False
        print_canvas()

def print_canvas():
    reset_canvas()
    for i in range(6):
        for j in range(6):
            if game.board[i][j]==-2:
                color='blue'
            elif game.board[i][j]==-1:
                color='red'
            elif game.board[i][j]==1 or game.board[i][j]==2:
                color='gray'
            else:
                color='white'
            canvas.create_oval(j*40+5,i*40+5,(j+1)*40-5,(i+1)*40-5,fill=color,width=0)

root = tk.Tk()
root.title("ガイスター")
root.geometry("480x240")

canvas = tk.Canvas(root, width=240, height=240, bg="white")
canvas.place(x=0, y=0)
for i in range(6):
    for j in range(6):
        canvas.create_rectangle(i*40,j*40,(i+1)*40,(j+1)*40)

canvas.bind("<Button-1>", click)

frame=tk.Frame(master=root,width=240,height=240)
frame.place(relx=0.5,rely=0,relwidth=0.5,relheight=1)

text_w=tk.Text(master=frame,state=tk.NORMAL,font=('メイリオ','10'),bg="white")
text_w.place(relx=0,rely=0,relwidth=0.85,relheight=0.75)

sb_y=tk.Scrollbar(master=frame,orient=tk.VERTICAL,command=text_w.yview)
sb_y.place(relx=0.90,rely=0,relwidth=0.05,relheight=0.75)
text_w.configure(yscrollcommand=sb_y.set)

entered_txt=tk.StringVar()

etr=tk.Entry(master=frame,width=30,textvariable=entered_txt)
etr.bind('<Return>',send_msg)
etr.place(relx=0.05,rely=0.85,relwidth=0.65,relheight=0.1)

bt=tk.Button(master=frame,text="発言",bg="skyblue",command=send_msg)
bt.place(relx=0.75,rely=0.85,relwidth=0.20,relheight=0.1)

game=Gaister()

print_canvas()

HOST='127.0.0.1'
PORT=50010
BUFSIZE=4096

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

stocked_msg=[]

def listen():
    try:
        sock.connect((HOST,PORT))
        while True:
            r_read_sockets,w_ready_sockets,e_ready_sockets=select.select([sock],[],[])
            try:
                recev_msg=sock.recv(BUFSIZE).decode()
            except:
                break
            stock_msg(recev_msg)
    except Exception as e:
        print(e)
    finally:
        sock.close()
        receive_msg("サーバとの接続が切断されました")

check_msg()

thrd=threading.Thread(target=listen)
thrd.start()

root.mainloop()
