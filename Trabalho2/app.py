import sys
import datetime
import hashlib
import csv
import pandas as pd

def generateToken(user):
    now = datetime.datetime.now()
    data = pd.read_csv("app_database.csv", index_col="user")
    seed = data.loc[user][0]
    seed = seed + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)
    token1 = hashlib.sha256(seed.encode()).hexdigest()
    token2 = hashlib.sha256(token1.encode()).hexdigest()
    token3 = hashlib.sha256(token2.encode()).hexdigest()
    token4 = hashlib.sha256(token3.encode()).hexdigest()
    token5 = hashlib.sha256(token4.encode()).hexdigest()
    tokenList = [token1[:6], token2[:6], token3[:6], token4[:6], token5[:6]]
    return(tokenList)

def verifyUser(user):
    col_list = ["user", "seed_password"]
    df = pd.read_csv("app_database.csv", usecols=col_list)
    for row in df["user"]:
        if(user == row):
            return(True)
    return(False)

def verifyToken(tokenList, token):
    validTokenFlag = False
    writeInvalidTokenFlag = False
    with open('invalidTokens') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        if(line == token):
            print("Token inválido ou já utilizado!!!")
            return(False)
    for item in tokenList:
        if(item == token):
            validTokenFlag = True
            writeInvalidTokenFlag = True
        if(writeInvalidTokenFlag == True):
            with open('invalidTokens', 'a+') as f:
                f.write("%s\n" % item)
    if(validTokenFlag == False):
        print("Token vencido ou incorreto!!!")
    return(validTokenFlag)


def main():
    inputUser = input("Informe seu usuário: ")
    inputPassw = input("Informe seu token de acesso: ")

    if(verifyUser(inputUser) == False):
        print("Usuário não encontrado!!!")
        return

    tokenList = generateToken(inputUser)
    if(verifyToken(tokenList, inputPassw) == True):
        print("Token válido!!!")

    return

if __name__ == "__main__":
    main()