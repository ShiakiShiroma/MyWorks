# tkinterのインポート
from tkinter import *
from tkinter import scrolledtext
from mod_game_control import *
from mod_thr_cnn import *
import time
###########################################
'''
[説明]
mod_disp.pyはGUIを操作するモジュール

'''
###########################################

#タイトル画面
def disp0(frame,old_frame):
    ##ウィジェットのサイズ
    global button_width
    global button_height
    
    print("disp0:タイトル画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # メインフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_frame = Label(new_frame, text="タイトル画面")
    button_change = Button(new_frame, text="メニュー画面へ", command=lambda:change_disp(1),width=button_width,height=button_height)

    # 各種ウィジェットの設置
    label1_frame.pack()
    button_change.pack()

    ###新しいフレームを返す
    return new_frame



#メニュー画面
def disp1(frame,old_frame):
    ##ウィジェットのサイズ
    global button_width
    global button_height
    
    print("disp1:メニュー画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_new_frame = Label(new_frame, text="メニュー画面")
    button_change_disp0 = Button(new_frame, text="タイトル画面へ", command=lambda:change_disp(0),width=button_width,height=button_height)
    button_change_disp2 = Button(new_frame, text="接続画面(サーバ)へ", command=lambda:change_disp(2),width=button_width,height=button_height)
    button_change_disp3 = Button(new_frame, text="接続画面(クライアント)へ", command=lambda:change_disp(3),width=button_width,height=button_height)

    # 各種ウィジェットの設置
    label1_new_frame.pack()
    button_change_disp0.pack()
    button_change_disp2.pack()
    button_change_disp3.pack()

    ###新しいフレームを返す
    return new_frame




#接続画面(サーバ)
def disp2(frame,old_frame):
    ##ウィジェットのサイズ
    global button_width
    global button_height
    
    print("disp2:サーバ画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)


    label1_new_frame = Label(new_frame, text="クライアントからの接続を待っています。")
    label2_new_frame = Label(new_frame, text="ポート番号：33333")
    button_change_disp0 = Button(new_frame, text="タイトル画面へ", command=lambda:change_disp(0),width=button_width,height=button_height)

    label1_new_frame.pack()
    label2_new_frame.pack()
    button_change_disp0.pack()    

    return new_frame




#接続画面(クライアント)
def disp3(frame,old_frame):
    
    ##ウィジェットのサイズ
    global button_width
    global button_height
    
    print("disp3:クライアント画面")

    ###古いフレームを削除する
    old_frame.destroy()   
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH)

    # アドレスとポート番号のフレームをまとめるフレーム
    ad_prt_frame = Frame(new_frame)
    ad_prt_frame.pack()

    #ラベルと入力欄を扱うフレーム(IPアドレス)
    frame_address = Frame(ad_prt_frame)
    vc_ip = frame_address.register(limit_ip)#文字数を制限するプログラム
    lab_address = Label(frame_address, text="IPアドレス")
    entry_address = Entry(frame_address, validate="key", validatecommand=(vc_ip, "%P"),width=16,font=("Helvetica",28))

    lab_address.pack(side=LEFT)
    entry_address.pack(side=LEFT)
    frame_address.pack(side=LEFT)

    #ラベルと入力欄を扱うフレーム(ポート番号)
    frame_port = Frame(ad_prt_frame)
    vc_port = frame_port.register(limit_port)#文字数を制限するプログラム
    lab_port = Label(frame_port, text="ポート番号")
    entry_port = Entry(frame_port, validate="key", validatecommand=(vc_port, "%P"),width=16,font=("Helvetica",28))

    lab_port.pack(side=LEFT)
    entry_port.pack(side=LEFT)
    frame_port.pack(side=LEFT)

    #画面遷移するボタン
    frame_btn = Frame(new_frame)    
    button_change_disp5 = Button(frame_btn, text="接続待機画面へ", command=lambda:change_disp(5,entry_address.get(),entry_port.get()),width=button_width,height=button_height)
    button_change_disp0 = Button(frame_btn, text="タイトル画面へ", command=lambda:change_disp(0),width=button_width,height=button_height)
    
    button_change_disp5.pack(anchor=S)
    button_change_disp0.pack(anchor=S)
    frame_btn.pack()    

    return new_frame

##ゲーム画面
def disp4(frame,old_frame):
    #答え
    global ans
    
    print("disp4:ゲーム画面")

    ##メインで宣言したentry_listを特別に呼び出す。
    global entry_list
    
    ###古いフレームを削除する
    old_frame.destroy()
    
    #大フレームを作成
    frm0    = Frame(frame)
    frm0.pack()



    #左フレームを作成
    frm1    = Frame(frm0,bg="green")        #中フレームを使って小フレームをまとめる。
    frm1.pack(side=LEFT )

    frm1_1    = Frame(frm1)        #フレームを使ってラベルとテキストボックスをまとめる
    frm1_1.pack()

    frm1_2    = Frame(frm1)        #フレームを使ってラベルとテキストボックスをまとめる
    frm1_2.pack()

    lab0    = Label(frm1_1,text="じぶんのこたえ：{0} \n".format(ans),font=("Helvetica",20))
    lab0.pack(anchor=NE )

    lab1    = Label(frm1_1,text="数字を入力してください",font=("Helvetica",20))
    lab1.pack(side=LEFT)

    vc = frm1_2.register(limit_char)#文字数を制限するプログラム

    ent1 = Entry(frm1_2, validate="key", validatecommand=(vc, "%P"),width=4,font=("Helvetica",28))
    ent1.pack(side=LEFT)

    but1     = Button(frm1_2,text="Play",command=lambda:game_controller(str( ent1.get() )),width=12,height=2)
    but1.pack(side=LEFT)

    #右フレームを作成
    frm2    = Frame(frm0,bg='blue')        #フレームを使ってラベルとテキストボックスをまとめる
    frm2.pack(side=RIGHT)


    entry_list    = scrolledtext.ScrolledText(frm2,font=("Helvetica",16))
    entry_list.configure(state='disabled')      #テキストボックスを入力不可にする
    entry_list.pack(expand=True)

    entry_list.update()

    return frm0

#接続待機画面
def disp5(frame,old_frame):
    ##ウィジェットのサイズ

    
    print("disp5:接続待機画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_new_frame = Label(new_frame, text="サーバへ接続しています。")
    
    # 各種ウィジェットの設置
    label1_new_frame.pack()   

    ###新しいフレームを返す
    return new_frame

#エラー画面
def disp_error(frame,old_frame):
    ##ウィジェットのサイズ

    
    print("disp_error:エラー画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_new_frame = Label(new_frame, text="エラーが発生しました。")
    label2_new_frame = Label(new_frame, text="ゲームを終了してください。")
    
    # 各種ウィジェットの設置
    label1_new_frame.pack()
    label2_new_frame.pack()

    ###新しいフレームを返す
    return new_frame

#勝利画面
def disp_WIN(frame,old_frame):
    ##ウィジェットのサイズ

    
    print("disp_WIN:勝利画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_new_frame = Label(new_frame, text="おめでとうございます！ゲームに勝利しました！！")
    label2_new_frame = Label(new_frame, text="ゲームを終了してください。")
    
    # 各種ウィジェットの設置
    label1_new_frame.pack()
    label2_new_frame.pack()

    ###新しいフレームを返す
    return new_frame


#敗北画面
def disp_LOSE(frame,old_frame):
    ##ウィジェットのサイズ

    
    print("disp_LOSE:敗北画面")

    ###古いフレームを削除する
    old_frame.destroy()
    
    # 新しいフレームの作成と設置
    new_frame = Frame(frame)
    new_frame.pack(fill = BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_new_frame = Label(new_frame, text="残念ながら負けてしまいました...")
    label2_new_frame = Label(new_frame, text="ゲームを終了してください。")
    
    # 各種ウィジェットの設置
    label1_new_frame.pack()
    label2_new_frame.pack()

    ###新しいフレームを返す
    return new_frame


##文字数を制限するプログラム
def limit_char(string):
    return len(string) <= 4

##文字数(IPアドレス)を制限するプログラム
def limit_ip(string):
    return len(string) <= 15

##文字数(PORT番号)を制限するプログラム
def limit_port(string):
    return len(string) <= 6

#disp4内でのみ使用する。
#stringをlistに追加する
def add_list(string):
    global entry_list       #disp4で宣言
    global num_line         #このモジュール内のメインで宣言
    
    num_line = num_line + 1.0

    entry_list.configure(state='normal')            #テキストボックスを入力不可にする
    entry_list.insert(num_line ,"\n"+str(string))#テキストボックスに文字を追加
    entry_list.configure(state='disabled')          #テキストボックスを入力不可にする
    entry_list.see("end")                           #テキストの最後の列を表示する
    entry_list.update()                             #即座に画面に表示する。


#画面を変更する
def change_disp(num_disp,ip=None,port=None):
    global base_frame
    global main_frame

    
    #タイトル画面に遷移する。
    if( num_disp == 0 ):
        main_frame = disp0(base_frame,main_frame)

    #メニュー画面に遷移する。
    elif( num_disp == 1 ):
        main_frame = disp1(base_frame,main_frame)

    #接続画面(サーバ)に遷移する。
    elif( num_disp == 2 ):
        
        #queueにIPアドレスとポート番号,クライアントモードを格納
        que_mode.put("server_mode")
        que_addr.put(None)
        que_addr.put(None)
        event_socket_start.set()
        main_frame = disp2(base_frame,main_frame)
        main_frame.update()

        event_socket_start2.wait()      #threadからの合図を待つ

        if(event_error.is_set()):
            #エラー画面へ遷移する。
            change_disp(999)
        else:
            #ゲーム画面へ遷移する。
            change_disp(4)

    #接続画面(クライアント)に遷移する。
    elif( num_disp == 3 ):
        main_frame = disp3(base_frame,main_frame)

    #接続画面(クライアント)に遷移する。
    elif( num_disp == 4 ):
        main_frame = disp4(base_frame,main_frame)

    #接続待機画面に遷移する。
    elif( num_disp == 5 ):
        #queueにIPアドレスとポート番号,クライアントモードを格納
        que_mode.put("client_mode")
        que_addr.put(ip)
        que_addr.put(port)
        event_socket_start.set()
        main_frame = disp5(base_frame,main_frame)
        main_frame.update()

        event_socket_start2.wait()      #threadからの合図を待つ

        if(event_error.is_set()):
            #エラー画面へ遷移する。
            change_disp(999)
        else:
            #ゲーム画面へ遷移する。
            change_disp(4)

    elif(num_disp==100):
        main_frame = disp_WIN(base_frame,main_frame)

    elif(num_disp==200):
        main_frame = disp_LOSE(base_frame,main_frame)

    #エラー画面に遷移する。
    else:
        
        main_frame = disp_error(base_frame,main_frame)

        
#モジュールとして呼び出された時の処理
if __name__ != "__main__":

################パラメータや変数宣言#########################

    button_width = 18
    button_height = 3
    
    # rootメインウィンドウの設定
    root = Tk()
    root.title("tkinter application")
    root.geometry("800x600")

    # 基盤フレームの作成と設置
    base_frame = Frame(root)
    base_frame.pack(fill = BOTH, pady=20)

    #mainフレームを作成、change_disp()内でのみmain_frameをグローバル変数として呼び出す。
    main_frame = Frame(base_frame)
    main_frame.update()
    main_frame.pack()
    
    #リストに文字を追加するときに使用する。
    entry_list = ""
    num_line = 1.0

#メインとして起動したときの処理
else:

    # rootメインウィンドウの設定
    root = Tk()
    root.title("tkinter application")
    root.geometry("800x600")
    root.resizable(width=False,height=False)

    # 基盤フレームの作成と設置
    base_frame = Frame(root)
    base_frame.pack(fill = BOTH, pady=20)

    #mainフレームを作成、change_disp()内でのみmain_frameをグローバル変数として呼び出す。
    main_frame = Frame(base_frame)
    main_frame.update()
    main_frame.pack()

    change_disp(1)
    
    root.mainloop()


