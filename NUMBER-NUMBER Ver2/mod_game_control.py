import random
from mod_socket import *
#from mod_disp import *
import mod_disp
from mod_thr_cnn import *
###########################################
'''
[説明]
mod_game_control.pyはゲームの機能を記述したモジュール

'''
###########################################


#ゲームを操作する
def game_controller(data_to_send):
    global is_your_turn
    

    if(is_your_turn.is_set() == True):

        #送信内容を調べる。
        if(len(data_to_send) < 4 or data_to_send.isdigit() == False):
            mod_disp.add_list(data_to_send + " : 再入力してください")
            return
        
        #送信内容の確認
        mod_disp.add_list(data_to_send+"を送信します。")
        
        #フラグをクリアにする。
        is_your_turn.clear()
        
        #threadにデータを渡す。
        que_data.put(data_to_send)

        #threadにデータの送信を許可する。
        event_cnn.set()
        
    else:
        mod_disp.add_list("あいてのターンです。")
    


#引数numがhitもしくはblowなのかを判定する。
def hit_or_blow(num,ans):

    #for文を使って一つずつ数字があっているか確かめるために、引数num,ansをリスト型に直している。
    numi = list(num)
    answer = list(ans)
    result = ""
    count_blow = 0
    count_hit = 0
    
    #------------------------------判定部(HIT判定)---------------------------------#
    for i in range(0,4):
        if(num[i] == str(answer[i]) ):#入力した数が乱数と一致しているかどうか調べる
            count_hit = count_hit+1
            answer[i] = -2
    #------------------------------判定部(BLOW判定)---------------------------------#
    for i in range(0,4):
        for j in range(0,4):
            #print("{0} : {1}".format(int(inp[i]),j))
            if(numi[i] == str(answer[j]) and not i == j):#入力した数が乱数と一致しているかどうか調べる
                count_blow = count_blow+1
                numi[i] = "a"
                answer[j] = -2
    #------------------------------出力部---------------------------------#
    result = num +"  →  HIT:" + str(count_hit) + " , BLOW:" + str(count_blow)

    #終了判定をする
    if( count_hit == 4 ):
        que_still_play.put("END")
    else:
        que_still_play.put("PLAYING")
    
    return result



def create_rand_num():
    #ランダムな４桁の数rand_numを生成する。
    gen_rand=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(gen_rand)
    rand_num = gen_rand[0:4]

    #整数(配列)→文字列に変換して答えansを生成する。
    ans = ""
    
    #整数(配列)を文字列に変換
    for z in range(0,4):
                ans = ans + str(rand_num[z])
    return ans




if(__name__ != "__main__"):
    print("hello world")

    #ランダムな４桁の数rand_numを生成する。
    gen_rand=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(gen_rand)
    rand_num = gen_rand[0:4]

    #整数(配列)→文字列に変換して答えansを生成する。
    ans = ""
    
    #整数(配列)を文字列に変換
    for z in range(0,4):
                ans = ans + str(rand_num[z])

    
    
else:
    print("HELLO WORLD")
    while(1):

        inp = input("１を入力:")
        if( inp != "1" ):
            break

        ans = create_rand_num()
        guess = create_rand_num()
        
        print(ans)
        print(guess)

        print(hit_or_blow(guess,ans))

        












