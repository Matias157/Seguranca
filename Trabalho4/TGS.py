import socket
import pickle
import csv
import pandas as pd
import random
import string
import time
from pyDes import *

HOST = '127.0.0.1'
PORT = 65433
k_tgs = "9SWQCRSR"

def getServiceKey(service):
    data = pd.read_csv("TGS_service_database.csv", index_col="service")
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
                        M3 = pickle.loads(data)
                        print("M3 = " + str(M3))
                        ID_C = DESDecrypt(M3[1][0], k_tgs).decode()
                        T_R = DESDecrypt(M3[1][1], k_tgs).decode()
                        k_c_tgs = DESDecrypt(M3[1][2], k_tgs).decode()
                        ID_S = DESDecrypt(M3[0][1], k_c_tgs).decode()
                        N2 = DESDecrypt(M3[0][3], k_c_tgs).decode()
                        k_s = getServiceKey(ID_S)
                        k_c_s = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        T_A = str(time.time() + (int(T_R)*60))
                        if (int(T_R) > 30):
                            T_A = str(time.time() + (30*60))
                        M4 = [[DESEncrypt(k_c_s, k_c_tgs), DESEncrypt(T_A, k_c_tgs), DESEncrypt(N2, k_c_tgs)], [DESEncrypt(ID_C, k_s), DESEncrypt(T_A, k_s), DESEncrypt(k_c_s, k_s)]]
                        print("M4 = [[" + str(DESEncrypt(k_c_s, k_c_tgs)) + "(" + k_c_s + "), " + str(DESEncrypt(T_A, k_c_tgs)) + "(" + T_A + "), " + str(DESEncrypt(N2, k_c_tgs)) + "(" + N2 + ")], [" + str(DESEncrypt(ID_C, k_s)) + "(" + ID_C + "), " + str(DESEncrypt(T_A, k_s)) + "(" + T_A + "), " + str(DESEncrypt(k_c_s, k_s)) + "(" + k_c_s + ")]]")
                        sendData = pickle.dumps(M4)
                    conn.sendall(sendData)

if __name__ == "__main__":
    main()