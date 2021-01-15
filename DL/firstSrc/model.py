import torch 
from data import MyData
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
                                    nn.Linear(64512, 5)

                                )   

    def forward(self, image):
        return self.model(image)

if __name__ == "__main__":
    path = "first_crop_classification/data/Crop_details.csv"
    image, _, _ = MyData(path)[0]
    model = Model(3,32)
    

    image = image.unsqueeze(0)
    print(model(image).shape)



