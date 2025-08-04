import numpy as np
from PIL import Image
#Convert image into matrix
img = Image.open("lee_algorithm_test_map_multiple_targets.png").convert("RGB")
l, w = img.size
color_map = {
    (0, 0, 0): 'w',         # black
    (255, 0, 0): 't',       # red
    (0, 255, 0): 's',       # green
    (255, 255, 255): ' '    # white
}
a_t = []
for y in range(w):
    row = []
    for x in range(l):
        pixel = img.getpixel((x, y))
        char = color_map.get(pixel, '?')  # Use '?' for unknown color
        row.append(char)
    a_t.append(row)

a_t = np.array(a_t, dtype='U10')
a=a_t.copy()
i='0'
target=0
dir=[[1,0],[-1,0],[0,1],[0,-1]]
for r in range(l):
    for c in range(w):
        if(a[r][c]=='t'):
            target+=1
    
#Search for target
for x in range(target):
    for r in range(l):
        for c in range(w):
            if(a[r][c]=='s' or a[r][c]=='p'):
                a[r][c]='0'
                i='0'
    found = False
    while not found:
        for r in range(l):
            for c in range(w):
                if(a[r][c] == i):
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < l and 0 <= nc < w):
                            if (a[nr][nc] == ' '):
                                a[nr][nc] = str(int(i) + 1)
                            if (a[nr][nc] == 't'):
                                a[nr][nc] = 'p'
                                found = True
                                break
                if found:
                    break
        if found:
            break
        i = str(int(i) + 1)

#make path from target to source
    found=False  
    for x in range(int(i)+1):
        for r in range(l):
            for c in range(w):
                if(a[r][c]=='p'):
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < l and 0 <= nc < w):
                            if (a[nr][nc] == i):
                                a[nr][nc] = 'p'
                                i=str(int(i)-1)
                            if (a[nr][nc] == '0'):
                                a[nr][nc] = 'p'
                                found = True
                                break
            if found:
                break
        if found:
            break
    for r in range(l):
        for c in range(w):
            if(a[r][c]=='0'):
                a[r][c]='p'
            if(a[r][c]!='p' and a[r][c]!='w' and a[r][c]!='t'):
                a[r][c]=' '
            

for r in range(l):
    for c in range(w):
        if(a_t[r][c]=='s' or a_t[r][c]=='t'):
            a[r][c]=a_t[r][c]

#Convert Output matrix into Image
color_map_invert = {
    'w': (0, 0, 0),        # black
    ' ': (255, 255, 255),  # white
    's': (0, 255, 0),      # green
    't': (255, 0, 0)       # red
}

cell_size = 10
rows = len(a)
cols = len(a[0])

# Create a new image
img = Image.new("RGB", (cols * cell_size, rows * cell_size), "white")
pixels = img.load()

# Fill in each block
for y in range(rows):
    for x in range(cols):
        color = color_map_invert.get(a[y][x], (127, 127, 127))  # gray fallback
        for i in range(cell_size):
            for j in range(cell_size):
                pixels[x * cell_size + i, y * cell_size + j] = color

# Save as JPG
img.save("Output.jpg", "JPEG")