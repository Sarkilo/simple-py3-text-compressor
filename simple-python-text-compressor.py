"""
Text compressor/decompressor with tiered alphabet.

Tier 0 (5-bit code, values 0-31):
    0-25  -> lowercase letters a-z
    26    -> space
    27    -> '.'
    28    -> ','
    29    -> '\n'
    30    -> ESCAPE_1B  -> go to Tier 1b (symbols)
    31    -> ESCAPE_1A  -> go to Tier 1a (uppercase)

Tier 1a (next 5-bit code, read right after an ESCAPE_1A):
    0-25  -> uppercase letters A-Z

Tier 1b (next 5-bit code, read right after an ESCAPE_1B):
    0-27  -> symbol from SYMBOLS_TIER1B, in order:
             '  *  "  !  ?  ;  :  @  #  $  %  ^  &  (  )  -  _  =  +  {  }  [  ]  /  \\  <  >  |

Packing:
    5-bit codes are packed tightly into full 8-bit bytes (not restricted to the
    printable ASCII range anymore). Since lcm(5, 8) = 40, every 8 Tier-0-only
    characters (no escapes needed) pack into exactly 5 bytes.

Header:
    The compressed payload is prefixed with a 4-byte big-endian character count.
    This is what lets decompress() know exactly how many characters to emit,
    so leftover zero-padding bits at the end of the last byte are never
    mistaken for a real code (they're simply never read).
"""

import struct

SPACE = 26
DOT = 27
COMMA = 28
NEWLINE = 29
ESCAPE_1B = 30  # escape into Tier 1b (symbols)
ESCAPE_1A = 31  # escape into Tier 1a (uppercase)

SYMBOLS_TIER1B = [
    '\'', '*', '"', '!', '?', ';', ':',
    '@', '#', '$', '%', '^', '&', '(', ')', '-', '_',
    '=', '+', '{', '}', '[', ']', '/', '\\', '<', '>', '|',
]
SYMBOL_TO_CODE = {s: i for i, s in enumerate(SYMBOLS_TIER1B)}


def char_to_codes(char):
    """Return the list of 5-bit codes (each 0-31) that represent `char`."""
    if char.islower():
        return [ord(char) - ord('a')]
    if char == ' ':
        return [SPACE]
    if char == '.':
        return [DOT]
    if char == ',':
        return [COMMA]
    if char == '\n':
        return [NEWLINE]
    if char.isupper():
        return [ESCAPE_1A, ord(char) - ord('A')]
    if char in SYMBOL_TO_CODE:
        return [ESCAPE_1B, SYMBOL_TO_CODE[char]]
    raise ValueError(f"Bro this {char!r} is not compressable")


class BitWriter:
    """Packs values of arbitrary bit-width into full bytes, LSB-first."""

    def __init__(self):
        self.buffer = bytearray()
        self.acc = 0
        self.bits = 0

    def write(self, value, width):
        self.acc |= (value & ((1 << width) - 1)) << self.bits
        self.bits += width
        while self.bits >= 8:
            self.buffer.append(self.acc & 0xFF)
            self.acc >>= 8
            self.bits -= 8

    def flush(self):
        # Pad any leftover bits with zeros to complete the final byte.
        if self.bits > 0:
            self.buffer.append(self.acc & 0xFF)
            self.acc = 0
            self.bits = 0
        return bytes(self.buffer)


class BitReader:
    """Reads values of arbitrary bit-width from bytes, LSB-first."""

    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.acc = 0
        self.bits = 0

    def read(self, width):
        while self.bits < width:
            if self.pos >= len(self.data):
                raise EOFError("Not enough bits left to read - corrupted data?")
            self.acc |= self.data[self.pos] << self.bits
            self.bits += 8
            self.pos += 1
        value = self.acc & ((1 << width) - 1)
        self.acc >>= width
        self.bits -= width
        return value


def compress(text):
    """Compress `text` into bytes. Returns a 4-byte length header + payload."""
    writer = BitWriter()
    count = 0
    for char in text:
        for code in char_to_codes(char):
            writer.write(code, 5)
        count += 1
    payload = writer.flush()
    header = struct.pack('>I', count)  # original character count
    return header + payload


def decompress(data):
    """Decompress bytes produced by compress() back into the original text."""
    (count,) = struct.unpack('>I', data[:4])
    reader = BitReader(data[4:])
    output = []
    for _ in range(count):
        v = reader.read(5)
        if v == ESCAPE_1B:
            v2 = reader.read(5)
            output.append(SYMBOLS_TIER1B[v2])
        elif v == ESCAPE_1A:
            v2 = reader.read(5)
            output.append(chr(v2 + ord('A')))
        elif v <= 25:
            output.append(chr(v + ord('a')))
        elif v == SPACE:
            output.append(' ')
        elif v == DOT:
            output.append('.')
        elif v == COMMA:
            output.append(',')
        elif v == NEWLINE:
            output.append('\n')
        else:
            raise ValueError(f"Unknown Tier 0 code: {v}")
    return ''.join(output)


if __name__ == "__main__":
    mode = input("Do you want cli or file? [c/f]: ")
    if mode == 'f':
        directory = input("Give me the direction of file you want to compress or decompress: ")
        action = input("Do you want to compress or decompress? [c/d]: ")
        if action == 'c':
            with open(directory, "r", encoding="utf-8") as fileread:
                text = fileread.read()
            compressed = compress(text)
            with open(directory + "_compressed", "wb") as filesave:
                filesave.write(compressed)
            print(f"Wrote {len(compressed)} bytes to {directory}_compressed")
        else:
            with open(directory, "rb") as fileread:
                data = fileread.read()
            decompressed = decompress(data)
            with open(directory + "_decompressed", "w", encoding="utf-8") as filesave:
                filesave.write(decompressed)
            print(f"Wrote {len(decompressed)} chars to {directory}_decompressed")
    else:
        while True:
            action = input("Compress or decompress (or q to quit)? [c/d/q]: ").strip().lower()
            if action == 'q':
                break
            elif action == 'c':
                text = input("Give me the text you want to compress: ")
                try:
                    compressed_bytes = compress(text)
                except ValueError as e:
                    print(e)
                    continue
                print("Compressed (hex):", compressed_bytes.hex())
                print(f"Original chars: {len(text)}  Compressed bytes: {len(compressed_bytes)}")
            elif action == 'd':
                hex_text = input("Give me the compressed hex value you want to decompress: ").strip()
                try:
                    data = bytes.fromhex(hex_text)
                    decompressed_text = decompress(data)
                except (ValueError, EOFError) as e:
                    print(f"Couldn't decompress that: {e}")
                    continue
                print("Decompressed:", decompressed_text)
            else:
                print("Please enter 'c', 'd', or 'q'.")
				
