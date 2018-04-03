# -*- coding: utf-8 -*-
# @Date    : 2018-02-08 00:13:05
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

import hashlib
import random
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import logging
from subprocess import call
import glob
import os

def hash_string(string):
    if not string:
        string = ""
    #sha1加密
    m = hashlib.sha1()
    m.update(string)
    #返回加密的16进制数
    return m.hexdigest()
#默认随机生成4个数字或字母组合字符，长度可设置
def get_random_texts(length=4):
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    auth_text = ''
    for i in xrange(length):
        auth_text += random.choice(string)
    logging.info(auth_text)
    return auth_text
#生成验证码图片
def get_pic(text):
    #生成图片的尺寸
    size = (120,30)
    img = Image.new("RGB",size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGB")
    font=ImageFont.truetype(r"C:\Windows\Fonts\simsunb.ttf",26)
    distance = size[0]/len(text) #计算一个图片文字的合理间距
    #备选颜色
    colors = ['red','blue','darkviolet','orange','deeppink','purple','olive','green','lime']
    for i in range(len(text)):
        color = random.choice(colors) #随机选择一个颜色
        draw.text([i * distance,0], text[i],color,font=font)
    logging.info(text)
    
    for i in range(100):
        draw.point((random.randint(0,size[0]),random.randint(0,size[1])),fill=random.choice(colors))
    
    params = [
            1 - float(random.randint(1,2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1,10)) / 100,
            float(random.randint(1,2)) / 500,
            0.001,
            float(random.randint(1,2)) / 500
        ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
    img.save('verify.png')
def to_dict(params):
    if params.startswith('http://'):
        params = params.split('?')
    result = {}
    items = params.split('&')
    for item in items:
        key,value = item.split('=')
        result[key] = value
    return result

def to_mp4(input_file):
    """ 
        把视频文件统一转换成200kbps码率的mp4
    """
    postion = input_file.find('.')
    output_file = input_file.replace(input_file[postion:], '.mp4')
    cmd = '..\\ffmpeg.win32.exe -y -i {} -b:v 200k {}'.format(input_file, output_file)
    try:
        if os.path.exists(output_file):
            return true
        a = call(cmd,shell=True)
        if a == 1:
            logging.error('Failed to transfer video')
            logging.error(cmd)
            return False
        logging.info("Transfer finished")
        os.remove(input_file)
        return True
    except Exception,e:
        logging.error('Failed to transfer video')
        logging.error(e)
        return False

def get_page_seq(count, items=30):
    pages = (count - 1) / items + 1
    if pages > 1 and pages <= 11:
        pageseq = list(range(1,pages + 1))
    elif pages > 11:
        pageseq = list(range(1,10))
        pageseq += ['...',pages]
    else:
        pageseq = None

    return pageseq
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s: %(message)s",datefmt="%m/%d/%Y %p %I:%M:%S")
    #a = hash_string("")
    #print a
    #s = get_random_texts()
    #get_pic(s)
    #path = r'D:\web\5\*.wmv'
    #files = glob.glob(path)
    #print files

    #for i in files:
    #    to_mp4(i)
    print get_page_seq(31)