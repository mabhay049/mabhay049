import tkinter as tk
import urllib3
from tkinter import *

root = tk.Tk()
root.geometry("450x450+500+300")
root.title("SECURE_CHECK")

welcomeLabel = tk.Label(text="SECURE_CHECK").pack()
startLabel = tk.Label(text='FIRST UPDATE THEN  START CHECKING ').pack()

def HASHCHECK():
    global Answer
    with open("hash_removed25.txt", "r") as doc:
        fr1 = doc.read()
        input_stream_lines = (fr1).split()
    Answer = input_stream_lines

    tk.Label(text="INPUT HASH").place(x=150, y=225)
    global myAnswer
    myAnswer = Entry()
    myAnswer.place(x=300, y=225)

def checkAnswer():
    entry = myAnswer.get()
    c = 0
    for j in Answer:
        if j == entry.lower():
            c = c + 1
        else:
            pass
    if c == 0:
        tk.Label(text="NOT INFECTED").pack()
    else:
        tk.Label(text="INFECTED").pack()

def INUPDT():
    tk.Label(text="RANGE_START").place(x=150, y=100)
    global entry1
    entry1 = Entry()
    entry1.place(x=300, y=100)

    tk.Label(text="RANGE_END").place(x=150, y=125)
    global entry2
    entry2 = Entry()
    entry2.place(x=300, y=125)

def UPDATE():
    no1 = int(entry1.get())
    no2 = int(entry2.get())
    for i in range(no1, no2):
        fileNumber = '%05d' % i
        url = ('https://virusshare.com/hashes/VirusShare_%s.md5') % (fileNumber)
        #print(url)
        http1 = urllib3.PoolManager()
        HTML1 = http1.request('GET', url)  # make requests to website
        with open('recent10.txt', 'ab')as fr:
            fr.write(HTML1.data)
            fr.close()
        try:
            file = open('recent10.txt', 'r')
            output_stream = []
            input_stream_lines = (file.read()).split("\n")
            for line in input_stream_lines:
                if "#" in line:
                    pass
                else:
                    output_stream.append(line)
            with open("hash_removed25.txt", "a+") as wr:
                # wr.write("\n")
                wr.writelines("%s\n" % i for i in output_stream)
        except IOError:
            print('\033[91m' + "Error: can\'t find file or read data." + '\033[0m')
            exit(0)
        else:
            print('\x1b[6;30;42m' + "Unused charactors removed succesfully!!!\n" + '\x1b[0m')
    tk.Label(text="UPDATED").pack()

def INCLR():
    tk.Label(text="OLD FILEs NAME:\n recent10.txt & \nhash_removed25.txt").place(x=150, y=300)
    global entry3
    entry3 = Entry()
    entry3.place(x = 300, y = 300)

def CLEAR():
    with open((entry3.get()).lower(), "w")as cl:
        cl.write("")
        cl.close()
    tk.Label(text="CLEAR").pack()

def HIW():
    t = Tk()
    w = Label(t, text="First step is Updating \n 1.choose the range (for testing)\n 2. diffrence between range not be more than One. \n 3. the range between 1-374.\n"
                         "\nSecond step for testing choose md5hash\n 1.Double click on any entry in recent10.txt file \n \nThird step is you can clear any file\n 1.Give input as file name \n2.Then Click CLEAR button\n \n")
    w.pack()

    t.mainloop()

HASHBtn = tk.Button(text="INPUT", command=HASHCHECK).place(x = 25, y = 200)
checkBtn = tk.Button(text="CHECK HASH", command=checkAnswer).place(x=300, y = 250)
INPUT4Btn = tk.Button(text="INPUT RANGE", command=INUPDT).place(x = 25, y = 100)
updateBtn = tk.Button(text="UPDATE HASH TABLE", command=UPDATE).place(x=300, y = 150)
INPUT3Btn = tk.Button(text="INPUT FILE", command=INCLR).place(x = 25, y = 300)
CLEARBtn = tk.Button(text="CLEAR HASH FILE", command=CLEAR).place(x=300, y = 350)
HIWBtn = tk.Button(text="HOW IT WORKS", command=HIW).place(x=300, y = 60)

tk.mainloop()

