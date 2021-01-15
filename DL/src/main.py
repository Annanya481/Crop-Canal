from data import getData
from model import Model
from torch import nn as nn 
from torch.utils.data import DataLoader
import torch 
from tqdm import tqdm 


model = Model(in_channel=3, out_channel=32)
loss_fn = nn.BCEWithLogitsLoss()
optim = torch.optim.Adam(model.parameters(), lr=0.001)
train_dl = getData(batch_size=32, shuffle=True)

def accuracy(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum/y_test.shape[0]
    acc = torch.round(acc * 100)
    
    return acc
def train(model=model, train_dl=train_dl, loss_fn=loss_fn, optim=optim):
    epoch_loss = 0
    model.train()
    epoch_acc = 0
    for x, y in tqdm(train_dl, total=len(train_dl), leave=False):
        optim.zero_grad()

        model_out = model(x)
        y = y.unsqueeze(1)
        y = y.type(torch.float)
        
        loss = loss_fn(model_out, y)
        acc = accuracy(model_out, y).item()

        loss.backward()

        optim.step()

        epoch_loss += loss.item()
        epoch_acc += acc
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
    return epoch_loss/len(train_dl), epoch_acc/len(train_dl)

if __name__ == "__main__":
    
    for epoch in range(15):
        loss, acc = train()
        print(f'LOSS: {loss} EPOCH: {epoch}, ACC: {acc}')


    torch.save(model.state_dict(), f'MODEL_{epoch}.pt')
    # if epoch%10==0:
    #     torch.save(model.state_dict(), f'MODEL_{epoch}.pt')