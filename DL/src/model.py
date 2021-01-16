import torch 
from data import getData
import torchvision
from torch import nn as nn 

class Model(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(Model, self).__init__()
        
        self.model =  nn.Sequential(
                                    nn.Conv2d(in_channel, out_channel, kernel_size=(3,3), padding=1),
                                    nn.MaxPool2d((2,2)), 
                                    nn.ReLU(),
                                    nn.Dropout(),
                                    nn.Conv2d(out_channel, out_channel*2, kernel_size=(3,3), padding=1),
                                    nn.MaxPool2d((3,2)), 
                                    nn.ReLU(),
                                    nn.Dropout(),
                                    nn.Conv2d(out_channel*2, out_channel*3, kernel_size=(3,3), padding=1), 
                                    nn.Flatten(), 
                                    nn.Linear(88800, 1)
                                )   

    def forward(self, image):
        return self.model(image)

if __name__ == "__main__":
    train_dl = getData(batch_size=32, shuffle=True)    
    model = Model(3,32)
    for image, y in train_dl:
        # image = image.unsqueeze(0)
        print(model(image).shape)
        break



