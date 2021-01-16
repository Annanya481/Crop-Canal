# from tensorflow.keras.models import load_model
from load_model import ptModel
import torch 
from torchvision import transforms
from PIL import Image
import numpy as np 


class predictMain():
    def __init__(self):
        self.firstModel = ptModel("firstCrop")
        self.riceModel = ptModel("riceModel")
    
        self.firstModel.load_state_dict(torch.load('models/Model_crop_prediction.pt'))
        self.firstModel.eval()

        self.fristTrans = transforms.Compose([

            transforms.Resize((128, 128)), 
            # transforms.Grayscale(), 
            transforms.ToTensor()
        ])

        self.riceTrans = transforms.Compose([
                transforms.Resize((200,200)),
                transforms.CenterCrop(150),
                transforms.ToTensor()
            ])


    def predict(self, firstimage, veri1, veri2, veri3, veri4, veri5):
        veri1 = Image.open(veri1)
        veri2 = Image.open(veri2)
        veri3 = Image.open(veri3)
        veri4 = Image.open(veri4)
        veri5 = Image.open(veri5)
        firstimage = self.fristTrans(Image.open(firstimage))
        
        with torch.no_grad():
            image_type = self.firstModel(firstimage.unsqueeze(0))
        cropType = np.argmax(image_type[0])
        cropName = None
        if cropType == 1:
            cropName = "maize"
        elif cropType == 2:
            cropName = "rice"
        elif cropType == 3:     
            cropName = "sugercare"

        if cropName:
            
            if cropName == "rice":
                self.riceModel.load_state_dict(torch.load('models/modelrice.pt'))
                self.riceModel.eval()
                with torch.no_grad():
                    veri1 = self.riceModel(self.riceTrans(veri1).unsqueeze(0))
                    veri2 = self.riceModel(self.riceTrans(veri2).unsqueeze(0))
                    veri3 = self.riceModel(self.riceTrans(veri3).unsqueeze(0))
                    veri4 = self.riceModel(self.riceTrans(veri4).unsqueeze(0))
                    veri5 = self.riceModel(self.riceTrans(veri5).unsqueeze(0))
                
            if cropName == "maize":
                self.maizeModel = self.riceModel
                self.maizeModel.load_state_dict(torch.load('models/modelMaize.pt'))
                self.maizeModel.eval()
                with torch.no_grad():
                    veri1 = self.maizeModel(self.riceTrans(veri1).unsqueeze(0))
                    veri2 = self.maizeModel(self.riceTrans(veri2).unsqueeze(0))
                    veri3 = self.maizeModel(self.riceTrans(veri3).unsqueeze(0))
                    veri4 = self.maizeModel(self.riceTrans(veri4).unsqueeze(0))
                    veri5 = self.maizeModel(self.riceTrans(veri5).unsqueeze(0))


            return cropName, veri1, veri2, veri3, veri4, veri5






        
        
                    
