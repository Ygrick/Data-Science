import vk_requests
import time
from vk_token import my_token
import app_logger


logger = app_logger.get_logger(__name__)
api = vk_requests.create_api(service_token=my_token)


# спарсим фразы преподавателей из различных ЦИТАТНИКОВ-сообществ
def parse_phrase_of_teachers():
    groups = api.groups.search(q='цитаты преподавателей',
                               type='page',
                               count=20)

    # взятие основных полей (id, тип закрытости, имя)
    list_groups = list((map(lambda item: {'id': item['id'],
                                          'is_closed': item['is_closed'],
                                          'name': item['screen_name'],
                                          }, groups['items'])))

    # отсеиваем устаревшие группы
    list_groups = [group for group in list_groups[2:] if group['id'] not in [192769854, 176415720, 83394558]]

    # берём посты групп за 2022 год
    time_2022 = 1640984400
    for group in list_groups:
        # постоянный сдвиг
        offset = 0
        # это время поста, оно должно быть больше чем 01.01.2022
        time_post = 2000000000
        print(group['name'])
        group['posts'] = []
        while(time_post > time_2022):
            posts = api.wall.get(domain=group['name'],
                                 offset=offset,
                                 count=100)['items']

            posts_list = [post['text'] for post in posts]
            # в словаре добавляем посты к конкретной группе (к которой они принадлежат)
            group['posts'].append(posts_list)
            # сдвигаем
            offset += 100
            # смотрим какая дата у посленего взятого нами поста
            time_post = posts[-1]['date']
            # спим
            time.sleep(0.33)

    # создадим общий список всех фраз из всех постов всех цитатников
    # по ним будем проводить статистику
    list_of_phrase = []
    for group in list_groups[:]:
        for post in group['posts'][0]:
            # после \n\n идёт фио препода, поэтому отбросим эту часть + уберём все переносы строк
            index_sub_str = post.find('\n\n')  # индекс с которого начинается \n\n
            result_str_to_append = post[:index_sub_str].replace('\n', ' ')

            list_of_phrase.append(result_str_to_append)
    return list_of_phrase