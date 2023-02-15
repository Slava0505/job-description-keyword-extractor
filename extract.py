from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
model_name = "models/keyT5-custom" # or 0x7194633/keyt5-base
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def logging(text_message = 'Something went wrong'):
    print(text_message)
    
import fire
import os

class Extractor(object):
    """A simple calculator class."""

    def extract(self, text, **kwargs):
        inputs = tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
        s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
        s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
        s = [el for el, _ in groupby(s)]
        s = list(set(s))
        return s
    
    def text(self, text = "testing/example.txt"):
        if len(text)<5:
            logging("It's doesn't look like path or text")
            exit()
        elif text[-4:] == '.txt':
            path = text
            if not os.path.exists(path):
                logging("File doesn't exist")
                exit()
            text = open(path).read()
        else:
            text = text
        
        extracted = self.extract(text, top_p=1.0, max_length=64)
        print(extracted)
        
        
if __name__ == '__main__':
    fire.Fire(Extractor)
