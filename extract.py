
def logging(text_message = 'Something went wrong'):
    print(text_message)
    
from datetime import datetime
import time
from tqdm.auto import tqdm, trange


start_loading_time = datetime.now()

logging("The model loadnig..")
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
model_name = "models/keyT5-custom" # or 0x7194633/keyt5-base
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

logging(f"The model was loaded in {datetime.now() - start_loading_time}")

    
from itertools import groupby
import fire
import os
import pandas as pd

class Extractor(object):
    """An Extractor class."""
    
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
        logging("Extaction was started")
        start_extraction_time = datetime.now()
        extracted = self.extract(text, top_p=1.0, max_length=64)
        logging(f"Extaction was ended in {datetime.now() - start_extraction_time}")
        
        logging(extracted)
        
    def csv(self, path = "testing/example.csv"):
        if not os.path.exists(path):
            logging("File doesn't exist")
            exit()
        test_df = pd.read_csv(path)
        logging("Extaction was started")
        start_extraction_time = datetime.now()
        
        batch_size = 4  # сколько примеров показывем модели за один шаг
        
        
        extracted_key_skills = []
        for i in tqdm(range(len(test_df))):
            
            
            text = test_df.iloc[i].description
            extracted = self.extract(text, top_p=1.0, max_length=64)
            extracted = ';'.join(extracted)
            extracted_key_skills.append(extracted)
            
        test_df['extracted_key_skills'] = extracted_key_skills
        logging(f"Extaction was ended in {datetime.now() - start_extraction_time} seconds")
        
        result_path = path.replace('.csv', '_result.csv')
        test_df.to_csv(result_path, index = False)
        logging(f"Result file was saved in {result_path}")
        
        
        
if __name__ == '__main__':
    fire.Fire(Extractor)
