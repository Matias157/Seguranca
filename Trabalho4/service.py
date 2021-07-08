import socket
import pickle
import csv
import pandas as pd
import random
import string
import time
from pyDes import *

HOST = '127.0.0.1'
PORT = 65434
k_s = "1TXRDSTS"

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
                        M5 = pickle.loads(data)
                        print("M5 = " + str(M5))
                        ID_C = DESDecrypt(M5[1][0], k_s).decode()
                        T_A = DESDecrypt(M5[1][1], k_s).decode()
                        k_c_s = DESDecrypt(M5[1][2], k_s).decode()
                        S_R = DESDecrypt(M5[0][2], k_c_s).decode()
                        N3 = DESDecrypt(M5[0][3], k_c_s).decode()
                        if (S_R == "0"):
                            answer = "-------------------------------------------\n---------Welcome " + ID_C + "---------\n-------------------------------------------\n1 - Check Balance\n2 - Exit\n-------------------------------------------\n-------------------------------------------\n-------------------------------------------"
                        elif (S_R == "1"):
                            answer = "------US$ 500,00------"
                        elif (S_R == "2"):
                            answer = "end"
                        else:
                            answer = "INVALID INPUT!!!!\n-------------------------------------------\n---------Welcome " + ID_C + "---------\n-------------------------------------------\n1 - Check Balance\n2 - Exit\n-------------------------------------------\n-------------------------------------------\n-------------------------------------------"
                        if (time.time() > float(T_A)):
                            answer = "timeout"
                        M6 = [DESEncrypt(answer, k_c_s), DESEncrypt(N3, k_c_s)]
                        print("M6 = [" + str(DESEncrypt(answer, k_c_s)) + "(" + answer + "), " + str(DESEncrypt(N3, k_c_s)) + "(" + N3 + ")]")
                        sendData = pickle.dumps(M6)
                    conn.sendall(sendData)

if __name__ == "__main__":
    main()