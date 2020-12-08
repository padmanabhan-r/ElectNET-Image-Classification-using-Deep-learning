# Load Data from MongoDB to create Training and Validation Data
from pymongo import MongoClient
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import time
import os
import shutil
import copy
import PIL
import warnings
from inference.ElectNet import ElectNet_50
warnings.filterwarnings("ignore")
from mongo_dataloader import DatasetDB


def train_model(data_loaders, dataset_sizes, model, criterion, optimizer, scheduler, num_epochs=25):
    best_loss = 1.0
    since = time.time()

    best_model_wts = model.state_dict()
    best_acc = 0.0
    

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)
        for phase in ['train', 'val']:
            if phase == 'train':
                scheduler.step()
                model.train(True)  # Set model to training mode
            else:
                model.train(False)  # Set model to evaluate mode
                
            running_loss = 0.0
            running_corrects = 0
            
            for data in data_loaders[phase]:
                inputs, labels = data
                labels = torch.tensor(list(map(lambda x: classes[x.lower().replace(" ","_")], labels)))
                if use_gpu:
                    inputs = Variable(inputs.cuda())
                    labels = Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()
                outputs = model(inputs)
                _, preds = torch.max(outputs.data, 1)
                loss = criterion(outputs, labels)
                
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
     
                # statistics
                running_loss += loss.item()
      

            epoch_loss = running_loss / dataset_sizes[phase]
            print('{} Loss: {:.4f}'.format(phase, epoch_loss))
            is_best = False
        
            if phase == 'val' and epoch_loss <= best_loss:
                best_loss = epoch_loss
                best_model_wts = copy.deepcopy(model.state_dict())
                is_best = True
   
            save_checkpoint({
                'epoch': epoch + 1,
                'state_dict': model.state_dict(),
                'best_prec1': epoch_loss
            }, is_best, epoch)

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Loss: {:4f}'.format(best_loss))
    # load best model weights
    model.load_state_dict(best_model_wts)
    return model
  
def save_checkpoint(state, is_best, epoch, filename='checkpoint.pth'):
    epoch = epoch + 1
    torch.save(state, str(epoch)+filename)
    if is_best:
        shutil.copyfile(str(epoch)+filename, 'model_best.pth')

#Image Categories
classes = {"bluetooth_speaker":0,
            "camera":1,
            "earphone":2,
            "gaming_console":3,
            "home_audio_speaker":4,
            "laptop":5,
            "memory_card":6,
            "mobile":7,
            "over_ear_headphone":8,
            "pendrive":9,
            "power_bank":10,
            "printer":11,
            "router":12,
            "smart_watch":13,
            "tablet_or_ereader":14,
            "usb_cable":15,
            "wireless_mouse":16,
          }

#Create Trainloader and Validation Loader
trainset = DatasetDB(set_name='TR')
trainloader = DataLoader(dataset=trainset, batch_size=8, shuffle=True)
valset = DatasetDB(set_name='TE')
testloader = DataLoader(dataset=valset, batch_size=8, shuffle=True)

use_gpu = torch.cuda.is_available()

data_loaders = {"train": trainloader, "val": testloader}
dataset_sizes = {'train':len(trainset), 'val':len(valset)}

model_ft = ElectNet_50()

#Check if GPU is available
if use_gpu:
    model_ft = model_ft.cuda()

criterion = nn.CrossEntropyLoss()

# Observe that all parameters are being optimized
optimizer_ft = optim.SGD(model_ft.parameters(),lr=0.01, momentum=0.9)

# Decay LR by a factor of 0.1 every 7 epochs
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

# train model
print("Training Model")
print()
model_ft = train_model(data_loaders,dataset_sizes, model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                       num_epochs=5)