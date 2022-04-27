import vk_requests
from vk_token import my_token
import nltk
import pymorphy2
from nltk.corpus import stopwords
import re
import numpy as np
import app_logger


logger = app_logger.get_logger(__name__)

nltk.download('stopwords')

# для парсинга
api = vk_requests.create_api(service_token=my_token)

# какая-то штука для приведения слов к инфинитивам (слушал -> слушать, пела -> петь ... и т.д.)
morph = pymorphy2.MorphAnalyzer()

# слова которые удалим из наших фраз
# тут общие слова + слова которые не понравились мне + паразиты + местоимения + много чего
stopwords_ru = stopwords.words("russian") + ['это', 'нею', 'самый', 'ещё', "нужно",
                                             "очень", "свой", "ваш", "наш", "весь",
                                             "всё", "который", "потому", "что", "поэтому",
                                             "почему", "просто", "вообще", 'жизнь',
                                             'хороший', 'большой', 'сегодня', 'хотеть',
                                             'сказать', 'видеть', 'время', ]
# господи знать бы что это
patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"


# нормализация текста
def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if token not in stopwords_ru:
                tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


# взятие 100 постов групп
def take_posts(id_of_group):
    posts = api.wall.get(owner_id=id_of_group,
                         offset=0,
                         count=100)['items']
    posts_list = [post['text'] for post in posts]
    clear_posts_list = []
    for post in posts_list:
        try:
            clear_posts_list.append(lemmatize(post))
        except:
            pass
    return clear_posts_list


# предсказание
def predict(text, filter_list):
    """
    Предсказание цитаты - преподавательская или нет
    :param text: исходный текст, который надо предсказать
    :param filter_list: список с ключевыми словами
    :return: кортеж из (Предсказание, Какие_ключевые_слова_найдены_в_тексте)
    """
    list_common_words = []
    for word_from_filter in filter_list:
        try:
            if word_from_filter in text:
                list_common_words.append(word_from_filter)
        except:
            pass
    return len(list_common_words) > 0, list_common_words


def calculate_score(list_of_phrase, filter_list):
    """
    Метрика
    :param list_of_phrase: список фраз, на основе которых будет score
    :param filter_list: список с ключевыми словами
    :return: score

    """
    list_of_predict = [int(predict(item, filter_list)[0]) for item in list_of_phrase]
    count_teachers_phrase = np.array(list_of_predict).sum()
    return count_teachers_phrase / len(list_of_predict)
