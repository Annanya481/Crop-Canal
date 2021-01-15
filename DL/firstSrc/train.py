from data import MyData
from model import Model
from torch import nn as nn 
from torch.utils.data import DataLoader
import torch 
from tqdm import tqdm 

path = "first_crop_classification/data/Crop_details.csv"
data = MyData(path)
train_dl = DataLoader(data, batch_size=32, shuffle=True, num_workers=2)

model = Model(in_channel=3, out_channel=32)
loss_fn = nn.CrossEntropyLoss()
optim = torch.optim.Adam(model.parameters(), lr=0.001)

def accuracy(pred,y):
    out = torch.log_softmax(pred,dim=1)
    _,predictions = torch.max(out,dim=1)

    correct = (predictions==y).float()
    
    acc = correct.sum()/len(correct)

    return acc


def train(model=model, train_dl=train_dl, loss_fn=loss_fn, optim=optim):
    epoch_loss = 0
    model.train()
    epoch_acc = 0
    for x, y, _ in tqdm(train_dl, total=len(train_dl), leave=False):
        optim.zero_grad()

        model_out = model(x)
        loss = loss_fn(model_out, y)
        print(model_out.shape, y.shape)
        acc = accuracy(model_out, y).item()

        loss.backward()

        optim.step()

        epoch_loss += loss.item()
        epoch_acc += acc
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
    return epoch_loss/len(train_dl), epoch_acc/len(train_dl)

if __name__ == "__main__":
    
    for epoch in range(10):
        loss, acc = train()
        print(f'LOSS: {loss} EPOCH: {epoch}, ACC: {acc}')


    torch.save(model.state_dict(), f'MODEL_{epoch}.pt')
    # if epoch%10==0:
    #     torch.save(model.state_dict(), f'MODEL_{epoch}.pt')