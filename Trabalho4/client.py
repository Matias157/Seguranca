import sys
import hashlib
import socket
import pickle
import csv
import pandas as pd
import random
import string
import time as tm
from pyDes import *

HOST = '127.0.0.1'
PORT_AS = 65432
PORT_TGS = 65433
PORT_SERVICE = 65434

def signUp(user, password):
    with open('client_database.csv', 'a+', newline='') as database:
        databasewriter = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        databasewriter.writerow([user, password])
        return

def verifyUser(user):
    col_list = ["user", "password"]
    df = pd.read_csv("client_database.csv", usecols=col_list)
    for row in df["user"]:
        if(user == row):
            return(True)
    return(False)

def sendDataToAS(user, password):
    with open('AS_client_database.csv', 'a+', newline='') as database:
        databasewriter = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        databasewriter.writerow([user, password])
        return

def signIn(user, password):
    data = pd.read_csv("client_database.csv", index_col="user")
    if(verifyUser(user) == True):
        if(data.loc[user][0] != password):
            return(False)
        else:
            return(True)
    else:
        return(False)

def DESEncrypt(text, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(text)
    return(d)

def DESDecrypt(text, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.decrypt(text)
    return(d)

def main():
    print("-------------------------------------------")
    print("---------------------MENU------------------")
    print("-------------------------------------------")
    print("0 - Create User");
    print("1 - Access Services");
    print("2 - Exit");
    print("-------------------------------------------")
    print("-------------------------------------------")
    print("-------------------------------------------")

    menu = input()
    if(menu != '0' and menu != '1' and menu != '2'):
        return
    else:
        if(menu == '0'):
            inputUser = input("Crie seu usuário: ")
            inputPassw = input("Crie sua senha: ")

            if(len(inputUser) == 0 or len(inputPassw) == 0):
                print("Algum dos campos foi deixado em branco!")
                return

            if(inputUser == inputPassw):
                print("Campos idênticos são inválidos!!!")
                return

            if(verifyUser(inputUser)):
                print("Nome de usuário indisponível!!!")
                return

            inputPassw = hashlib.sha256(inputPassw.encode()).hexdigest()
            userKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            signUp(inputUser, userKey, inputPassw)
            sendDataToAS(inputUser, userKey)

            return

        elif(menu == '1'):
            inputUser = input("Informe seu usuário: ")
            inputPassw = input("Informe sua senha: ")

            inputPassw = hashlib.sha256(inputPassw.encode()).hexdigest()

            if(signIn(inputUser, inputPassw) == False):
                print("Usuário ou senha incorretos!!!")
                return

            print("-------------------------------------------")
            print("---------Welcome " + inputUser + "---------")
            print("-------------------------------------------")
            print("0 - Online Banking Services");
            print("1 - Exit");
            print("-------------------------------------------")
            print("-------------------------------------------")
            print("-------------------------------------------")

            menu = input()
            if(menu != '0' and menu != '1'):
                return
            else:
                if(menu == '0'):
                    print("Inform the required time of your session in minutes")
                    time = input()
                    try:
                        temp = int(time)
                    except ValueError:
                        print("Please inform a valid time")
                        return
                    key = inputPassw[:8]
                    print(key)
                    ID_C = inputUser
                    ID_S = "OB1"
                    T_R = time
                    N1 = str(random.randrange(100))
                    M1 = [ID_C, [DESEncrypt(ID_S, key), DESEncrypt(T_R, key), DESEncrypt(N1, key)]]
                    print("M1 = [" + ID_C + ", [" + str(DESEncrypt(ID_S, key)) + "(" + ID_S + "), " + str(DESEncrypt(T_R, key)) + "(" + T_R + "), " + str(DESEncrypt(N1, key)) + "(" + N1 + ")]]")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, PORT_AS))
                        sendData = pickle.dumps(M1)
                        s.sendall(sendData)
                        M2 = s.recv(1024)
                        M2 = pickle.loads(M2)
                    if (DESDecrypt(M2[0][1], key).decode() != N1):
                        print("Different random numbers!!!")
                        return
                    print("M2 = " + str(M2))
                    k_c_tgs = DESDecrypt(M2[0][0], key).decode()
                    N2 = str(random.randrange(100))
                    M3 = [[DESEncrypt(ID_C, k_c_tgs), DESEncrypt(ID_S, k_c_tgs), DESEncrypt(T_R, k_c_tgs), DESEncrypt(N2, k_c_tgs)], [M2[1][0], M2[1][1], M2[1][2]]]
                    print("M3 = [[" + str(DESEncrypt(ID_C, k_c_tgs)) + "(" + ID_C + "), " + str(DESEncrypt(ID_S, k_c_tgs)) + "(" + ID_S + "), " + str(DESEncrypt(T_R, k_c_tgs)) + "(" + T_R + "), " + str(DESEncrypt(N2, k_c_tgs)) + "(" + N2 + ")], [" + str(M2[1][0]) + ", " + str(M2[1][1]) + ", " + str(M2[1][2]) + "]]")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, PORT_TGS))
                        sendData = pickle.dumps(M3)
                        s.sendall(sendData)
                        M4 = s.recv(1024)
                        M4 = pickle.loads(M4)
                    if (DESDecrypt(M4[0][2], k_c_tgs).decode() != N2):
                        print("Different random numbers!!!")
                        return
                    print("M4 = " + str(M4))
                    k_c_s = DESDecrypt(M4[0][0], k_c_tgs).decode()
                    T_A = DESDecrypt(M4[0][1], k_c_tgs).decode()
                    S_R = "0"
                    print("Your session will end at " + tm.ctime(float(T_A)))
                    answer = ""
                    while(True):
                        N3 = str(random.randrange(100))
                        M5 = [[DESEncrypt(ID_C, k_c_s), DESEncrypt(T_A, k_c_s), DESEncrypt(S_R, k_c_s), DESEncrypt(N3, k_c_s)], [M4[1][0], M4[1][1], M4[1][2]]]
                        #print("M5 = [[" + str(DESEncrypt(ID_C, k_c_s)) + "(" + ID_C + "), " + str(DESEncrypt(T_A, k_c_s)) + "(" + T_A + "), " + str(DESEncrypt(S_R, k_c_s)) + "(" + S_R + "), " + str(DESEncrypt(N3, k_c_s)) + "(" + N3 + ")], [" + str(M4[1][0]) + ", " + str(M4[1][1]) + ", " + str(M4[1][2]) + "]]")
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT_SERVICE))
                            sendData = pickle.dumps(M5)
                            s.sendall(sendData)
                            M6 = s.recv(1024)
                            M6 = pickle.loads(M6)
                        if (DESDecrypt(M6[1], k_c_s).decode() != N3):
                            print("Different random numbers!!!")
                            return
                        answer = DESDecrypt(M6[0], k_c_s).decode()
                        if (answer == "end"):
                            print("------Session ended------")
                            break
                        if (answer == "timeout"):
                            print("------Session timed out------")
                            break
                        print(answer)
                        S_R = input()
                else:
                    return

            return
        else:
            return

if __name__ == "__main__":
    main()