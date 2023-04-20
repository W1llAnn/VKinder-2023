import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json

from vk_api.utils import get_random_id
from random import randrange

from vk_api.exceptions import ApiError


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import sqlalchemy as sq



from createbd import work_bd
from core import VkTools
from config import acces_token, comunity_token




class BotInterfase:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message, attachment=None):
        self.bot.method('messages.send',
                       {'user_id': user_id,
                       'message': message,
                       'random_id': get_random_id(),
                       'attachment': attachment
                       }
                       )
    

   
    def handler(self):
        longpoll = VkLongPoll(self.bot)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                response = str(event.from_user and event.to_me and event.text).lower()
                user_id=event.user_id

                if len(response) < 10 and response =='привет':
                    self.message_send(user_id=event.user_id, message='Приветствую! Напишите "Поиск" чтобы начать')
                
                
                elif len(response) < 10 and response == 'поиск':
                    self.message_send(user_id=event.user_id, message='Для поиска напишите мужчина/женщина возраст от возраст до город. Например "мужчина 20 25 Москва" ')

                

                elif len(response) > 10:
                    

                    #Пол
                    sex = 0
                    if response[0:7].lower() == 'мужчина':
                        sex = 2
                    elif response[0:7].lower() == 'женщина':
                        sex = 1
                    else:
                        self.message_send(user_id=event.user_id, message='Неверно указан пол, попробуйте еще раз')
                        break
                    #sex = int(sex)

                    #print(type(sex))


                    # Возраст
                    age_from = int(response[8:10], base=10)
                    if int(age_from) < 18:
                        self.message_send(user_id=event.user_id, message='Выставлен минимальный возраст - 18 лет')
                        break
                    else:
                        age_from=int(age_from)
                    #print(type(age_from))
                    
                    age_to = int(response[11:13], base=10)
                    if int(age_to) > 98:
                        self.message_send(user_id=event.user_id, message='Выставлено максимальное значение 99 лет')
                        break
                    else:
                        age_to=int(age_to)
                    #print(type(age_to))
                    
                    # Город
                    max_len_resp = len(response)
                    city = str(response[14:max_len_resp].lower())  



                    # TEST
                    #self.message_send(user_id=event.user_id, message = f' Тест: ' + str(sex) + ' ' + str(age_from) + ' ' + str(age_to) + ' ' + str(city))



                    # Поиск анкет 
                    VkTools.result = tools.users_search(city, age_from, age_to, sex)
                    #print(VkTools.result[0]['id'])
                    work_bd.create_table()

                    

                    for i in range(2):


                        
                        response_from = work_bd.from_bd(event.user_id, dating_user)
                        dating_user = str(VkTools.result[i]['id'])
                        
                        print(response_from)
                        print(type(response_from))
                        print(dating_user)
                        print(type(dating_user))

                        if dating_user not in response_from:
                            
                        
                            self.message_send(user_id=event.user_id, message=f'\n {VkTools.result[i]}')

                            
                            sorted_user_photo = tools.photos_get(VkTools.result[i]['id'])
                            print(sorted_user_photo)


                            try:
                                self.message_send(user_id, f'фото:', 
                                                    attachment=','.join
                                                    ([sorted_user_photo[0][1], sorted_user_photo[1][1],
                                                    sorted_user_photo[2][1]]))


                            except IndexError:
                                for photo in range(len(sorted_user_photo)):
                                    self.message_send(user_id, f'фото:',
                                        attachment=sorted_user_photo[photo][0])



                            # Делаем запись в БД               worksheet_id это найденые анкеты
                            #work_bd.to_bd(event.user_id, VkTools.result[i]['id'])

                            
                        else:
                            dating_user = VkTools.result[i+1]['id']



                else:
                    self.message_send(user_id=event.user_id, message='Неверная команда. Напишите "Привет" чтобы начать.')
                    
         


if __name__ == '__main__':
    while True:
        tools = VkTools(acces_token)
        bot = BotInterfase(comunity_token)
        
        
        BotInterfase.handler(bot)
        
    




        

