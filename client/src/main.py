import socket
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import ntpath
import subprocess


choice = 0
fullPath = ""
currentUrl = ""
currentip = ""



def pdfSend(filePath, ip):
    print("\n")
    print(ip)
    print("\n")
    if filePath == ("/") or ip == "":
        return ""
    SERVER_IP = (ip, 3031)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(SERVER_IP)
    data = client.recv(1024).decode()
    print(f"From server: {data}")
    client.send(f"1{ntpath.basename(filePath)}".encode())                                       #1 in front to tell the server it is an upload request
    url = client.recv(1024).decode()
    pdf = open(filePath, "rb")
    send = pdf.read(1024)
    while send:
        client.send(send)
        print("sending...")
        send = pdf.read(1024)
    choix = 0
    return url



window = tk.Tk()

def browseFiles():
    global fullPath
    fileToSend.set(filedialog.askopenfilename(initialdir = "/Users", title = "Select a File", filetypes = (("pdf files", "*.pdf"),("all files", "*.*"))))
    fullPath = fileToSend.get()
    fileToSend.set(ntpath.basename(fullPath))

def sendButton(filePath):
    global currentUrl
    urlDisplayVar.set(pdfSend(fullPath, currentip))
    currentUrl = urlDisplayVar.get()

def copyUrl():
    subprocess.run("pbcopy", text=True, input=currentUrl)

def ipSave():
    global currentip
    currentip = ipVar.get()

    

fileToSend = StringVar()
fileToSend.set("/")

urlDisplayVar = StringVar()
urlDisplayVar.set("Merci d'importer un pdf pour obtenir une url")

ipVar = StringVar()

window.title("Miaow PDF")
window.geometry("500x500")
window.configure(bg="white")

title = tk.Label(window, font=("Segoe UI",25), bg="white", fg="black", text="Miaow PDF")
title.place(relx=0.5, rely=0.1, anchor="center")

ipBox = tk.Entry(window, bg="white", fg="black", textvariable=ipVar)
ipBox.place(relx=0.5, rely=0.2, anchor="center")

submitIp = tk.Button(highlightbackground="white", fg="black", text='Soumettre ip', width=20, command=ipSave)
submitIp.place(relx=0.5, rely=0.3, anchor="center")

fileExplorer = tk.Button(highlightbackground="white", fg="black", text='Importer un fichier', width=20, command=browseFiles)
fileExplorer.place(relx=0.5, rely=0.4, anchor="center")

selectedFileLabel = tk.Label(window, font=("Segoe UI",15), bg="white", fg="black", textvariable=fileToSend)
selectedFileLabel.place(relx=0.5, rely=0.5, anchor="center")

urlDisplay = tk.Button(highlightbackground="white", fg="black", text='Envoyer', width=20, command=lambda: sendButton(fullPath))
urlDisplay.place(relx=0.5, rely=0.6, anchor="center")

urlLabel = tk.Label(window, font=("Segoe UI",15), bg="white", fg="black", textvariable=urlDisplayVar)
urlLabel.place(relx=0.5, rely=0.7, anchor="center")

urlDisplay = tk.Button(highlightbackground="white", fg="black", text='Copier url', width=20, command=copyUrl)
urlDisplay.place(relx=0.5, rely=0.8, anchor="center")


window.mainloop()   

    #utiliser Listbox pour l historique


