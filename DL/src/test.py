from model import Model
import torch 
from torchvision import transforms
import numpy as np 

model = Model(in_channel=3, out_channel=32)
model.load_state_dict(torch.load('rice_crop/src/modelrice.pt'))

transform = transforms.Compose([

            transforms.Resize((200, 200)), 
            transforms.CenterCrop(150), 
            transforms.ToTensor()

        ])
from PIL import Image
model.eval()

img_to_model = transform(Image.open('rice_crop/data/Rice Seed Dataset/Healthy_Images/healthy (11).jpg'))
with torch.no_grad():
    model_out = model(img_to_model.unsqueeze(0))

print(model_out)
print(model_out[0].item())
if model_out[0].item() > 0.5:
    print("unhealthy")
    
else:
    print("healthy")
