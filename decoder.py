from PIL import Image

def read_encoded():
    filename = input("File to decode: ")

    try:
        image = Image.open(filename)
    except FileNotFoundError:
        try:
            image = Image.open(filename + "-encoded.png")
        except FileNotFoundError:
            print("Can not find file.")
            quit()

    pixels = image.load()

    return image, pixels, filename

def main():
    image, pixels, filename = read_encoded()

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

    print("Do not forget to replace the file extension with the original one to complete restoration of your file.")

main()
input("Press Enter to quit.")
        
