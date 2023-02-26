from lwcc import LWCC
import cv2,os
import numpy as np
from tkinter import *
from tkinter import filedialog
from threading import Thread
from tkinter import messagebox


global filename
global fps
global count_store

def gui():
    base = Tk()
    base.geometry("700x350")
    base.title("CROWD SURVEILLANCE")
    global up
    global down
    global first 
    first=1
    global alert
    alert=0

    def add_new_video_file():
            #base.destroy()
            global filename
            filename = str(filedialog.askopenfilename())
            #print(filename)
            temp = ''
            for i in filename:
                if i == '/':
                    temp += '\\'
                else:
                    temp += i
            filename = temp
        
    def run():
            control_thread = Thread(target=frame_extraction, daemon=True)
            control_thread.start()

    def frame_extraction():  # Read the video from the given path   
    
    
        cam = cv2.VideoCapture(filename)
        print('Function: ',filename)
        fps = 120
        currentframe = 0

        try:
            print('Creating a folder named images....')
            if not os.path.exists('images'):
                os.makedirs('images')
        except OSError:
            messagebox.showerror("Error", "Failed to create the Directory")

        while (1):
            ret, frame = cam.read()
            if not ret:
                break
            if ret:
                name = './images/frame' + str(currentframe) + '.jpg'
                if currentframe % fps == 0:
                    cv2.imwrite(name, frame)
                    count_function(name)
                    try:
                        os.remove('./images/frame' + str(currentframe) + '.jpg')
                    except OSError:
                        messagebox.showerror("Error", "Couldn't Delete the Frame Created")
                        continue
            currentframe += 1
        cam.release()

    def count_function(filename,model_name = "SFANet", model_weights = "SHB"):
        global first
        global up
        global down
        global alert
        temp=0.0
        temp1=0.0
        count= LWCC.get_count(filename, return_density = True,model_name = "SFANet", model_weights = "SHB", resize_img = False)
        print(count)
        if(first==1):
            tamp1=float(count[0])
            temp=float(count[0])
            temp+=(temp*0.5)
            up=temp
            temp1-=(temp1*0.5)
            down=temp1
        first+=1
        if(count[0]>=up or count[0]<=down):
            
            if(alert<100):
                alert+=10
            #print("alert level "+str(alert)+"%")    
        count_textbox.config(text="Alert level "+str(alert)+"%")   


    lb = Label(base, text="CROWD SURVEILLANCE", font=("VERDANA",25))
    lb.place(x=100, y=20)
    lb.pack()
    count_textbox = Label(base, text = "--*--",fg = "green",bg= "black", font ="Times 25 bold",padx=50, pady=10 )
    count_textbox.place(x=240, y=175)
    count_textbox.pack()
    add_video_button = Button(base, text="Add video ", font=("Arial Bold", 10), command=add_new_video_file)
    add_video_button.place(x=575, y=138)
    add_video_button.pack()
    Start_button= Button(base, text="Start", font=("Arial Bold", 10), command=run)
    Start_button.place(x=280, y=220)
    Start_button.pack()
    base.mainloop()





def start():
    t1 = Thread(target=gui)  # Creates a thread for first_page function
    t1.start()  # runs the thread



if __name__ == '__main__':
    start()  # runs the thread function