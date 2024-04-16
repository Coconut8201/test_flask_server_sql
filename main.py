from flask import Flask, request, jsonify
import os
import pymysql

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/data"

def database_R(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='password', db='aaa', charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

@app.route('/v1/uploadVideo', methods=['POST'])
# @authorize_and_log
def upload_file():
   """
   Upload a .mp4 file to the server.

   Returns:
      JSON response: Success message with file path if the file is uploaded successfully,
                     error message otherwise.
   """
     
    # 確保請求中有檔案
   if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

   file = request.files['file']
   #確保用戶選擇了檔案
   if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
   #確保檔案是.mp4格式
   if file and file.filename.endswith('.mp4'):
        # 指定檔案儲存路徑
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            print(f"upload_folder = {upload_folder}")
        file_path = os.path.join(upload_folder, file.filename)
        # 儲存檔案至伺服器中
        file.save(file_path)     
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
   else:
        return jsonify({'error': 'File must be in .mp4 format'}), 400



@app.route('/v1/getData', methods=['GET'])
def get_data():
   """
   Retrieve all data from the database.

   Returns:
       JSON response: All data from the database.
   """
   sql = "select * from app_info"  # 請替換成你的資料庫表格名稱
   data = database_R(sql)
   return jsonify(data), 200





if __name__ == '__main__':
   app.run(debug=True)
