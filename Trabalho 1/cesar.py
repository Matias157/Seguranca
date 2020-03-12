import sys

algarismos = []
for i in range(65, 91):
        algarismos.append(chr(i))
for i in range(97, 123):
        algarismos.append(chr(i))
for i in range(48, 58):
        algarismos.append(chr(i))

def cesar(entrada, k):
        saida = []
        for letra in entrada:
                if(letra == ' ' or letra == "\n"):
                        saida.append(letra)
                else:
                        novonumero = algarismos.index(letra)
                        novonumero = (novonumero + k) % len(algarismos)
                        novaletra = algarismos[novonumero]
                        saida.append(novaletra)
        return("".join(saida))

def decifcesar(entrada, k):
        saida = []
        for letra in entrada:
                if(letra == ' ' or letra == "\n"):
                        saida.append(letra)
                else:
                        novonumero = algarismos.index(letra)
                        novonumero = (novonumero - k) % len(algarismos)
                        novaletra = algarismos[novonumero]
                        saida.append(novaletra)
        return("".join(saida))

def main():
        if(sys.argv[1] != "cesar" or (sys.argv[2] != "-c" and sys.argv[2] != "-d") or sys.argv[3] != "-k"):
                print("COMANDO INCORRETO!")
                #print(sys.argv[1])
                #print(sys.argv[2])
                #print(sys.argv[3])
                #print(sys.argv[4])
                #print(sys.argv[5])
                #print(sys.argv[6])
                return
        else:
                if(sys.argv[2] == "-c"):
                        fin = open(sys.argv[5], "r")
                        fout = open(sys.argv[6],"w+")
                        fout.write(cesar(fin.read(), int(sys.argv[4])))
                        fin.close()
                        fout.close()
                else:
                        fin = open(sys.argv[5], "r")
                        fout = open(sys.argv[6],"w+")
                        fout.write(decifcesar(fin.read(), int(sys.argv[4])))
                        fin.close()
                        fout.close()

if __name__ == "__main__":
    main()