from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
model_name = "models/keyT5-custom" # or 0x7194633/keyt5-base
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s

article = """В связи с развитием отдела маркетинга примем в штат специалиста по маркетингу в области аналитики Мы готовы предложить:  Официальное трудоустройство Система мотивации (оклад + премия) Дополнительная мотивация по КПЭ после успешного прохождения периода адаптации Дополнительная мотивация (подача предложений по улучшению и участие в проектной деятельности) Развитие в компании посредством внешнего и внутреннего обучения Насыщенная корпоративная жизнь (спортивные мероприятия среди коллег, проведение семейных праздников, подарки детям сотрудников и периодическое проведение конкурсов для детей)  Предстоит заниматься:   Участием в разработке маркетинговой стратегии   Участием в формировании бюджета, ведение отчетности фактического исполнения бюджетов, формирование отчетов   Участием в маркетинговых исследованиях, подготовке и проведению «тайного покупателя», замере NPS   Аналитикой продаж в разрезе рынков, направлений бизнеса, клиентов   Продакт маркетингом   Организацией и проведением стимулирующих акций – разработка механик, согласование с клиентами, проведение и контроль акций, анализ эффективности   Разработкой программ лояльности   Маркетинговым сопровождение обучения, клиентских семинаров   Участием в организации и проведении мероприятий событийного маркетинга, в том числе выставок, конференций   Составлением информационных материалов для продаж: скрипты, матрицы, презентации   Участием в разработке мероприятий для развития бренда, роста узнаваемости бренда   Мы хотим видеть в кандидате:   Высшее или средне специальное в области маркетинга, рекламы, социологии, журналистики   Дополнительные курсы повышения квалификации будет преимуществом   Знание программ обязательно - Microsoft Office (Word, Excel, PowerPoint, Outlook) Excel – формулы, функции, сводные таблицы Будет преимуществом – 1С ERP ."""

print(generate(article, top_p=1.0, max_length=64))  
# ['авиаперевозки', 'отмена авиарейсов', 'отмена рейсов', 'отмена авиарейсов', 'отмена рейсов', 'отмена авиарейсов']
