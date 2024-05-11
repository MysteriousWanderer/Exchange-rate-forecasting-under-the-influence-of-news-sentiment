from transformers import AutoTokenizer, AutoModel
import torch
from torch import nn
from datasets import Dataset, concatenate_datasets
import evaluate
from tqdm import tqdm
from torch.utils.data import DataLoader


class BERT(nn.Module):
    def __init__(self, num_label):
        super().__init__()
        self.bert = AutoModel.from_pretrained("hfl/chinese-bert-wwm-ext")
        self.linear = nn.Linear(768, num_label)

    def forward(self, X):
        Y = self.bert(**X)
        return self.linear(Y.pooler_output)

'''
tokenizer = AutoTokenizer.from_pretrained("hfl/chinese-bert-wwm-ext")

dataset = Dataset.from_csv("../data/train_data.csv", cache_dir='../data')
dataset = dataset.remove_columns(("time", "num"))
tokenized_dataset = concatenate_datasets([dataset, Dataset.from_dict(tokenizer(dataset['title'], padding=True))], axis=1)
tokenized_dataset = tokenized_dataset.remove_columns('title')
tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
tokenized_dataset.set_format("torch")
train_dataloader = DataLoader(tokenized_dataset, shuffle=True, batch_size=128)

t_dataset = Dataset.from_csv("../data/test_data.csv", cache_dir='../data')
t_dataset = t_dataset.remove_columns(("time", "num"))
t_tokenized_dataset = concatenate_datasets([t_dataset, Dataset.from_dict(tokenizer(t_dataset['title'], padding=True))], axis=1)
t_tokenized_dataset = t_tokenized_dataset.remove_columns('title')
t_tokenized_dataset = t_tokenized_dataset.rename_column("label", "labels")
t_tokenized_dataset.set_format("torch")
test_dataloader = DataLoader(t_tokenized_dataset, shuffle=True, batch_size=128)
'''
# model = torch.load("../data/modelforsentiment.pkl")
model = BERT(num_label=3)
print(model)
exit(0)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
loss = nn.CrossEntropyLoss()
gpu = torch.device('cuda')
model.to(gpu)

ACC = 0.0
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    for batch in tqdm(train_dataloader):
        X = {k: v.to(gpu) for k, v in batch.items() if k != 'labels'}
        Y = batch['labels']
        Y = Y.to(gpu)
        outputs = model(X)
        L = loss(outputs, Y)
        L.backward()
        optimizer.step()
        optimizer.zero_grad()

    model.eval()
    metric = evaluate.load("accuracy")
    for batch in tqdm(test_dataloader):
        X = {k: v.to(gpu) for k, v in batch.items() if k != 'labels'}
        with torch.no_grad():
            outputs = model(X)
        predictions = torch.argmax(outputs, dim=-1)
        metric.add_batch(predictions=predictions, references=batch["labels"])
    acc = metric.compute()['accuracy']
    print(acc)
    if acc > ACC:
        torch.save(model, "../data/modelforsentiment.pkl")
        ACC = acc

