from PIL import Image, ImageDraw, ImageFont, ImageFile
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
import cgitb,io,sys
import cgi
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
#from werkzeug import secure_filename
from PIL import ImageFile 
ImageFile.LOAD_TRUNCATED_IMAGES = True
from werkzeug.utils import secure_filename

alex = set(['png', 'jpg'])
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def main():
  #isError
  cgitb.enable()
  print("Content-Type: text/html; charset=UTF-8")
  print("")
  make_AA()

def fileche(fname):
    return '.' in fname and \
        fname.rsplit('.', 1)[1] in alex

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        imgfile = request.files['imgfile']
        if imgfile and allowed_file(imgfile.filename):
            filename = secure_filename(imgfile.filename)
            imgfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imgurl = '/uploads/' + filename
            return render_template('index.html', img_url=img_url)
        else:
            return ''' <p>変換不可の拡張子です.(.png or .jpg)</p> '''
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
  with open('index.html','r') as file:
    html = file.read()
  file.closed
  aa=chr_map[imarray].tolist()
  with open('try.html','w') as html:
    for i in range(len(imarray)):html.write(''.join(aa[i])+"\n")

def make_AA(str_='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!?"#$%&\'({[+-*/,.:;<=@^_`|~ ',width=1000,out_path="res.txt",isFW=False):
    #form = cgi.FieldStorage()
    #img = form.getvalue("imagefile")
    #imag=Image.open(file_path).convert('L')
    img_file = request.files['img_file']
    filename = secure_filename(img_file.filename)
    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# 画像をアップロード先に保存する
    img_file.save(img_url)

    return render_template('index.html', result_img=img_url)
    if isFW:str_=list(str_.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})))
    else:str_=list(str_)
    imarray=np.asarray(img.resize((width,width*img.height//img.width//(2-int(isFW)))))
    out(make_map(str_),imarray,out_path)



if __name__ == "__main__":
    app.debug = True
    main()
