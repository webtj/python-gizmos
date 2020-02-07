from PIL import Image
import argparse
'''
将图片转为灰度文本格式
'''
# 命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')  # 输入文件
parser.add_argument('-o', '--output')  # 输出文件
parser.add_argument('--width', type=int, default=80)  # 输出字符画宽
parser.add_argument('--height', type=int, default=80)  # 输出字符画高

# 获取参数
args = parser.parse_args()
IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

# 首先将RGB转换成灰度值，再将灰度值转换成对应的字符
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
# ascii_char = list("b")

def get_char(r, g, b, alpha=256, as_c=ascii_char):
    # 判断 alpha 值
    if alpha == 0:
        return ' '
    # 获取字符集的长度，这里为 70
    length = len(as_c)
    # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
    # gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    # gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    # gray = (r * 30 + g * 59 + b * 11 + 50) / 100
    gray = (r * 313524 + g * 615514 + b * 119538) >> 20

    # 灰度值范围为 0-255，而字符集只有 70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    unit = (256.0 + 1) / length
    # 返回灰度值对应的字符
    return as_c[int(gray / unit)]


if __name__ == "__main__":
    # 打开图片调整高度
    im = Image.open(IMG)
    # Image.NEAREST 表示输出低质量的图片
    im = im.resize((WIDTH, HEIGHT),Image.NEAREST)

    txt = ""
    # 遍历每一行
    for i in range(HEIGHT):
        # 遍历每一列
        for j in range(WIDTH):
            # 获取每一行每一列的rgb值，getpixel获取坐标的rgb值，加上*作为元祖传入函数
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'
    print(txt)

    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open("output.txt", 'w') as f:
            f.write(txt)
