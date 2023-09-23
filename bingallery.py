from PIL import Image
import os
import sys

# common file extensions to look for if the user is too lazy
# to provide one as input
# ordered in order of preference
common_extensions = [".bin", ".exe", ".com", # binaries, executables
                     ".png", ".jpg", ".jpeg", ".svg", ".webm", # pictures
                     ".ogg", ".wav", ".flac", ".mp3", # audio
                     ".mp4", ".mov", # video
                     ".zip", ".pdf", ".tar", ".7z", ".lnk", ".ico"] # misc


def read_file_encode(filename):

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

    return data

def read_file_decode(filename):

    try:
        image = Image.open(filename)
    except FileNotFoundError:
        try:
            image = Image.open(filename + "-encoded.png")
        except FileNotFoundError:
            print("Can not find file.")
            quit()

    pixels = image.load()

    return image, pixels

def main():

    system_args = sys.argv
    
    if len(system_args) < 3:
        print("binGallery: file <--> image converter")
        print("https://github.com/arda-guler/binGallery")
        print("")
        print("Syntax for encoding: bingallery encode <filename> <image_width(optional)>")
        print("Syntax for decoding: bingallery decode <filename>")
        print("")
        print("Default image width for encoded images is 1920 px.")
        return

    else:
        if system_args[1] == "encode" or system_args[1] == "e":
            
            # ENCODING
            width = None
            if len(system_args) == 4:
                width = int(system_args[3])
                
            filename = system_args[2]
            data = read_file_encode(filename)

            print("Encoding", filename, "...")
            print("Depending on the size of the file, this might take a while.")

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

            if not width:
                width = 1920
                
            height = int(len(rgbs)/width) + 1

            output = Image.new(mode="RGB", size=(width, height))
            pixels = output.load()

            for i in range(len(rgbs)):
                image_x = i % width
                image_y = int(i / width)

                pixels[image_x, image_y] = rgbs[i]

            output.save(filename+"-encoded.png")
            print("Done!")
            print("Output file:", filename+"-encoded.png")
            
        elif system_args[1] == "decode" or system_args[1] == "d":

            # DECODING
            filename = system_args[2]
            image, pixels = read_file_decode(filename)

            print("Decoding", filename, "...")

            width = image.size[0]
            height = image.size[1]

            data = []

            for y in range(height):
                for x in range(width):
                    current_pixel = pixels[x, y]
                    for i in current_pixel:
                        data.append(i.to_bytes(1, "big"))

            with open(filename + "-decoded.original_extension", "wb") as f_out:
                for d in data:
                    f_out.write(d)

            print("Done!")
            print("Output file:", filename + "-decoded.original_extension")
            print("Do not forget to replace the file extension with the original one to complete the restoration of the decoded file.")

main()

