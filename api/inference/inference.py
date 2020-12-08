from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers.pytorch import create_endpoint
from model import load_electnet_model

def predict_category(model, input_data):
	from torchvision import transforms
	import torch 
	# import torch.nn as nn
	import io
	import numpy as np
	from PIL import Image
	# import torch.nn.functional as F
	
	classes = [
		"bluetooth_speaker",
		"camera",
		"earphone",
		"gaming_console",
		"home_audio_speaker",
		"laptop",
		"memory_card",
		"mobile",
		"over_the_ear_headphone",
		"pendrive",
		"power_bank",
		"printer",
		"router",
		"smart_watch",
		"tablet_or_ereader",
		"usb_cable",
		"wireless_mouse"
	]
	
	data_transform = transforms.Compose([
		transforms.Resize(224),
		transforms.RandomResizedCrop(224),
		transforms.RandomHorizontalFlip(),
		transforms.RandomRotation(0,45),
		transforms.RandomVerticalFlip(0.5),
		transforms.ToTensor(),
		transforms.Normalize(
			mean=[0.485, 0.456, 0.406],
			std=[0.229, 0.224, 0.225]
		)
	])
	model.train(False)
	img_data ={}
	result = []
	num_imgs = len(input_data)
	sizes = []
	for i in range(num_imgs):
		np_arr = np.array(Image.open(io.BytesIO(input_data[i])).convert('RGB'))
		img = Image.fromarray(np_arr.astype('uint8'), 'RGB')
		img = data_transform(img).unsqueeze_(0)
		output = model(img)
		result.append(classes[(torch.max(output,1)[1][0]).numpy()])
	return result

clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.connect()

create_endpoint(
	clipper_conn, 
	name='electnet', 
	version=2, 
	slo_micros=19000000, 
	input_type="bytes", 
	func=predict_category, 
	pytorch_model=load_electnet_model(), 
	pkgs_to_install=[
		'torch==0.4.1',
		'torchvision',
		'Pillow'
	]
)
