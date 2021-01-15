import torchvision
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

transforms = torchvision.transforms.Compose([
                torchvision.transforms.Resize((200,200)),
                torchvision.transforms.CenterCrop(150),
                torchvision.transforms.ToTensor()
])

def getData(batch_size, shuffle):
    data = ImageFolder(root="/home/aradhya/Desktop/hacks/rice_crop/data/Rice Seed Dataset", transform=transforms)
    print(data.class_to_idx)
    train_dl = DataLoader(data, batch_size=batch_size, shuffle=shuffle, num_workers=2)

    return train_dl





# from PIL import Image

# img = Image.open('rice_crop/data/Rice Seed Dataset/Healthy_Images/healthy (16).jpg') 
# small_img = torchvision.transforms.Resize((200,200))
# # small_img(img).show()

# torchvision.transforms.CenterCrop(150)(small_img(img)).show()