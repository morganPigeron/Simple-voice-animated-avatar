import tkinter as tk
import os

import pyaudio
import audioop

from app import getImage
from functools import partial

class Application(tk.Tk):

    def __init__(self):

        #init parent class
        tk.Tk.__init__(self)
        
        #change title
        self.title("Animation")

        #variable anim
        self.selecteur1 = 0
        self.selecteur2 = 0
        self.selecteur3 = 0
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000

        #init image
        self.initImage(self.defaultPath())

        #init audio stream
        self.initAudio()
        
        #init animation box
        self.initAnimation()

        #init sound settings
        self.initSettings()

        #init menubar
        self.initMenu(getImage.dicoAvatars())

    def initAudio(self):
        #object pyaudio
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
                            format = self.FORMAT,
                            channels = self.CHANNELS,
                            rate = self.RATE,
                            input = True,
                            output = True,
                            input_device_index = 1,
                            frames_per_buffer = self.CHUNK
                            )

    def printAudioDevice(self):
        for i in range( self.p.get_device_count() ):     
            devinfo = self.p.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

    def refresh(self):
        
        #read an audio chunk
        data = self.stream.read(self.CHUNK)

        #get rms volume
        rms = audioop.rms(data, 2)
        self.micValue.set(rms) #update gui
              
        #little image selector
        if rms <= int(self.seuilBas.get()):
            if self.selecteur1 == len(self.steadyTab)-1:
                self.selecteur1 = 0

            else:
                self.selecteur1 = self.selecteur1 + 1

            self.img = self.steadyTab[self.selecteur1]
            self.imgRefresh()    
             
        
        elif rms >= int(self.seuilBas.get()) and rms <= int(self.seuilHaut.get()):
            
            if self.selecteur2 == len(self.talkTab)-1:
                self.selecteur2 = 0
            else:
                self.selecteur2 = self.selecteur2 + 1

            self.img = self.talkTab[self.selecteur2]
            self.imgRefresh()
                     
        else:

            if self.selecteur3 == len(self.shoutTab)-1:
                self.selecteur3 = 0
            else:
                self.selecteur3 = self.selecteur3 + 1

            self.img = self.shoutTab[self.selecteur3]
            self.imgRefresh()
            

        #recall this function after 33 ms
        self.after(33, self.refresh)

    def initImage(self,Folder):
 
        self.steadyTab = []
        self.talkTab = []
        self.shoutTab = []

        steadyPath = os.path.abspath(os.path.join(Folder, "Steady"))
        for image in os.listdir(steadyPath):
            print("charger l'image : " + os.path.join(steadyPath, image))
            self.steadyTab.append(tk.PhotoImage(file = os.path.join(steadyPath, image)))

        talkPath = os.path.abspath(os.path.join(Folder, "Talk"))
        for image in os.listdir(talkPath):
            print("charger l'image : " + os.path.join(talkPath, image))
            self.talkTab.append(tk.PhotoImage(file = os.path.join(talkPath, image)))

        shoutPath= os.path.abspath(os.path.join(Folder, "Shout"))
        for image in os.listdir(shoutPath):
            print("charger l'image : " + os.path.join(shoutPath, image))
            self.shoutTab.append(tk.PhotoImage(file = os.path.join(shoutPath, image)))

    def imgRefresh(self):
        self.labelImage.config(image=self.img)

    def initSettings(self):
        self.micValue = tk.IntVar()
        
        self.seuilBas = tk.DoubleVar()
        self.seuilBas.set(1000) #not mandatory

        self.seuilHaut = tk.DoubleVar()
        self.seuilHaut.set(10000) #not mandatory

        self.labelvalue = tk.Label(self)
        self.labelvalue.configure(textvariable=self.micValue)
        self.labelvalue.pack()

        self.labelSeuilBas = tk.Label(self, text="Seuil Bas")
        self.labelSeuilBas.pack()

        self.sliderSeuilBas = tk.Scale( 
                                self, 
                                variable = self.seuilBas, 
                                orient=tk.HORIZONTAL, 
                                from_=0, to=19000,
                                length = 256
                                )
        self.sliderSeuilBas.pack(anchor = tk.CENTER)

        self.labelSeuilHaut = tk.Label(self, text="Seuil Haut")
        self.labelSeuilHaut.pack()

        self.sliderSeuilHaut = tk.Scale( 
                                self,
                                variable = self.seuilHaut,
                                orient=tk.HORIZONTAL,
                                from_=0, to=19000,
                                length = 256
                                )
        self.sliderSeuilHaut.pack(anchor = tk.CENTER)

    def initAnimation(self):
        self.img = self.steadyTab[0] #hold image in use
        self.labelImage = tk.Label(self, image = self.img, bg = "green")
        self.labelImage.pack()

    def selectAnimation(self,Folder):
        self.initImage(Folder)

    def initMenu(self,Avatars):

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)

        submenu = tk.Menu(filemenu, tearoff=0)
        for elements in Avatars:
            submenu.add_command(label=str(elements), command=partial(self.selectAnimation, Avatars[elements]))
        filemenu.add_cascade(label='Avatars', menu=submenu)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        #above command will display menu
        self.config(menu=menubar)
    
    def defaultPath(self):
        path = os.path.dirname(__file__)
        basePath = os.path.abspath(os.path.join(path, os.pardir))
        imgPath = os.path.abspath(os.path.join(basePath, "images"))
        deflt = os.path.abspath(os.path.join(imgPath, "Default"))

        return deflt

if __name__ == "__main__":
    app = Application()
    app.printAudioDevice()
    app.after(33,app.refresh)
    app.mainloop()