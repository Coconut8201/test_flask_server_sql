from flask import Flask, request, jsonify
import os
import pymysql
from datetime import datetime 

app = Flask(__name__)

# sql 資料庫設定
def database_R(sql):
    db = pymysql.connect(host='localhost', user='root', passwd='password', db='aaa', charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    if "INSERT" in sql.upper():
        row_count = cursor.rowcount
        db.commit()  # 確保資料庫的變更被提交
        
        # 如果受影響的行數大於0，表示INSERT語句成功
        if row_count > 0:
            message = f"{row_count} rows inserted."
        else:
            message = "No rows inserted."
    else:
        message = cursor.fetchall()
    
    db.close()
    
    return message

# 新增sql table UploadVideo video_input 的資料
def add_sqldata_video_input(user_id: str, video_path: str):
    # table name = UploadVideo
    sql_insert = f""" 
    INSERT INTO UploadVideo (UID, user_id, upload_time, video_server_path)
    VALUES ('{datetime.now().strftime("%Y%m%d%H%M%S")}', '{user_id}', '{datetime.now().strftime("%Y-%m-%d")}', '{video_path}');
    """
    sql_select = "SELECT * FROM UploadVideo;"
    
    data_insert = database_R(sql_insert)   
    data_select = database_R(sql_select)
    
    response_data = {
        "insert_result": data_insert,
        "select_result": data_select
    }
    
    return jsonify(response_data), 200

# 將影片上傳到 server 中(main)
@app.route('/v1/uploadVideo', methods=['POST'])
# @authorize_and_log
def upload_file():
    """
    Upload a .mp4 file to the server.
    
    @param {string} user_id - The ID of the user uploading the file.
    
    @return {JSON} - A JSON response indicating the upload status and file path.
    
    - If the file is uploaded successfully, a success message and the file path will be returned.
    - If there is no file part in the request, an error message will be returned.
    - If no file is selected, an error message will be returned.
    - If the file format is not .mp4, an error message will be returned.
    """

    user_id = request.args.get('user_id')

    # 確保請求中有檔案
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.mp4'):
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4")
        print(f"file_path = {file_path}")
        absolute_path = os.path.abspath(file_path)
        file.save(file_path)
        
        add_sqldata_video_input(str(user_id), absolute_path)
        
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
    else:
        return jsonify({'error': 'File must be in .mp4 format'}), 400
   



# 根據使用者id 調用影片資料
@app.route('/v1/get_usr_videoData', methods=['GET'])
def get_data():
    """
    Retrieve video data from the database based on the specified user ID.
    
    @param {string} user_id - The ID of the user whose video data needs to be retrieved.
    
    @return {JSON} - A JSON response containing the video data for the specified user.
    
    - If the user ID is provided and matches records in the database, the corresponding video data will be returned.
    - If the user ID is not provided or does not match any records, an empty array will be returned.
    """
    user_id = request.args.get('user_id')
    sql = f"SELECT * FROM UploadVideo WHERE user_id = '{user_id}';"
    data = database_R(sql)
    return jsonify(data), 200



# 其他需要用到sql 時可以下這個指令
@app.route('/v1/setting_sql',methods=['GET'])
def setting_sql():
     """
     # table name = UploadVideo
     Modify the data type of 'user_id' column in the 'video_input' table.
     
     This function alters the 'user_id' column in the 'video_input' table to be of type 'varchar(255)'.
     
     @return {JSON} - A JSON response containing the execution result of the SQL query.
     
     - If the SQL query is executed successfully, a success message will be returned.
     - If there is an error during the execution of the SQL query, an error message will be returned.
     """  
     
     sql = f""" 
     ALTER TABLE UploadVideo
     MODIFY user_id varchar(255);
     """
     
     data = database_R(sql)
     return jsonify({f"data = {data}"}), 200


if __name__ == '__main__':
   app.run(debug=True)
