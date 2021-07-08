import sys
from unidecode import unidecode

algarismos = []
for i in range(48, 58):
        algarismos.append(chr(i))
for i in range(65, 91):
        algarismos.append(chr(i))
for i in range(97, 123):
        algarismos.append(chr(i))

def analFreq(entrada):
    freq = [0] * len(algarismos)
    for letra in entrada:
        try:
            letra = chr(letra)
        except:
            pass
        try: 
            letra = unidecode(letra)
        except:
            pass
        print(letra, end="")
        if(letra == ' ' or letra == "\n" or letra == "." or letra == "," or letra == "?"):
            pass
        else:
            try:
                indice = algarismos.index(letra)
                freq[indice] += 1
            except:
                pass
    novoindice = freq.index(max(freq))
    chave = novoindice - algarismos.index("a")
    print("\ncaractere mais frequente: " + algarismos[novoindice])
    print("Chave encontrada: " + str(chave))

def main():
    try:
        fin = open(sys.argv[1], "r")
    except:
        print("ARQUIVO NAO EXISTE!")
        return
    try:
        texto = fin.read()
    except:
        fin.close()
        fin = open(sys.argv[1], "rb")
        texto = fin.read()
    analFreq(texto)
    fin.close()

if __name__ == "__main__":
    main()       