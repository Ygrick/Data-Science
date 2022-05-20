from NLP_analysis import lemmatize, take_posts, predict, calculate_score
from nltk.probability import FreqDist
from parsing import parse_phrase_of_teachers
import app_logger


logger = app_logger.get_logger(__name__)

# Список фраз для анализа
train = parse_phrase_of_teachers()

# нормализация фраз
normalize_list_of_phrase = []
for item in train:
    lemma = lemmatize(item)
    if lemma:
        normalize_list_of_phrase += lemma

# список самых популярных слов
fdist = FreqDist(normalize_list_of_phrase)
most_popular_words = fdist.most_common(60)

# из списка самых популярных слов уберём те,
# длина которые меньше двух букв
# + сделаем такой список фильтром (т.е. список основных фраз преподавателя)
filter_list = []
for word in most_popular_words:
    if len(word[0]) > 2:
        filter_list.append(word[0])


# https://vk.com/-102022158 - признания оренбург
# https://vk.com/-80799731 - цитатник мирэа
# создадим тестовую выборку, чтоб проверить предсказательную способность
no_teachers, teachers = take_posts(-102022158), take_posts(-80799731)

print('----------------------')
# logger.info(predict(no_teachers[0], filter_list))
print(f'score не цитатника: {calculate_score(no_teachers, filter_list)}')
# logger.info(predict(teachers[0], filter_list))
print(f'score цитатника: {calculate_score(teachers, filter_list)}')
print('----------------------')
print('Score - это отношение: (фразы предсказанные как преподавателськие)/(все фразы)')
print('Если score > 50, то паблик считается цитатником преподавателей, иначе - нет')
