import os
import tornado.web
import json
import uuid
import sqlite3
from tornado.ioloop import IOLoop
from pyulog import ULog
from helper import get_log_filename, load_ulog_file, get_total_flight_time, get_airframe_name
from config import get_db_filename
from .common import CustomHTTPError, TornadoRequestHandlerBase

class UploadLogAPIHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            print("Received request:", self.request)
            print("Arguments:", self.request.arguments)
            print("Files:", self.request.files)
            
            if 'filearg' not in self.request.files:
                raise ValueError("No file found in request")
            
            file_obj = self.request.files['filearg'][0]
            filename = file_obj['filename']
            print(f"File received: {filename}")
            
            log_id = str(uuid.uuid4())
            new_file_name = get_log_filename(log_id)
            print(f"Directory exists: {os.path.exists(os.path.dirname(new_file_name))}")
            print(f"Can write to directory: {os.access(os.path.dirname(new_file_name), os.W_OK)}")
            
            with open(new_file_name, 'wb') as f:
                f.write(file_obj['body'])
            print(f"File saved as: {new_file_name}")
            
            self.write({"status": "success", "message": "Log uploaded successfully", "log_id": log_id})
        
        except Exception as e:
            print("Error during file upload:", e)
            self.set_status(500)
            self.write(f"<html><title>Error 500</title><body>HTTP Error 500: {str(e)}</body></html>")
