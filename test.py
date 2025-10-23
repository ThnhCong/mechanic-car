import tkinter as tk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageGrab


class interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Motion of car")
        self.root.geometry("600x400")
        self.screen_height = root.winfo_screenheight()
        self.screen_width = root.winfo_screenwidth()
        self.canvas = tk.Canvas(root, height=self.screen_height, width=self.screen_width)
        self.canvas.pack()

        self.button_start = tk.Button(self.root, text= "Start", command= self.start)
        self.button_start.place(x= self.screen_width/2, y= self.screen_height/2)

        self.button_reset = tk.Button(self.root, text="Reset", command=self.reset)
        self.button_reset.place(x=self.screen_width / 2+50, y=self.screen_height / 2)

    def motion(self):
        self.img = Image.fromarray(cv2.resize(cv2.imread("car_rgba.png", cv2.IMREAD_UNCHANGED), (150,150)))
        self.img_flip = Image.fromarray(cv2.flip(np.array(cv2.resize(cv2.imread("car_rgba.png", cv2.IMREAD_UNCHANGED), (100,100))), 1))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.img_id = self.canvas.create_image(self.screen_width/2, self.screen_height/2+100,image= self.img_tk)

        self.cordinate_x = self.canvas.create_line(30, 10, 10, 30, 50, 30, 30, 10, 30, 400, 30, 310, 430, 310, 410, 290, 410, 330, 430, 310)
        self.canvas.create_polygon(30, 10, 10, 30, 50, 30, fill= "black", outline= "black")
        self.canvas.create_polygon(430, 310, 410, 290, 410, 330, fill= "black", outline= "black")
        self.canvas.create_text(15, 310, fill= "black", font= ("Times New Roman", 15), text= "O")
        self.canvas.create_text(430, 340, fill= "black", font= ("Times New Roman", 15), text= "time(s)", anchor="nw")
        self.canvas.create_text(40, 40, fill= "black", font= ("Times New Roman", 15), text= "position", anchor= "nw")

        self.canvas.create_line(self.screen_width/2-60, self.screen_height/2+150, self.screen_width/2+180, self.screen_height/2+150)
        p = -2
        for i in range(int(self.screen_width/2)-60, int(self.screen_width/2)+181, 30):
            self.canvas.create_line(i, self.screen_height/2+145, i, self.screen_height/2+155)
            self.canvas.create_text(i, self.screen_height/2+165, font= ("Times New Roman", 15), text= f"{p}")
            p += 1

        y0 = 305
        y1 = 315
        t = 0.0
        for i in range(90, 391, 60):
            self.canvas.create_line(i, y0, i, y1)
            self.canvas.create_text(i, 330, fill= "black", font= ("Times New Roman", 15), text= f"{t+0.5}")
            self.canvas.create_line(i, 400, i, 80, dash= (4,2))
            t += 0.5

        x0 = 25
        x1 = 35
        T = -2
        for y in range(370, 99, -30):
            if y != 310:
                self.canvas.create_line(x0, y, x1, y)
                self.canvas.create_text(15, y, fill= "black", font= ("Times New Roman", 15), text= T)
                self.canvas.create_line(30, y, 400, y, dash= (4, 2))
                T += 1
            if y == 310:
                T += 1


        self.t = np.linspace(0,3,300)
        self.x = -4*self.t + 2*self.t**2
        self.t = 120*self.t
        self.x = 30*self.x
        for i in np.arange(0, len(self.t)-1):
            self.canvas.create_line(self.t[i]+30, 310-self.x[i], 30+self.t[i+1], 310-self.x[i+1], fill= "red")

        self.canvas.create_text(360, 220, font= ("Times New Roman", 15), fill= "green", text= "x = -4t + 2t²", anchor= "nw")
        self.img_id_oval = self.canvas.create_oval((30+self.t[0])-7, (310-self.x[0])-7, (30+self.t[0])+7, (310-self.x[0])+7, fill= "black")

    def start(self, i=0):
        self.canvas.coords(self.img_id, self.screen_width/2 + self.x[i], self.screen_height/2+100)
        self.canvas.coords(self.img_id_oval, (30+self.t[i])-7, (310-self.x[i])-7, (30+self.t[i])+7, (310-self.x[i])+7)
        self.canvas.after(10, self.start, i+1)
    def reset(self):
        self.canvas.coords(self.img_id, self.screen_width/2, self.screen_height/2+100)
        self.canvas.coords(self.img_id_oval, (30+self.t[0])-7, (310-self.x[0])-7, (30+self.t[0])+7, (310-self.x[0])+7)

if __name__ == "__main__":
    root = tk.Tk()
    project = interface(root)
    project.motion()
    root.mainloop()