import socket
import pickle
import csv
import pandas as pd
import random
import string
from pyDes import *

HOST = '127.0.0.1'
PORT = 65432

def getUserPassword(user):
    data = pd.read_csv("AS_client_database.csv", index_col="user")
    return (data.loc[user][0])

def getTGSKey(service):
    data = pd.read_csv("AS_TGS_database.csv", index_col="service")
    return (data.loc[service][0])

def DESEncrypt(text, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(text)
    return(d)

def DESDecrypt(text, key):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.decrypt(text)
    return(d)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        M1 = pickle.loads(data)
                        print("M1 = " + str(M1))
                        k_c = getUserPassword(M1[0])[:8]
                        print(k_c)
                        ID_S = DESDecrypt(M1[1][0], k_c).decode()
                        T_R = DESDecrypt(M1[1][1], k_c).decode()
                        N1 = DESDecrypt(M1[1][2], k_c).decode()
                        k_tgs = getTGSKey(ID_S)
                        k_c_tgs = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        M2 = [[DESEncrypt(k_c_tgs, k_c), DESEncrypt(N1, k_c)], [DESEncrypt(M1[0], k_tgs), DESEncrypt(T_R, k_tgs), DESEncrypt(k_c_tgs, k_tgs)]]
                        print("M2 = [[" + str(DESEncrypt(k_c_tgs, k_c)) + "(" + k_c_tgs + "), " + str(DESEncrypt(N1, k_c)) + "(" + N1 + ")], [" + str(DESEncrypt(M1[0], k_tgs)) + "(" + M1[0] + "), " + str(DESEncrypt(T_R, k_tgs)) + "(" + T_R + "), " + str(DESEncrypt(k_c_tgs, k_tgs)) + "(" + k_c_tgs + ")]]")
                        sendData = pickle.dumps(M2)
                    conn.sendall(sendData)

if __name__ == "__main__":
    main()