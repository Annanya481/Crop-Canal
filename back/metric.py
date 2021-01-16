import torch 

def ptcalMetric(predictions):
    
    count = 0
    predictions = torch.tensor(predictions)
    probability = torch.sigmoid(predictions)
    print(probability)
    for prediction in probability:
        count+=prediction.item()
    

    return count/5
    
