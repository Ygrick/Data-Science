import torch


def predict_bert(text, model, tokenizer):
    test_text = tokenizer(text, padding='max_length', max_length=50, truncation=True, return_tensors="pt")

    with torch.no_grad():
        mask = test_text['attention_mask'].to('cpu')
        input_id = test_text['input_ids'].squeeze(1).to('cpu')
        model.to('cpu')

        output = model(input_id, mask)
        label_of_edu = 'education' if output.argmax(dim=1).item() else 'not education'

        print(f'ВСЕ ВЫХОДЫ: {output[0]}')
        print(f'КЛАСС: {label_of_edu}')
