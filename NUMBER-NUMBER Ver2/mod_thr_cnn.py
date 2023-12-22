###########################################
'''
[説明]
mod_thr_cnn.pyはスレッドでソケット通信を行うプログラム

'''
###########################################

#ソケット通信の機能を取得
from mod_socket import *

#スレッドを作成する機能を取得
from threading import Thread

#スレッドのイベントを作成するのに使用している
import threading
import time

##GUIを操作する機能を取得
import mod_disp

#ゲームの機能を取得
import mod_game_control as mod_game

#スレッド間でデータの共有を行うためのQueueクラスを取得する。
import queue




def thread_cnn_loop():
    #許可が下りるまで待機
    event_socket_start.wait()

    #クライアントモードかサーバーモードか選ぶ
    mode = que_mode.get()

    
    #queueからIPアドレスとポート番号を取得
    ser_ip = que_addr.get()
    ser_port = que_addr.get()

    #相手と接続を試みる。
    try:
        #クライアントとして接続するとき
        if( mode == "client_mode"):
            my_cli = do_client(ser_ip,ser_port)

        #サーバーとして接続するとき
        elif( mode == "server_mode"):
            #PORT番号は33333とする。
            my_ser,my_cli,addr = do_server(33333)

        
        print("******************************************")
        print("通信成功")
        print("******************************************")
        event_socket_start2.set()
    except Exception as e:
        print("******************************************")
        print("エラーが発生しました。")
        print(e)
        print("******************************************")

        #エラーが発生したことをGUIに知らせる。
        event_error.set()
        event_socket_start2.set()

        #プログラムを終了する
        return

    time.sleep(1)

    #ルール説明をする。
    mod_disp.add_list("***NUMBER×NUMBERへようこそ！***")
    mod_disp.add_list("NUMBER×NUMBERは数当てゲームです！")
    mod_disp.add_list("交互に予想したデータを送りあい、相手の数字を当てたら勝ちです！")
    mod_disp.add_list("")
    mod_disp.add_list("++++ルール説明+++")
    mod_disp.add_list("・データの送受信は交互に行います。現在の順番は画面右に表示されます。")
    mod_disp.add_list("・あいての４桁の数字を当てることで勝利です")
    mod_disp.add_list("・送ったデータは以下のように返信されます")
    mod_disp.add_list("BLOW：数字は合っているが、桁の場所が違う数")
    mod_disp.add_list("HIT：数字も桁の場所が合っている数")
    mod_disp.add_list("")
    mod_disp.add_list("*******************************")

    if(mode == "client_mode"):

        print("GAME開始")

        #GUIにデータの受け渡しを許可する。(自分のターンにする。)
        is_your_turn.set()
        
        #GAME開始
        while(1):
            #例外処理
            try:
                
        ###########自分のターン############
                #GUIに現在の順番を表示する。
                mod_disp.add_list("")
                mod_disp.add_list("###じぶんのターン###")
                
                #排他制御    
                event_cnn.wait()
                event_cnn.clear()

                #キューからデータを受け取る。
                data_to_send = que_data.get()

                #データを送信する。
                send_data(my_cli,data_to_send)

                #送信内容を表示する。
                mod_disp.add_list("*送信した内容*")
                mod_disp.add_list(data_to_send)

                #処理結果データを受け取る。
                received_data = get_data(my_cli)

                #GAMEを続けるかどうかのデータを受け取る。
                Play_or_End = get_data(my_cli)

                #結果を表示する。
                mod_disp.add_list("*結果*")
                mod_disp.add_list(received_data)

                if(Play_or_End == "END" ):
                    print("GAMEに勝利しました。")
                    mod_disp.change_disp(100)    #勝利画面に移行する。
                    break
                
                
        ###########あいてのターン############

                #GUIに現在の順番を表示する。
                mod_disp.add_list("")
                mod_disp.add_list("###あいてのターン###")
                
                #データを受け取る。
                received_data = get_data(my_cli)

                #受け取ったデータを処理する(受信データと答えを比べる)
                result = mod_game.hit_or_blow(received_data,mod_game.ans)

                #GUIに文字を表示する。
                mod_disp.add_list("*あいてからの送信*")
                mod_disp.add_list(result)
                mod_disp.add_list("")

                #処理結果を相手に送信する。
                send_data(my_cli,result)

                #GAMEを続けるかどうか
                Play_or_End = que_still_play.get()
                send_data(my_cli,Play_or_End)
                
                if( Play_or_End == "END" ):
                    print("敗北しました。")
                    mod_disp.change_disp(200)
                    break

                #自分のターンに戻す。
                is_your_turn.set()
            
            except:
                print("接続が中断されました。")
                #エラー画面に遷移
                mod_disp.change_disp(999)
                break

    else:
        print("GAME開始")
        
        #GAME開始
        while(1):
            #例外処理
            try:                
        ###########あいてのターン############    

                #GUIに現在の順番を表示する。
                mod_disp.add_list("")
                mod_disp.add_list("###あいてのターン###")
                
                #データを受け取る。
                received_data = get_data(my_cli)

                #受け取ったデータを処理する(受信データと答えを比べる)
                result = mod_game.hit_or_blow(received_data,mod_game.ans)

                #GUIに文字を表示する。
                mod_disp.add_list("*あいてからの送信*")
                mod_disp.add_list(result)
                mod_disp.add_list("")

                #処理結果を相手に送信する。
                send_data(my_cli,result)

                #GAMEを続けるかどうか
                Play_or_End = que_still_play.get()
                send_data(my_cli,Play_or_End)

                if( Play_or_End == "END" ):
                    print("敗北しました。")
                    mod_disp.change_disp(200)
                    break
                
                #自分のターンに戻す。
                is_your_turn.set()

        ###########自分のターン############
                #GUIに現在の順番を表示する。
                mod_disp.add_list("")
                mod_disp.add_list("###じぶんのターン###")

                #排他制御    
                event_cnn.wait()
                event_cnn.clear()
                
                #キューからデータを受け取る。
                data_to_send = que_data.get()

                #データを送信する。
                send_data(my_cli,data_to_send)

                #送信内容を表示する。
                mod_disp.add_list("*送信した内容*")
                mod_disp.add_list(data_to_send)

                #処理結果データを受け取る。
                received_data = get_data(my_cli)

                #GAMEを続けるかどうかのデータを受け取る。
                Play_or_End = get_data(my_cli)


                #結果を表示する。
                mod_disp.add_list("*結果*")
                mod_disp.add_list(received_data)

                if(Play_or_End == "END" ):
                    print("GAMEに勝利しました。")
                    mod_disp.change_disp(100)    #勝利画面に移行する。
                    break

            except:
                print("接続が中断されました。")
                #エラー画面に遷移
                mod_disp.change_disp(999)
                break

    #threadが正常終了したことを知らせる。
    is_thread_end.set()

    #ソケットを閉じる
    if(mode == "client_mode"):
        close_connection(2,my_cli)
    elif(mode == "server_mode"):
        close_connection(1,my_cli,my_ser)
   


    
if(__name__!="__main__"):
    print("called as a module")

    #変数を宣言
    event_error = threading.Event() #エラー時に使用される。
    
    event_socket_start = threading.Event() #socket通信の開始
    
    event_socket_start2 = threading.Event() #socket通信の開始２

    event_cnn = threading.Event()   #データの送受信の同期

    is_your_turn = threading.Event()   #自分のターンかどうかを判別

    is_thread_end = threading.Event() #プログラムを途中終了したかどうか判別
    

    #スレッド間で共有する変数を保持するque_dataとque_cntを宣言。ゲームのデータを保存する。
    que_data = queue.Queue() #送受信するゲームデータを保持
    que_mode = queue.Queue() #サーバモードかクライアントモードか決めるデータを保持
    que_still_play = queue.Queue() #GAMEを終了するかどうかのデータを保持

    #IPアドレスとポート番号を格納
    que_addr = queue.Queue()
    
else:
    print("called as main")

    


    input("キー入力で終了します")
