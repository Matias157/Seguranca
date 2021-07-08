import sys
import datetime
import hashlib
import csv
import pandas as pd

def signUp(user, seed, password):
    with open('token_generator_database.csv', 'a+', newline='') as database:
        databasewriter = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        databasewriter.writerow([user, seed, password])
        return

def verifyUser(user):
    col_list = ["user", "seed_password", "password"]
    df = pd.read_csv("token_generator_database.csv", usecols=col_list)
    for row in df["user"]:
        if(user == row):
            return(True)
    return(False)

def sendDataToApp(user, seed):
    with open('app_database.csv', 'a+', newline='') as database:
        databasewriter = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        databasewriter.writerow([user, seed])
        return

def signIn(user, password):
    data = pd.read_csv("token_generator_database.csv", index_col="user")
    if(verifyUser(user) == True):
        if(data.loc[user][1] != password):
            return(False)
        else:
            return(True)
    else:
        return(False)

def generateToken(user):
    now = datetime.datetime.now()
    data = pd.read_csv("token_generator_database.csv", index_col="user")
    seed = data.loc[user][0]
    seed = seed + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)
    token1 = hashlib.sha256(seed.encode()).hexdigest()
    token2 = hashlib.sha256(token1.encode()).hexdigest()
    token3 = hashlib.sha256(token2.encode()).hexdigest()
    token4 = hashlib.sha256(token3.encode()).hexdigest()
    token5 = hashlib.sha256(token4.encode()).hexdigest()
    print("Tokens gerados em " + str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + " válidos até " + str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute + 1))
    print("Tokens: \n" + token1[:6] + "\n" + token2[:6] + "\n" + token3[:6] + "\n" + token4[:6] + "\n" + token5[:6])
    return

def main():
    print("-------------------------------------------")
    print("---------------------MENU------------------")
    print("-------------------------------------------")
    print("0 - Create User");
    print("1 - Generate Token");
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
            inputSeed = input("Crie uma senha semente: ")
            inputPassw = input("Crie sua senha, eu garanto que não vamos armazená-la ;): ")

            if(len(inputUser) == 0 or len(inputSeed) == 0 or len(inputPassw) == 0):
                print("Algum dos campos foi deixado em branco!")
                return

            if(inputUser == inputPassw or inputUser == inputSeed or inputSeed == inputPassw):
                print("Campos idênticos são inválidos!!!")
                return

            if(verifyUser(inputUser)):
                print("Nome de usuário indisponível!!!")
                return

            inputPassw = hashlib.sha256(inputPassw.encode()).hexdigest()
            inputSeed = hashlib.sha256(inputSeed.encode()).hexdigest()

            signUp(inputUser, inputSeed, inputPassw)
            sendDataToApp(inputUser, inputSeed)

            return

        elif(menu == '1'):
            inputUser = input("Informe seu usuário: ")
            inputPassw = input("Informe sua senha: ")

            inputPassw = hashlib.sha256(inputPassw.encode()).hexdigest()

            if(signIn(inputUser, inputPassw) == False):
                print("Usuário ou senha incorretos!!!")
                return

            print("-------------------------------------------")
            print("--------BEM VINDO " + inputUser + "--------")
            print("-------------------------------------------")
            print("0 - Generate Token");
            print("1 - Exit");
            print("-------------------------------------------")
            print("-------------------------------------------")
            print("-------------------------------------------")

            menu = input()
            if(menu != '0' and menu != '1'):
                return
            else:
                if(menu == '0'):
                    generateToken(inputUser)
                else:
                    return

            return
        else:
            return

if __name__ == "__main__":
    main()