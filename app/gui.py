import tkinter as tk

import pyaudio
import audioop

from app import getImage

class Application(tk.Tk):

    def __init__(self):

        #init parent class
        tk.Tk.__init__(self)
        
        #change title
        self.title("Animation")

        #variable anim
        self.selecteur = 0
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000

        #init image
        self.initImage()

        #init audio stream
        self.initAudio()
        
        #init animation box
        self.initAnimation()

        #init sound settings
        self.initSettings()

    def initAudio(self):
        #object pyaudio
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
                            format = self.FORMAT,
                            channels = self.CHANNELS,
                            rate = self.RATE,
                            input = True,
                            output = False,
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

            self.img = self.imgTab[0]
            self.imgRefresh()

                
        elif rms >= int(self.seuilBas.get()) and rms <= int(self.seuilHaut.get()):

            if self.selecteur == 0:
                self.img = self.imgTab[1]
                self.imgRefresh()
                self.selecteur = 1

            elif self.selecteur == 1:
                self.img = self.imgTab[2]
                self.imgRefresh()
                self.selecteur = 0
            
            
        else:
            self.img = self.imgTab[3]
            self.imgRefresh()

        #recall this function after 33 ms
        self.after(33, self.refresh)

    def initImage(self):
 
        self.imgTab = []

        for path in getImage.imgList():
            self.imgTab.append(tk.PhotoImage(file=path))

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
        self.img = self.imgTab[0].copy() #hold image in use
        self.labelImage = tk.Label(self, image = self.img, bg = "green")
        self.labelImage.pack()
            
        
if __name__ == "__main__":
    app = Application()
    app.printAudioDevice()
    app.after(33,app.refresh)
    app.mainloop()
    