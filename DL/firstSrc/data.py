import pandas as pd
from PIL import Image
import numpy as np
import torch 
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

path = "first_crop_classification/data/Crop_details.csv"


class MyData(Dataset):
    def __init__(self,path):
        df = pd.read_csv(path)  
        
        self.images, self.label, self.name = df['path'], np.array(df['croplabel']), df['crop']
        self.transform = transforms.Compose([

            transforms.Resize((128, 128)), 
            # transforms.Grayscale(), 
            transforms.ToTensor()

        ])
    
    def change_paths(self, name):
        name = name.split('/')
        name = name[3:]
        name = "/".join(name)
        return 'first_crop_classification/data/'+name

    def __len__(self):
        return len(self.label)

    def __getitem__(self, xid):
        img = self.transform(Image.open(self.change_paths(self.images[xid])))
        label = self.label[xid]
        return img, label, self.name[xid]


if __name__ == "__main__":
    data = MyData(path)
    image, label, name = data[400]
    print(label, name)
    transforms.ToPILImage()(image).show()
    
