#!/usr/bin/env python3
import struct, zlib, math

def make_png(size):
    bg = (26, 58, 92)
    fg = (255, 255, 255)
    pixels = []
    cx, cy, r = size//2, size//2, size*0.38
    pad = size * 0.18
    for y in range(size):
        row = []
        for x in range(size):
            # circle background
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if dist <= r:
                row.extend(fg)
            else:
                row.extend(bg)
        pixels.append(bytes([0]) + bytes(row))

    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    raw = b''.join(pixels)
    compressed = zlib.compress(raw, 9)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    with open(f'/home/claude/sindooa-pwa/icons/{name}', 'wb') as f:
        f.write(make_png(size))
    print(f'생성완료: {name}')
