import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer

from train_and_eval_model import training, evaluate
from BertClassifier import BertClassifier
from test_model import predict_bert


tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
print('Обучить модель - 0')
print('Загрузить модель - 1')
if int(input()) == 0:
    # prepare dataset
    df = pd.read_csv('/../data/pharse_dataset.csv').drop('Unnamed: 0', axis=1)
    df = df.dropna().reset_index(drop=True)
    df_train, df_val, df_test = np.split(df.sample(frac=1, random_state=42),
                                         [int(.8 * len(df)), int(.9 * len(df))])
    print(len(df_train), len(df_val), len(df_test))
    EPOCHS = 5
    model = BertClassifier()
    LR = 1e-6
    training(model, df_train, df_val, LR, EPOCHS)
    evaluate(model, df_test)
    torch.save(model, 'src/../data/model_bert_nlp.pt')
else:
    model = torch.load('src/../data/model_bert_nlp.pt', map_location='cpu')
    model.eval()

while True:
    print("Введите предложение: ")
    predict_bert(input(), model, tokenizer)
