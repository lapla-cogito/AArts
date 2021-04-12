from PIL import Image, ImageDraw,ImageFont
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
import cgitb,io,sys


def main():
  #isError
  cgitb.enable()
  make_AA('image.png')

def make_map(str_):
    l=[]
    font = ImageFont.truetype('MSGOTHIC.TTF', 20)
    for i in str_:
        im = Image.new("L",(30,30),"white")
        draw = ImageDraw.Draw(im)
        draw.text((0,0),i,fill='white',font=font)
        l.append(np.asarray(im).mean())
    l_as=np.argsort(l)
    lenl=len(l)
    l2256=np.r_[np.repeat(l_as[:-(256%lenl)],256//lenl),np.repeat(l_as[-(256%lenl):],256//lenl+1)]
    chr_map=np.array(str_)[l2256]
    return chr_map

def out(chr_map,imarray,out_path):
    aa=chr_map[imarray].tolist()
    with open(out_path,"w") as f:
        for i in range(len(imarray)):f.write(''.join(aa[i])+"\n")

def make_AA(file_path,str_='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!?"#$%&\'({[+-*/,.:;<=@^_`|~ ',width=1000,out_path="res.txt",isFW=False):
    imag=Image.open(file_path).convert('L')
    if isFW:str_=list(str_.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})))
    else:str_=list(str_)
    imarray=np.asarray(imag.resize((width,width*imag.height//imag.width//(2-int(isFW)))))
    out(make_map(str_),imarray,out_path)



if __name__ == "__main__":
    main()
