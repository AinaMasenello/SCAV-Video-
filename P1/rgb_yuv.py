import subprocess
import numpy as np
from scipy.fftpack import dct, idct

#EX 1:

def translate_rgb_yuv(r,g,b):
    Y = 0.299*r + 0.587*g + 0.114*b
    U = 0.492 * (b-Y)
    V = 0.877 * (r-Y)
    return [Y,U,V]

def translate_yuv_rgb(y,u,v):
    R = y + 1.140*v
    G = y - 0.395*u - 0.581*v
    B = y + 2.032*u
    return [R,G,B]

#print(translate_rgb_yuv(0,128,0))
#print(translate_yuv_rgb(75.1360, -37.0420, -65.8943))

#EX 2:
    
def resize(input_path_image, output_path_image, width):
    command = [
            'ffmpeg',
            '-i', input_path_image,          # Input image path
            '-vf', f'scale={width}:-1',  # Resize filter with specified width
            output_path_image               # Output image path
        ]   
    subprocess.run(command, check=True)

input_image = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/prova.jpeg'
output_image = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/prova_320.jpeg'
desired_width = 320

#resize(input_image, output_image, desired_width)

#EX 3:

def generate_zigzag_pattern(width, height):
    pattern = []
    for i in range(width):
        for j in range(height):
            if i % 2 == 0:
                pattern.append((i, j))
            else:
                pattern.append((i, height - 1 - j))
    return pattern

def serpentine(file_path):
    with open(file_path, 'rb') as file:
            # Read the header (first 54 bytes of BMP)
            bmp_header = bytearray(file.read(54))
            width = int.from_bytes(bmp_header[18:22], 'little')
            height = int.from_bytes(bmp_header[22:26], 'little')
            image_data = bytearray(file.read())

            # Process the image data in a serpentine pattern
            zigzag_pattern = generate_zigzag_pattern(width, height)
            pixel_values = []

            for x, y in zigzag_pattern:
                index = (y * width + x) * 3  # 3 bytes per pixel for RGB
                if index < len(image_data):
                    pixel = image_data[index:index + 3]  # 3 bytes for RGB
                    pixel_values.append(pixel)

            return pixel_values
        
file_path = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/lenna.jpeg'

#print(serpentine(file_path))

#EX 4:

def compress_and_convert_to_bw(input_image, output_image, quality=0):
    # Define FFMPEG command to convert to black and white and apply compression
    command = [
            'ffmpeg',
            '-i', input_image,
            '-vf', 'format=gray',
            '-q:v', str(quality),
            output_image
        ]

    # Run the FFmpeg command
    subprocess.run(command, check=True)
output_image = '/Users/ainamasenello/Documents/GitHub/SCAV-Video-/prova_bw.jpeg'
#compress_and_convert_to_bw(input_image, output_image)

#EX 5:

def run_length_encode(input_bytes):
    if not input_bytes:
        return bytes()

    encoded_data = bytearray()
    current_byte = input_bytes[0]
    count = 1

    for byte in input_bytes[1:]:
        if byte == current_byte:
            count += 1
        else:
            encoded_data.append(current_byte)
            encoded_data.append(count)
            current_byte = byte
            count = 1

    encoded_data.append(current_byte)
    encoded_data.append(count)

    return bytes(encoded_data)

original_bytes = b'\x01\x01\x01\x02\x03\x03\x04\x04\x04\x05'
#print(run_length_encode(original_bytes))

#EX 6:

class DCTConverter:
    def __init__(self):
        pass

    def dct_encode(self, data):
        """
        Encode input data using Discrete Cosine Transform (DCT).

        Args:
            data (np.ndarray): Input data to be encoded.

        Returns:
            np.ndarray: Encoded data using DCT.
        """
        return dct(data, norm='ortho')

    def dct_decode(self, encoded_data):
        """
        Decode data previously encoded using DCT.

        Args:
            encoded_data (np.ndarray): Data encoded using DCT.

        Returns:
            np.ndarray: Decoded data.
        """
        return idct(encoded_data, norm='ortho')
    

data_to_encode = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    
# Create an instance of the DCTConverter
dct_converter = DCTConverter()

# Encode the data using DCT
encoded_data = dct_converter.dct_encode(data_to_encode)
#print("Encoded Data:", encoded_data)

# Decode the data
decoded_data = dct_converter.dct_decode(encoded_data)
#print("Decoded Data:", decoded_data)