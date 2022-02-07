import os
from git.cmd import Git
import msvcrt as m
from pygments import lex
import pygments.lexers
from pygments.token import Token as ParseToken
from os import system

mainPath = os.path.dirname(os.path.realpath(__file__))+"//"
progressionList = []
suppLangs = (((".py",".py3"),"#"),(".c",("//","/*")),(".cpp",("//","/*")))
def main():
    tags = []
    #Sprawdzenie czy istnieje plik z postępem czyszczenia repo
    if os.path.isfile(mainPath+"prg.prg"):
        print("Wykryto plik z postępem skryptu.")
        print("Naciśnij ENTER, aby go wczytać.")
        if m.getch().decode("ASCII") == "\r":
            progression = open(mainPath+"prg.prg")
            lines = progression.readlines()
            endOfTags = False
            for l in lines:
                if not endOfTags: 
                    if not l.strip()+"\n" == "\n":
                        input(l.strip())
                        tags.append(l.strip())
                    else:
                        endOfTags=True
                else:
                    if not l.strip() == "":
                        progressionList.append(l)
            progression.close()
        else:
            os.remove(mainPath+"prg.prg") 
    #Podanie tagów, jeśli nie zostały wczytane z pliku
    if tags == []:
        while(1):
            system("cls")
            inTag = input("Podaj tag komentarzy do usunięcia.\n")
            if not inTag.strip() == "":
                tags.append(inTag.strip())
                print("Naciśnij ENTER, aby dodać kolejny tag. Naciśnij dowolny inny klawisz, aby kontynować.")
                if not m.getch().decode("ASCII") == "\r":
                    system("cls")
                    break
                else:
                    continue
            input("Podaj niepusty tag. (białe znaki nie są uznawane)\n")
        f = open(mainPath+"prg.prg","w")
        for t in tags:
            f.write(t+"\n")
        if not progressionList == []:
            f.write("\n")
            for prog in progressionList:
                f.write(prog)
        f.close()
    #Stworzenie listy plików do wyczyszczenia
    g = Git(mainPath)
    files = g.ls_files().split("\n")
    #Czyszczenie kodu
    for f in files:
        notCleared=True
        for prg in progressionList:
            if f == prg.strip():
                notCleared=False
        if notCleared:
            filePath = mainPath+f
            for lang in suppLangs:
                if filePath.endswith(lang[0]):
                    print("Czyszczenie pliku "+f)
                    cT=[]
                    for cO in lang[1]:
                        for t in tags:
                            cT.append(cO+t)
                    if ".py" in lang[0]:
                        clearCode(filePath,pygments.lexers.get_lexer_by_name("py3"),cT)
                        continue
                    if ".cpp" in lang[0]:
                        clearCode(filePath,pygments.lexers.get_lexer_by_name("cpp"),cT)
                        continue
                    if ".c" in lang[0]:
                        clearCode(filePath,pygments.lexers.get_lexer_by_name("c"),cT)
                        continue
            appProg(f)
            system("cls")
    os.remove(mainPath+"prg.prg")
    print("Czyszczenie kodu w repozytorium zakończone")

def clearCode(f,lexer,cTag):
    file = open(f)
    content = file.read()
    file.close()
    generator = lex(content,lexer)
    line = []
    lines = []
    for token in generator:
        token_type = token[0]
        token_text = token[1]
        if token_type in ParseToken.Comment:  
            tagFound = False
            for cT in cTag:
                if(token_text.startswith(cT)):
                    tagFound = True
            if tagFound:
                continue
        if not token_text == '\n':
            line.append(token_text)
            tagFound = False
        if token_text == '\n':
            if (''.join(line).isspace() or line == []) and tagFound:
                tagFound = False
                line = []
                continue
            lines.append(''.join(line))
            line = []
    if line:
        lines.append(line)
    file = open(f,"w")
    fileLen = len(lines)-1
    for i, line in enumerate(lines):
        if i==fileLen:
            file.write(line)
        else:
            file.write(line+"\n")
    file.close()

def appProg(f):
    progressionList.append(f)
    prg = open(mainPath+"prg.prg","a")
    prg.write("\n"+f)
    prg.close()
    

if __name__ == "__main__":
    main()