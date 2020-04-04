# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:43:36 2018

"""

from app import gui
from newModule import dim

print(dim.add(2,3))

app = gui.Application()
app.printAudioDevice()
app.after(33,app.refresh)
app.mainloop()