import torch.nn as nn
from torchvision import models

class ElectNet_50(nn.Module):
	def __init__(self):
		super(ElectNet_50, self).__init__()
		ResNet50 = models.resnet50(pretrained=True)
		modules = list(ResNet50.children())[:-1]
		backbone = nn.Sequential(*modules)

		# Create new layers
		self.backbone = nn.Sequential(*modules)
		self.fc1 = nn.Linear(2048, 1028)
		self.fc2 = nn.Linear(1028,512)
		self.fc3 = nn.Linear(512,34)
		self.dropout = nn.Dropout(p=0.5)
		self.fc4 = nn.Linear(34,17)
		self.fc5 = nn.Softmax()
		
	def forward(self, img):
		# Get the flattened vector from the backbone of resnet50
		out = self.backbone(img)
		# processing the vector with the added new layers
		out = out.view(out.size(0), -1)
		out = self.fc1(out)
		out = self.fc2(out)
		out = self.fc3(out)
		out = self.dropout(out)
		out = self.fc4(out)
		return self.fc5(out)