# job description key skills extractor

Trained T5-large model for creating key skills from job description.  
Supported languages: ru


[Pretraining Large version](https://huggingface.co/0x7194633/keyt5-large)
|
[Pretraining Base version](https://huggingface.co/0x7194633/keyt5-base)




# Training

This command starts training on data/it_dataset_sample.csv
```bash
~$ python train.py
```

data/it_dataset_sample.csv
is set of 500 vacancies with key skills:

description | key_skills 
--- | ---
Твои задачи:  Разработка и поддержка технической, проектной и эксплуатационной документации по ГОСТ... | 	MS Visio;ГОСТ;Подготовка презентаций;Техническая документация;разработка нормативных документов;...
Компания «Технологии Успеха» - лидер рынка автоматизации гостинично-ресторанного бизнеса в ЮФО предлагает тебе стать частью нашего дружного коллектива... | 	Веб-программирование;JavaScript;CSS;MySQL;PHP5;PHP;Веб-дизайн;SQL;ООП;Yii;Разработка ПО;... 
Обязанности:  Дизайн и верстка полиграфической продукции (каталоги, буклеты, визитки, листовки, баннеры и пр.)... | Adobe Illustrator;Adobe Photoshop;Adobe InDesign;CorelDRAW;Графический дизайн;Microsoft office (Power Point; Word; Exсel);...

By default, you teach the keyT5-large 
You can change this line in train.py to teach T5-base
```python
raw_model = '0x7194633/keyt5-large' # или 0x7194633/keyt5-base
```


# Usage:

For the extraction test you can use:
```bash
~$ python extract.py text
```
By default it uses text in testing/example.txt file for extractions
```bash
['аналитическое мышление', 'ms powerpoint']
```
-----
For the extraction test from your text you can use:
```bash
~$ python extract.py text "your text"
```
or 
```bash
~$ python extract.py text path_to_txt_file
```
-----
To extract keywords from several texts at a time you need to create similar csv file:  

description | 
--- | 
vacancy1 |
vacancy2 |

And use 
```bash
~$ python extract.py csv path_to_csv_file
```
It'll generate result file 

description | extracted_key_skills
--- | ---
vacancy1 | skill1;skill2;...
vacancy2 | skill3;skill4;...

and output to the console
results:
```bash
Num of vacancies: 20
Median num of ectracted key_skills: 2
Top of ectracted key_skills in current set of vacancies:
adobe photoshop                      4
git                                  2
adobe indesign                       2
работа в условиях многозадачности    2
adobe illustrator                    2
```