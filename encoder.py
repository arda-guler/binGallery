from PIL import Image
import os

from utils import *

def read_file():
    filename = input("File to encode: ")

    file_found = False
    
    try:
        file = open(filename, "rb")
        file_found = True
    except:
        for extension in common_extensions:
            
            try:
                file = open(filename + extension, "rb")
                filename = filename + extension
                file_found = True
                break
            except FileNotFoundError:
                pass

    if not file_found:
        print("Can not find or open file.")
        quit()

    filesize = os.path.getsize(filename)

    data = []
    i = 0
    while i < filesize:
        try:
            data.append(file.read(1))
            i += 1
        except:
            break

    file.close()

    return data, filename

def main():
    data, filename = read_file()

    ints = []
    for byte in data:
        ints.append(int.from_bytes(byte, "big"))

    rgbs = []
    i = 0
    while i < len(ints):
        if i+2 < len(ints):
            rgbs.append((ints[i], ints[i+1], ints[i+2]))
        elif i+1 < len(ints):
            rgbs.append((ints[i], ints[i+1], 0))
        else:
            rgbs.append((ints[i], 0, 0))

        i += 3
            
##    for i in range(0, len(ints), 3):
##        try:
##            rgbs.append((ints[i], ints[i+1], ints[i+2]))
##        except:
##            try:
##                rgbs.append((ints[i], ints[i+1], 0))
##            except:
##                rgbs.append((ints[i], 0, 0))

    width = int(input("Width of output image in pixels (integer):"))
    height = int(len(rgbs)/width) + 1

    output = Image.new(mode="RGB", size=(width, height))
    pixels = output.load()

    for i in range(len(rgbs)):
        image_x = i % width
        image_y = int(i / width)

        pixels[image_x, image_y] = rgbs[i]

    output.save(filename+"-encoded.png")

main()
input("Press Enter to quit.")
