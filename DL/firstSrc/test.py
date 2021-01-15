from model import Model
import torch 
from torchvision import transforms
import numpy as np 

model = Model(in_channel=3, out_channel=32)
model.load_state_dict(torch.load('first_crop_classification/src/Model_crop_prediction.pt'))

transform = transforms.Compose([

            transforms.Resize((128, 128)), 
            # transforms.Grayscale(), 
            transforms.ToTensor()

        ])
from PIL import Image
model.eval()

img_to_model = transform(Image.open('first_crop_classification/data/kag2/wheat/wheat0002a.jpeg'))
with torch.no_grad():
    model_out = model(img_to_model.unsqueeze(0))

prob = torch.nn.Softmax(dim=1)(model_out)    
model_out = np.argmax(np.array(prob[0]))

if model_out == 0:
    print("jute")

elif model_out == 1:
    print("maize")

elif model_out == 2:
    print("rice")

elif model_out == 3:
    print("sugercane")

else:
    print("Wheat")



