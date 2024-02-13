import random
import random
import struct
class PulseSensor():
    def __init__(self):
        self.pulse = 0

    def get_data(self):
        val1 = random.randint(1, 100)
        val2 = random.randint(1, 100)
        val3 = random.randint(0, 2)
        val4 = random.randint(1, 100)
        val4a = random.randint(1, 9)
        val5 = random.randint(1, 100)
        val5a = random.randint(1, 9)
        val6 = random.randint(1, 100)
        val6a = random.randint(1, 9)

        # Print the generated values
        print("Random values:")
        print("val1:", val1)
        print("val2:", val2)
        print("val3:", val3)
        print("val4:", val4)
        print("val4a:", val4a)
        print("val5:", val5)
        print("val5a:", val5a)
        print("val6:", val6)
        print("val6a:", val6a)


        # Convert values to bytes
        val1_bytes = val1.to_bytes(1, byteorder='big')
        val2_bytes = val2.to_bytes(1, byteorder='big')
        val3_bytes = val3.to_bytes(1, byteorder='big')
        val4_bytes = val4.to_bytes(1, byteorder='big')
        val4a_bytes = val4a.to_bytes(1, byteorder='big')
        val5_bytes = val5.to_bytes(1, byteorder='big')
        val5a_bytes = val5a.to_bytes(1, byteorder='big')
        val6_bytes = val1.to_bytes(1, byteorder='big')
        val6a_bytes = val6a.to_bytes(1, byteorder='big')

        # Print bytes representation
        print("\nBytes representation:")
        print("val1 bytes:", val1_bytes)
        print("val2 bytes:", val2_bytes)
        print("val3 bytes:", val3_bytes)
        print("val4 bytes:", val4_bytes)
        print("val4a bytes:", val4a_bytes)
        print("val5 bytes:", val5_bytes)
        print("val5a bytes:", val5a_bytes)
        print("val6 bytes:", val6_bytes)
        print("val6a bytes:", val6a_bytes)

        # Create byte array
        byte_array = bytearray()
        byte_array.extend(val1_bytes)
        byte_array.extend(val2_bytes)
        byte_array.extend(val3_bytes)
        byte_array.extend(b'\x01')  # Insert byte > 0
        byte_array.extend(val4_bytes)
        byte_array.extend(val4a_bytes)
        byte_array.extend(b'\x01')  # Insert byte > 0
        byte_array.extend(val5_bytes)
        byte_array.extend(val5a_bytes)
        byte_array.extend(b'\x01')  # Insert byte > 0
        byte_array.extend(val6_bytes)
        byte_array.extend(val6a_bytes)

        # Print byte array
        print("\nByte array:")
        print(byte_array)

        return byte_array