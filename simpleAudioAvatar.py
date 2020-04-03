# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:43:36 2018

"""

import pyaudio
import audioop
import tkinter as tk

#My lib
from anim import getImage


CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

selecteur = 0

#object pyaudio
p = pyaudio.PyAudio()
print(p.get_device_count())


#open audio stream
stream = p.open(
                format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                input_device_index = 1,
                frames_per_buffer = CHUNK
                )

#Get audio device 
device_index = None           
for i in range( p.get_device_count() ):     
    devinfo = p.get_device_info_by_index(i)   
    print( "Device %d: %s"%(i,devinfo["name"]) )
    

#function  

def refresh():
    global selecteur
    
    #read an audio chunk
    data = stream.read(CHUNK)

    #get rms volume
    rms = audioop.rms(data, 2)
    valeur["text"] = rms
            
    
    #little image selector
    if rms <= int(seuilBas.get()):
        labelImage["image"] = photo0
        
    elif rms >= int(seuilBas.get()) and rms <= int(seuilHaut.get()):
        if selecteur == 0:
            labelImage["image"] = photo11
            selecteur = 1
        elif selecteur == 1:
            labelImage["image"] = photo12
            selecteur = 0
        
    else:
        labelImage["image"] = photo2
    
    #recall this function after 33 ms
    fenetre.after(33, refresh)
    
    
# tkinter stuff ...

fenetre = tk.Tk()
fenetre.title("Chat Animation")

titre = tk.Label(fenetre, text="Animation Audio")
titre.pack()

valeur = tk.Label(fenetre)
valeur.pack()

imgPathList = getImage.imgList()

photo0 = tk.PhotoImage(file=imgPathList[0])
photo11 = tk.PhotoImage(file=imgPathList[1])
photo12 = tk.PhotoImage(file=imgPathList[2])
photo2 = tk.PhotoImage(file=imgPathList[3])

labelImage = tk.Label(fenetre, image = photo0, bg = "green")
labelImage.pack()


# Add two scale widget to select wich animation will be displayed
# ex : quiet animation1  (in this case, an unique image)
#      normal volume animation 2 (in this case animation with 2 images)
#      loud animation 3 (in this case, an unique image)

labelSeuilBas = tk.Label(fenetre, text="Seuil Bas")
labelSeuilBas.pack()

seuilBas = tk.DoubleVar()
seuilBas.set(1000)
sliderSeuilBas = tk.Scale( fenetre, 
                          variable = seuilBas, 
                          orient=tk.HORIZONTAL, 
                          from_=0, to=19000,
                          length = 256
                          )
sliderSeuilBas.pack(anchor = tk.CENTER)

labelSeuilHaut = tk.Label(fenetre, text="Seuil Haut")
labelSeuilHaut.pack()

seuilHaut = tk.DoubleVar()
seuilHaut.set(10000)
sliderSeuilHaut = tk.Scale( fenetre,
                           variable = seuilHaut,
                           orient=tk.HORIZONTAL,
                           from_=0, to=19000,
                           length = 256
                           )
sliderSeuilHaut.pack(anchor = tk.CENTER)

#Tkinter mainloop
fenetre.after(33, refresh)    
fenetre.mainloop()
