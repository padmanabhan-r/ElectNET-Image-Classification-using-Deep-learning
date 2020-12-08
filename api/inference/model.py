import ElectNet
import torch 

def load_electnet_model():
	model_weights = torch.load('./static_files/model_best_1.pth', map_location='cpu')['state_dict']
	model = ElectNet.ElectNet_50()
	model.load_state_dict(model_weights)
	return model