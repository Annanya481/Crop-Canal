import torch.nn as nn
import torchvision


class firstModel(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(firstModel, self).__init__()
        
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

class riceModel(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(riceModel, self).__init__()
        
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
                                    nn.Linear(88800, 1),
                                )   

    def forward(self, image):
        return self.model(image)        


def ptModel(modelName):
    if modelName == "firstCrop":
        model = firstModel(in_channel=3, out_channel=32)
        return model
    
    model = riceModel(in_channel=3, out_channel=32)
    return model
