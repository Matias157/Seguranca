import sys
from unidecode import unidecode

algarismos = []
for i in range(48, 58):
        algarismos.append(chr(i))
for i in range(65, 91):
        algarismos.append(chr(i))
for i in range(97, 123):
        algarismos.append(chr(i))

def vernam(entrada, k):
    saida = []
    for i in range(0, len(entrada)):
        letra = unidecode(entrada[i])
        if(letra == ' ' or letra == "\n" or letra == "." or letra == "," or letra == "?"):
            saida.append(letra)
        else:
            saida.append(algarismos[((algarismos.index(letra) + algarismos.index(k[i])) % len(algarismos))])
    return("".join(saida))

def decifvernam(entrada, k):
    saida = []
    for i in range(0, len(entrada)):
        letra = unidecode(entrada[i])
        if(letra == ' ' or letra == "\n" or letra == "." or letra == "," or letra == "?"):
            saida.append(letra)
        else:
            saida.append(algarismos[((algarismos.index(letra) - algarismos.index(k[i])) % len(algarismos))])
    return("".join(saida))

def main():
    if(sys.argv[1] != "vernam" or (sys.argv[2] != "-c" and sys.argv[2] != "-d")):
        print("COMANDO INCORRETO!")
        return
    else:
        try:
            chave = open(sys.argv[3], "r")
        except:
            print("CHAVE NAO ENCONTRADA!")
            return
        try:
            fin = open(sys.argv[4], "r")
        except:
            print("ARQUIVO NAO EXISTE!")
            return
        textoin = fin.read()
        textochave = chave.read() 
        if(sys.argv[2] == "-c"):
            if(len(textochave) != len(textoin)):
                print("CHAVE DEVE TER O MESMO TAMANHO DA MENSAGEM!")
                return
            fout = open(sys.argv[5],"w+")
            fout.write(vernam(textoin, textochave))
            fin.close()
            fout.close()
        else: 
            if(len(textochave) != len(textoin)):
                print("CHAVE DEVE TER O MESMO TAMANHO DA MENSAGEM!")
                return
            fin = open(sys.argv[4], "r")
            fout = open(sys.argv[5],"w+")
            fout.write(decifvernam(textoin, textochave))
            fin.close()
            fout.close()

if __name__ == "__main__":
    main()

