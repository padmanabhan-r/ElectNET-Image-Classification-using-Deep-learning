import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify, abort, make_response, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import time
import zipfile 
import shutil
import json
import base64
import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('ElecNet')

UPLOAD_FOLDER = 'upload'
# ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'zip'])
ZIPPED_EXTENSIONS = set(['zip'])
IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])
ALLOWED_EXTENSIONS = set([])
ALLOWED_EXTENSIONS.update(ZIPPED_EXTENSIONS)
ALLOWED_EXTENSIONS.update(IMAGE_EXTENSIONS)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class BadRequestException(Exception):
	status_code = 400

	def __init__(self, message):
		Exception.__init__(self)
		self.message = message

	def to_dict(self):
		return {
			'success': False,
			'message': self.message
		}


@app.errorhandler(BadRequestException)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


def files_allowed(filename, extentions):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in extentions


@app.route('/upload', methods=['POST'])
def file_upload():

	logger.info(ALLOWED_EXTENSIONS)
	if 'filepond' not in request.files:
		raise BadRequestException('No files uploaded.')
	
	file = request.files['filepond']
	if file.filename == '':
		raise BadRequestException('No file selected.')
	
	if not files_allowed(file.filename, ALLOWED_EXTENSIONS):
		raise BadRequestException('Please select only .png, .jpeg, .jpg files')
	
	ts = time.time()
	directory = os.path.join(app.config['UPLOAD_FOLDER'], str(ts))
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = secure_filename(file.filename)
	file_path = os.path.join(directory, filename)
	file.save(file_path)

	if files_allowed(file.filename, ZIPPED_EXTENSIONS):
		zip_ref = zipfile.ZipFile(file_path, 'r')
		zip_ref.extractall(directory)
		zip_ref.close()
		os.remove(file_path)
		files = os.listdir(directory)
		for file in files:
			file_path = os.path.join(directory, file)
			if os.path.isdir(file_path):
				shutil.rmtree(file_path)
			else:
				if not files_allowed(file, IMAGE_EXTENSIONS):
					os.remove(file_path)

	return jsonify({
		'success': True, 
		'directory': ts
	})


def query(filename, fullpath):
	url = "http://localhost:1337/electnet/predict"
	logger.info('Filename: ' + filename)
	logger.info('fullpath: ' + fullpath)
	file = os.path.join(fullpath, filename)
	req_json = json.dumps({
		"input": base64.b64encode(open(file, "rb").read()).decode()
	})
	headers = {'Content-type': 'application/json'}
	r = requests.post(url, headers=headers, data=req_json)
	output = r.json()
	logger.info(output)
	category = output['output']
	categories = category.split('_')
	# logger.info(' '.join(categories).title())
	return ' '.join(categories).title()


@app.route('/results/<directory>', methods=['GET'])
def get_results(directory):
	fullpath = os.path.join(app.config['UPLOAD_FOLDER'], directory)
	logger.info(fullpath)
	files = os.listdir(fullpath)
	images = []
	# model = inference.load_electnet_model('./model/model_best.pth')
	# model.train(False)
	for file in files:
		file_path = os.path.join(directory, file)
		filename = 'http://127.0.0.1:5000/upload/' + file_path
		category = query(file, fullpath)
		image = {
			"image": filename,
			"category": category
			# "category": inference.predict_class('./upload/'+file_path, model),
		}
		images.append(image)
	return jsonify(images)


@app.route('/upload/<path:path>')
def send_file(path):
	return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.after_request
def add_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', '*')
	response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE");
	return response


if __name__ == "__main__":
	app.secret_key = os.urandom(24)
	app.run(debug=True,host="0.0.0.0",use_reloader=False)
	CORS(app, expose_headers='Authorization')
