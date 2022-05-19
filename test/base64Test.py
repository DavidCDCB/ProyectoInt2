import base64

binary_file = open('recorte.jpg', 'rb')
binary_file_data = binary_file.read()
base64_encoded_data = base64.b64encode(binary_file_data)
base64_message = base64_encoded_data.decode('utf-8')

print(base64_message)

base64_img_bytes = base64_message.encode('utf-8')
file_to_save = open('decoded_image.png', 'wb')
decoded_image_data = base64.decodebytes(base64_img_bytes)
file_to_save.write(decoded_image_data)