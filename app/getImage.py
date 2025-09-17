import os

def imgList():
    #get path of animation images 
    path = os.path.dirname(__file__)
    basePath = os.path.abspath(os.path.join(path, os.pardir))
    imgPath = os.path.abspath(os.path.join(basePath, "images"))

    pathList = []

    for image in os.listdir(imgPath):
        pathList.append(os.path.join(imgPath, image))

    pathList.sort()
    print(pathList)
    return pathList
"""
photo0 = tk.PhotoImage(file='images/chat0.png')
photo11 = tk.PhotoImage(file='images/chat11.png')
photo12 = tk.PhotoImage(file='images/chat12.png')
photo2 = tk.PhotoImage(file='images/chat2.png')
"""

if __name__ == "__main__":
    print(imgList())