def logging(text_message = 'Something went wrong'):
    print(text_message)
    
from datetime import datetime
import time
from tqdm.auto import tqdm, trange
BATCH_SIZE = 6


start_loading_time = datetime.now()

logging("The model loadnig..")
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
model_name = "models/keyT5-custom" # or 0x7194633/keyt5-base
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name).to('cuda:0')

logging(f"The model was loaded in {datetime.now() - start_loading_time}")

    
from itertools import groupby
import fire
import os
import pandas as pd

class Extractor(object):
    """An Extractor class."""
    
    def extract(self, text, **kwargs):
        inputs = tokenizer(text, return_tensors='pt').to(model.device)
        with torch.no_grad():
            hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
        s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
        s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
        s = [el for el, _ in groupby(s)]
        s = list(set(s))
        return s
    
    def batch_extract(self, batch_texts, **kwargs):
        batch_texts = list(batch_texts)
        inputs = tokenizer(batch_texts, return_tensors='pt', padding=True).to(model.device)
        with torch.no_grad():
            hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
        
        output = list()
        for i in range(len(batch_texts)):
            s = tokenizer.decode(hypotheses[i], skip_special_tokens=True)
            s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
            s = [el for el, _ in groupby(s)]
            s = list(set(s))
            output.append(s)
        return output
    
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
        
        batch_size = BATCH_SIZE
        is_incomplete_batch = len(test_df)%batch_size != 0
        
        extracted_key_skills = []
        for i in tqdm(range(0, int(len(test_df) / batch_size)+is_incomplete_batch)):
            
            batch_texts = test_df.iloc[i * batch_size: (i + 1) * batch_size].description
            
            batch_extracted = self.batch_extract(batch_texts, top_p=1.0, max_length=64)
            batch_extracted = [';'.join(extracted) for extracted in batch_extracted]
            extracted_key_skills += batch_extracted
            
        test_df['extracted_key_skills'] = extracted_key_skills
        logging(f"Extaction was ended in {datetime.now() - start_extraction_time}")
        
        result_path = path.replace('.csv', '_result.csv')
        test_df.to_csv(result_path, index = False)
        logging(f"Result file was saved in {result_path}")
        logging(self.get_analysis_results(test_df))
        
        
    def get_analysis_results(self, test_df):
        test_df['extracted_key_skills_list'] = test_df['extracted_key_skills'].str.split(';')
        top_key_skills = test_df['extracted_key_skills_list'].apply(pd.Series).stack().reset_index(drop=True).value_counts().iloc[:5]
        median_len = int(test_df['extracted_key_skills_list'].apply(len).median())

        result_log = ''
        result_log+=f'Num of vacancies: {len(test_df)}\n'
        result_log+=f'Median num of ectracted key_skills: {median_len}\n'
        result_log+='Top of ectracted key_skills in current set of vacancies:\n'
        result_log+=top_key_skills.to_string()

        
        return result_log
        
if __name__ == '__main__':
    fire.Fire(Extractor)