# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import random
import string
from datetime import timedelta
from model import predict_img
from cassandra_op import insert_data
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  
        #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        predict_res = predict_img(img)
        cttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        # 生成文件名
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        filename = ran_str + "%d.jpg" % int(time.time())
        imgpath = 'images/' + filename
        cv2.imwrite(os.path.join(basepath, 'static/images', filename), img)

        # 将结果插入数据库
        insert_data(imgpath,cttime,predict_res)
        
        return render_template('upload_ok.html',val1=time.time(),impath=imgpath,predictval=predict_res)
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    app.run(debug=True,port=8000,host='0.0.0.0')