from PIL import Image

def endStr(s,endString):
    if s.endswith(endString):
        return True
    else:
        return False
    
def _RGB_to_Hex(rgb):
    RGB = rgb.split(',')
    color = '0x'
    for i in RGB:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
#     print(color)
    return color
    

def pictohex(item,hex_file):
    d={}
    d_index = -1
    filename = item.split('\\')[-1].split('.')[0]
    backfix = item.split('\\')[-1].split('.')[1]
    hex_file.write('//' + 'pictrue_' + filename + '.' + backfix + '\n')
    img = Image.open(item)
  
    imgWidth, imgHeight = img.size
    img = img.convert("RGB")
    
    for h in range(imgHeight):
        for w in range(imgWidth):
            d_index += 1
            colors = img.getpixel((w, h))
            d[d_index] = _RGB_to_Hex(str(colors).strip('()'))
    
    hex_file.write('const long' + ' ' + 'pic_' + filename + '[] = {' + '\n')

    for i in range(len(d)):
        hex_file.write(d[i])
        hex_file.write(',')
    
    hex_file.write('};')
    hex_file.write('\n')
    hex_file.write('\n')



