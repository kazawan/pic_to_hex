import os 
import sys
import shutil
from PIL import Image
import time
import art
from rich.console import Console
from rich.text import Text
from rich.progress import track

os.popen('cls') # 清屏

logo = "PIC_TO_HEX"
print(art.text2art(logo, font='small'))

console = Console()

version = '1.0.0'





source_path = ''
output_path = ''
main_path =  os.path.dirname('./') 
argv_int = 0




for i in range (len(sys.argv)):
    if sys.argv[i] == '-i':
        argv_int += 1
            
    if sys.argv[i] == '-o':
        argv_int += 1
    if sys.argv[i] == '-v':
        console.print('Version: ' + version,style="bold green")
        sys.exit(1)

if argv_int != 2 or not sys.argv[1:]:
    console.print("⛔ Usage: pictohex [-i source_path] [-o output_path]",style="bold red")
    sys.exit(1)
else:
    for i in range (len(sys.argv)):
        if sys.argv[i] == '-i':
            source_path = sys.argv[i+1]
                
        if sys.argv[i] == '-o':

            output_path = sys.argv[i+1]
            if not os.path.exists(output_path):
                os.makedirs(output_path)

console.print('Source path: ' + source_path,style="bold green")    
console.print('output_path: ' + output_path,style="bold green")


if not os.access(source_path, os.F_OK):
    console.print('File not exists',style="bold red")
    sys.exit(1)

shutil.copy(source_path, main_path)

filename = source_path.split('\\')[-1]
console.print('filename: ' + filename,style="bold green")  



#check if exists file
# time.sleep(1)
img = Image.open(filename)
imgWidth, imgHeight = img.size
img = img.convert("RGB")

d = {}
d_index = -1

def RGB_to_Hex(rgb):
    RGB = rgb.split(',')
    color = '0x'
    for i in RGB:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
#     print(color)
    return color


for h in range(imgHeight):
    for w in range(imgWidth):
        d_index += 1
        colors = img.getpixel((w, h))
        d[d_index] = RGB_to_Hex(str(colors).strip('()'))

localtime = time.asctime( time.localtime(time.time()) )

dist_filename = 'pic_' + filename.split('.')[0] + '_' + str(imgWidth) + 'x' + str(imgHeight) + '.h'
dict = open(dist_filename, 'a')
dict.write('/** \n')
dict.write(' * @file ' + dist_filename + '\n')
dict.write(' * @brief ' + filename + '的RGB565格式数据 \n')
dict.write(' * @version ' + version +  '\n')
dict.write(' * @width' + str(imgWidth) + '\n')
dict.write(' * @height' + str(imgHeight) + '\n')
dict.write(' * @date ' + localtime)
dict.write(' * \n')
dict.write(' */ \n')
dict.write('\n')

dict.write('const long' + ' ' + dist_filename.split('.')[0] + '[] = {' + '\n')



for i in track(range(len(d)),description="Converting..."):
    dict.write(d[i])
    dict.write(',')
    print(d[i], end=',')

    if i % imgWidth == imgWidth - 1:
        print() # 换行

dict.write('};')

dict.close()


dist_path = output_path + '\\' + dist_filename

if os.access(dist_path, os.F_OK):
    console.print('File exists',style="bold red")
    input = input('Do you want to overwrite it? (y/n)')
    if input == 'y' or input == 'Y':
        os.remove(dist_path)
    elif input == 'n' or input == 'N':
        os.remove(filename)
        os.remove(dist_filename)
        console.print('❌ Exit',style="bold red")
        os.startfile(output_path)
        sys.exit(1)

    

shutil.move(dist_filename, output_path)

# 删除源文件
os.remove(filename)
os.startfile(output_path)

console.print('🍻 Done',style="bold green")
sys.exit(1)


