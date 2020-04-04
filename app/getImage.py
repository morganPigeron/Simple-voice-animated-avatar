import os

def imgList():
    #get path of animation images 
    path = os.path.dirname(__file__)
    basePath = os.path.abspath(os.path.join(path, os.pardir))
    imgPath = os.path.abspath(os.path.join(basePath, "images"))

    pathList = []

    for image in os.listdir(imgPath):
        pathList.append(os.path.join(imgPath, image))

    return pathList

def dicoAvatars():

    """
    Get the list of available avatars in the images folder
    inputs : none
    output : Avatar Dictionary (keys:Avatar names, values : Avatar path)

    """
    path = os.path.dirname(__file__)
    basePath = os.path.abspath(os.path.join(path, os.pardir))
    imgPath = os.path.abspath(os.path.join(basePath, "images"))

    listOfAvatars = []
    pathOfAvatars = []

    for dirnames in os.listdir(imgPath):
        listOfAvatars.append(dirnames)
        dirpath = os.path.abspath(os.path.join(imgPath, dirnames))
        pathOfAvatars.append(dirpath)

    Avatars = {}

    Avatars = dict(zip(listOfAvatars, pathOfAvatars))
    
    """for elements in Avatars:
        print("keys : " + str(elements) + "\tvalue : " + str(Avatars[elements]))"""

    return Avatars


"""
photo0 = tk.PhotoImage(file='images/chat0.png')
photo11 = tk.PhotoImage(file='images/chat11.png')
photo12 = tk.PhotoImage(file='images/chat12.png')
photo2 = tk.PhotoImage(file='images/chat2.png')
"""

if __name__ == "__main__":
    #print(imgList())
    print(dicoAvatars())