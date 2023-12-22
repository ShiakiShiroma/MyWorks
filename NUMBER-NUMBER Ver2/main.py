from mod_disp import *
from mod_thr_cnn import *
from tkinter import *
import threading 


if( __name__ == "__main__" ):

#変数を宣言
    
    #thread_testを作成＆開始
    cnn_thread = threading.Thread(target=thread_cnn_loop)
    cnn_thread.start()

    #GUIをタイトル画面にセット
    change_disp(0)

    #GUIを起動
    root.mainloop()

    #プログラムが正常終了したかどうか調べる。
    if( is_thread_end.is_set() ):
        #thread_testの終了を待つ
        cnn_thread.join()

    


    input("キー入力で終了します。")
    
    
