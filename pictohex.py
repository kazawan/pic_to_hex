import os 
import sys
import shutil
from PIL import Image
import time




source_path = ''
output_path = ''
main_path =  os.path.dirname('./') 

for i in range (len(sys.argv)):
    if sys.argv[i] == '-i':
        source_path = sys.argv[i+1]
            
    if sys.argv[i] == '-o':

        output_path = sys.argv[i+1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)

print('Source path: ' + source_path)    
print('output_path: ' + output_path)

shutil.copy(source_path, main_path)

filename = source_path.split('\\')[-1]
print('filename: ' + filename)  



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

dist_filename = 'pic_' + filename.split('.')[0] + '_' + str(imgWidth) + 'x' + str(imgHeight) + '.h'
dict = open(dist_filename, 'a')
dict.write('/** \n')
dict.write(' * @file ' + dist_filename + '\n')
dict.write(' * @brief ' + filename + '的RGB565格式数据 \n')
dict.write(' * @version 0.1 \n')
dict.write(' * @width' + str(imgWidth) + '\n')
dict.write(' * @height' + str(imgHeight) + '\n')
dict.write(' * \n')
dict.write(' */ \n')
dict.write('\n')

dict.write('const long' + ' ' + dist_filename.split('.')[0] + '[] = {' + '\n')



for i in range(len(d)):
    dict.write(d[i])
    dict.write(',')
    print(d[i], end=',')

    if i % imgWidth == imgWidth - 1:
        print() # 换行

dict.write('};')

dict.close()

shutil.move(dist_filename, output_path)

# 删除源文件
os.remove(filename)

os.startfile(output_path)
