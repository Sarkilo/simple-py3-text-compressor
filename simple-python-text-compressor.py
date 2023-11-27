def compress(text):
    compressed = []
    current_byte = 0
    bit_count = 0

    for char in text:
        if (char.islower()):
            char_value = ord(char) - ord('a')  # Map 'a' to 0, 'b' to 1, ..., 'z' to 25
            
            current_byte |= char_value << bit_count
            bit_count += 5

            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        elif (char == ' '):
            char_value = 26
		  
            current_byte |= char_value << bit_count
            bit_count += 5
		  
            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        elif (char == '.'):
            char_value = 27
		  
            current_byte |= char_value << bit_count
            bit_count += 5
		  
            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        elif (char == ','):
            char_value = 28
		  
            current_byte |= char_value << bit_count
            bit_count += 5
		  
            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        elif (char == '\''):
            char_value = 29
		  
            current_byte |= char_value << bit_count
            bit_count += 5
		  
            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        elif (char == '\n'):
            char_value = 30
		  
            current_byte |= char_value << bit_count
            bit_count += 5
		  
            if (bit_count >= 6):
                compressed.append(chr(current_byte + 0x20))  # Convert to printable ASCII (0x20 to 0x7E)
                bit_count -= 6
                current_byte >>= 6
        else:
            print(f"\nBro this {char} is not compressable \n")
            exit()
                
    if (bit_count > 0):
        compressed.append(chr(current_byte + 0x20))

    return ''.join(compressed)

def decompress(compressed_text):
    decompressed = []
    current_value = 0
    bit_count = 0

    for char in compressed_text:
        char_value = ord(char) - 0x20  # Convert back to original value (0x20 to 0x7E)
        current_value |= (char_value & 0x3F) << bit_count  # Use 6 bits (0x3F = 0b111111)
        bit_count += 6

        while (bit_count >= 5):
            letter_value = current_value & 0x1F  # Extract the lower 5 bits
            if (letter_value <= 25):
                decompressed.append(chr(letter_value + ord('a')))  # Map back to lowercase letter
            else:
                if (letter_value == 26):
                    decompressed.append(' ')
                elif (letter_value == 27):
                    decompressed.append('.')
                elif (letter_value == 28):
                    decompressed.append(',')
                elif (letter_value == 29):
                    decompressed.append('\'')
                elif (letter_value == 30):
                    decompressed.append('\n')
            bit_count -= 5
            current_value >>= 5

    return ''.join(decompressed)

if (input("Do you want cli or file? [c/f]: ") == 'f'):
    directory = input("Give me the direction of file you want to compress or decompress: ")
    with open(directory, "r") as fileread:
        if (input("Do you want to compress or decompress? [c/d]: ") == 'c'):
            with open(directory + "_compressed", "w") as filesave:
                while (True):
                    line = fileread.read()
                    if (line != ''):
                        filesave.write(compress(line))
                    else:
                        exit()
        else:
            with open(directory + "_decompressed", "w") as filesave:
                while (True):
                    line = fileread.read()
                    if (line != ''):
                        filesave.write(decompress(line))
                    else:
                        exit()

else:
    text = input("Give me the text you want to compress: ")
    compressed_text = compress(text)
    print("Compressed:", compressed_text)

    decompressed_text = decompress(compressed_text)
    print("Decompressed:", decompressed_text)