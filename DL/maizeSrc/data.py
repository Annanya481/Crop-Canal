from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader

def getData():
    trans = transforms.Compose([
                                     transforms.Resize((200,200)),
                                     transforms.CenterCrop(150),
                                     transforms.ToTensor()
                                    ])

    data = ImageFolder(root='/home/aradhya/Desktop/hacks/train', transform=trans)
    print(data.class_to_idx)
    traindl = DataLoader(data, batch_size=1, shuffle=True)
    return traindl
