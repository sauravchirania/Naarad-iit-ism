import base64

def encode_image(image_address):
    with open(image_address, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string

if __name__ == '__main__':
    IMG_ADDRESS = input("Give the location of the image file: ")
    print(encode_image(IMG_ADDRESS))