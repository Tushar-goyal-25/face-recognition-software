from tkinter import Tk
from tkmacosx import Button
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import subprocess
import face_recognition
import datetime


#Helper class
class Components:
    def get_button(self, window, text, color, command, fg='white'):
        button = Button(
            window,
            text=text,
            activebackground="black",
            activeforeground="white",
            fg=fg,
            bg=color,
            command=command,
            height=95,
            width=400,
            borderless=1,
            font=('Helvetica bold', 20)
        )


        return button
    def get_img_label(self, window):
        label = tk.Label(window)
        label.grid(row=0, column=0)
        return label

    def get_entry_text(self, window):
        inputtxt = tk.Text(window, height=2, width=20, font=("Arial", 32))
        return inputtxt
    
    def get_text_label(self, window, text):
        label = tk.Label(window, text=text)
        label.config(font=("sans-serif", 21), justify="left")
        return label
    def msg_box(self, title, description):
        messagebox.showinfo(title, description)

# Main Class

class App:
    def __init__(self):
        com = Components()
        self.main_window = Tk() #Creating a window
        self.main_window.geometry("1200x520+250+100") # size of the window
        #Buttons
        self.login_btn = com.get_button(self.main_window, "login", 'green', self.login)
        # self.login_btn.pack(padx=20, pady=10)
        self.login_btn.place(x=750, y=300)
        self.register_btn = com.get_button(self.main_window, "register", 'gray', self.register, fg="black")
        self.register_btn.place(x=750, y=400)
        #Webcam Label
        self.webcam_lbl = com.get_img_label(self.main_window)
        self.webcam_lbl.place(x=10, y=0, width= 700, height = 500)
        #Create Database
        self.add_webcam(self.webcam_lbl)
        self.db_dir = "./db"
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        #Create Log File
        self.log_path = './log.txt'

    #Login Window Functionality

    def login(self):
        com = Components()
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-3]
        if name in ['unknown_person', 'no_persons_found']:
            com.msg_box('try Again', 'Unkown User, Please register a user or try again')
        else:
            com.msg_box('Successful', 'Welcome {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now() ))
                f.close()



        os.remove(unknown_img_path)




    #Register WINDOW functionality
    def register(self):
        com = Components()
        self.register_window = tk.Toplevel(self.main_window) #Creating a window above the existing one
        self.register_window.geometry("1200x520+200+120") # size of the window
        #Buttons
        self.accept_btn = com.get_button(self.register_window, "Accept", 'green', self.accept_new_user)
        # self.login_btn.pack(padx=20, pady=10)
        self.accept_btn.place(x=750, y=300)
        self.return_btn = com.get_button(self.register_window, "Return", 'gray', self.return_user, fg="black")
        self.return_btn.place(x=750, y=400)
        #Lables
        self.capture_lbl = com.get_img_label(self.register_window)
        self.capture_lbl.place(x=10, y=0, width= 700, height = 500)
        self.add_img_to_label(self.capture_lbl)
        #text box
        self.entry_text = com.get_entry_text(self.register_window)
        self.entry_text.place(x=750, y=150)
        #text Box Label 
        self.text_label = com.get_text_label(self.register_window, "Please Input Username:")
        self.text_label.place(x=750, y=70)
        

    
    #Add image to the Database
    def add_img_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)

        #Put webcam in the label
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        #We do not use pillow for mat here because the pillow takes the most recent capture so if you are moving in the main window it will take the capture from there. Hence, this will not work.

    #Accept new User
    def accept_new_user(self):
        com = Components()
        name = self.entry_text.get(1.0, "end-1c") #Value user input
        cv2.imwrite( os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture) #adding the capture to the folder

        #Message box upon success
        com.msg_box('Success', 'User registered Successfully!')
        self.register_window.destroy()


    #Return to main window
    def return_user(self):
        self.register_window.destroy()



    #adding the webcam
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()
    
    #converting the webcam from opencv  format to pillow foramt 
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame #IN bgr format from open cv
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB) #conversion
        self.most_recent_capture_pil = Image.fromarray(img_) #in rgb format in pillow
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)

        #Put webcam in the label
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)



    #Start Function
    def start(self):
        self.main_window.mainloop() #to run the window
        # main loop is a fucntion that enters a loop to wait, process, update all events and Gui

#Main function
if __name__ == "__main__":
    app =App()
    app.start()