import os
import sys
from PIL import Image
from unit import endStr,pictohex
import art
from rich.progress import track
from rich.console import Console

console = Console()

os.system('cls') # 清屏
logo = "PIC.TO.HEX.DIR"
print(art.text2art(logo, font='small'))
source_path = ''
endString = ".png"
version = '1.0.0'
argv_int = 0
for i in range (len(sys.argv)):
    if sys.argv[i] == '-i':
        argv_int += 1
    if sys.argv[i] == '-b':
        argv_int += 1
    if sys.argv[i] == '-v':
        console.print('Version: ' + version,style="bold blue")
        sys.exit(1)

if argv_int == 0 or not sys.argv[1:]:
    console.print("⛔ Usage: pictohex [-i source_path] [-o output_path]",style="bold red")
    sys.exit(1)
else:
    for i in range (len(sys.argv)):
        if sys.argv[i] == '-i':
            source_path = sys.argv[i+1]
        if sys.argv[i] == '-b':
            endString = sys.argv[i+1]


filepath = source_path
dir_filename = os.listdir(filepath)

document = []
documentLen = 0

for i in range(len(dir_filename)):
    if endStr(dir_filename[i],endString):
        file_array_path = filepath + "\\" + dir_filename[i]
        document.append(file_array_path)
        documentLen += 1


dist_dir = filepath + "\\dist"
if not os.access(dist_dir, os.F_OK):
    os.mkdir(dist_dir)

dist_hex_file = dist_dir + "\\hex.h"
hex_file = open(dist_hex_file,'a')
hex_file.write('/** \n')
hex_file.write(' * @file hex.h \n')
hex_file.write(' * @brief 图片的RGB565格式数据 \n')
hex_file.write(' * @version 1.0 \n')
hex_file.write(' * \n')
hex_file.write(' */ \n')



for i in track(range(documentLen),description="Processing..."):
    pictohex(document[i],hex_file)

#close file
hex_file.close()
console.print('🍻 Done',style="bold green")
os.startfile(dist_dir)