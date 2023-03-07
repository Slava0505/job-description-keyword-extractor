import pandas as pd


from flashtext.keyword import KeywordProcessor
keyword_processor = KeywordProcessor()
for key_skill in all_key_skills_counts_filtred.index:
    keyword_processor.add_keyword(key_skill)
    keyword_processor.add_keyword(key_skill)
    
    
keywords_found = keyword_processor.extract_keywords('Обязанности:  анализ документации и работа со статистикой; разработка нагрузочных скриптов (Java или C#) ; запуск тестов и анализ результатов, написание отчетов и составление документации; А также: разработка заглушек и эмуляторов, разработка утилит для генерации данных, работа с базами данных.  Требования:  уверенное знание одного из языков программирование: C/C++, Java, C#, Phython; умение работать с базами данных на уровне написания простейших SQL-запросов; знание архитектур приложений (толстый/тонкий клиент); возможность работать полный рабочий день.  Условия:  работа в молодом активном коллективе; конкурентная заработная плата, оформление по ТК РФ; постоянное обучение внутри компании; возможность профессионального роста; участие в тестировании ПО в крупных российских банках.    Первый этап - собеседование по онлайн.')
print(keywords_found)


class Searcher(object):
    """Searcher class"""
    
    def search_in_text(self, text):
        """
        Поиск ключевых слов по одному тексту
        
        Output:
        list
        """
        pass
    
    
    def search_in_texts(self, texts):
        """
        Поиск ключевых слов по коллекции текстов 
                
        Output:
        list[list]
        """
        pass
    
    
    def save_skills_collection(self, area_id, key_skills, overwrite = True, collection_path='share/projects/Slava/hh_ru/old_job-description-keyword-extractor/data/key_skills_collection/keu_skills_collection.csv'):
        """
        Метод сохранения ключевых слов из списка key_skills в общую таблицу для реиспользования                
        
        Output:
        None
        """
        
        
        pass
    
    
    def load_skills_collection(self, area_id, collection_path='share/projects/Slava/hh_ru/old_job-description-keyword-extractor/data/key_skills_collection/keu_skills_collection.csv'):
        """
        Метод инициации поискового алгоритма для определенной области area_id  
        
        Output:
        None
        """
        
        pass
    
    
    def search_by_areas(self, texts, area_ids):
        """
        Метод для поиска вакансий с различными колекциями ключевых слов. Для того случая, когда на вход подаются вакансии из разных областей, а для разных областей присутствуют разные ключевые слова
        
        Output:
        list[list]
        """
        pass