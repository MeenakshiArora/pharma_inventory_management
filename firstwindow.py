from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
import random
import time
import datetime


def main():
    root=Tk()
    app=Window1(root)

class Window1:
    def __init__(self,root):
        self.root=root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1300x700")
        self.frame=Frame(self.root)
        self.root.configure(bg="#d7f1c9")
        Label(self.root, text="Login to Pharmacy System", font="stencil 30", fg="#21421e", bg="#d7f1c9").place(x=50, y=10)

        #self.frame.pack()


if __name__ == '__main__':
    main()