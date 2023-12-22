import socket

###########################################
'''
[説明]
mod_socket.pyはソケット通信を行うモジュール

'''
###########################################



####接続を開始する
def start_connection(select):

    if(select==1):
        port = 50000
        #サーバとして接続を行う
        print("サーバーとして機能します")
        host = socket.gethostname()     #サーバのホスト名を取得する
        ip = socket.gethostbyname(host) #サーバのIPアドレスを取得する
        print("サーバのIPアドレス:"+str(ip))
        print("サーバのポート番号:"+str(port))
        ser,cli,addr = do_server(port)
        
    elif(select==2):
        #クライアントとして接続を行う
        print("クライアントとして機能します")
        ser_addr = input("サーバのIPアドレスを記入してください：")
        ser_port = input("サーバのポート番号を記入してください：")
        ser = None
        addr = None
        cli = do_client(ser_addr,ser_port)

    else:
        #不正なデータ
        print("クライアントとして機能します")
        ser,cli,addr = None

    return ser,cli,addr

def do_server(port):

    PORT = port
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("",PORT))
    server.listen()

    client, addr = server.accept()

    return server , client , addr

def do_client(ser_ip,ser_port):
    HOST = ser_ip
    PORT = int(ser_port)

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))

    return client

####データを受信する    
def get_data(client):
    data = client.recv(4096)

    dec_data = data.decode("UTF-8")

    return dec_data

####データを送信する
def send_data(client,data):
    enc_data = bytes(data,'UTF-8')
    
    client.send(enc_data)


####接続を終了する
def close_connection(select,client,server=None):
    if(select==1):
        #サーバとして接続を終了する
        server.close()
        client.close()
        
    elif(select==2):
        #クライアントとして接続を行う
        client.close()




#モジュールとして呼び出されたときの処理
if(__name__ != "__main__" ):
    print("hi, this is mod_socket")
##    my_cli = ""         #クライアントのソケット
##    my_ser = ""         #サーバのソケット
##    addr = ""           #クライアント情報
    
#メインとして動作しているときの処理
else:
    print("called as main program")
