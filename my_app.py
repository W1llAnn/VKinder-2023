import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from vk_api.utils import get_random_id

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
    


    def worksheet(self,user_id, dat_user, name_dat_user, link_dat_user):
        sorted_user_photo = tools.photos_get(dat_user)
        #print(sorted_user_photo)


        sort_user_photo = []
        for photo in sorted_user_photo[:3]:
            sort_user_photo.append(photo) 
        #print(sort_user_photo)


        if sort_user_photo == []:
            self.message_send(user_id, f'\n {name_dat_user}, ссылка на профиль: {link_dat_user} фото: отсутствует')
        elif len(sort_user_photo) == 1:
            self.message_send(user_id, f'\n {name_dat_user}, ссылка на профиль: {link_dat_user} фото:', 
                                                    attachment=','.join
                                                    ([sort_user_photo[0][1]]))
        elif len(sort_user_photo) == 2:
            self.message_send(user_id, f'\n {name_dat_user}, ссылка на профиль: {link_dat_user} фото:', 
                                                    attachment=','.join
                                                    ([sort_user_photo[0][1], sort_user_photo[1][1]]))

        else:
            self.message_send(user_id, f'\n {name_dat_user}, ссылка на профиль: {link_dat_user} фото:', 
                                                    attachment=','.join
                                                    ([sort_user_photo[0][1], sort_user_photo[1][1],
                                                    sort_user_photo[2][1]]))
   


    def selection(self, user_id, response):
        response_spl = response.split()
        #print(response_spl)

        #Пол
        sex = 0
        if response_spl[0].lower() == 'мужчина':
            sex = 2
        elif response_spl[0].lower() == 'женщина':
            sex = 1
        else:
            self.message_send(user_id, message='Неверно указан пол, попробуйте еще раз')


        # Возраст
        age_from = int(response_spl[1], base=10)
        if int(age_from) < 18:
            self.message_send(user_id, message='Выставлен минимальный возраст - 18 лет')
        else:
            age_from=int(age_from)
            #print(type(age_from))
                    
        age_to = int(response_spl[2], base=10)
        if int(age_to) > 98:
            self.message_send(user_id, message='Выставлено максимальное значение 99 лет')
        else:
            age_to=int(age_to)

                    
        # Город
        city = str(response_spl[3].lower())  

        # Поиск анкет 
        VkTools.result = tools.users_search(city, age_from, age_to, sex)
        work_bd.create_table()
         
        for i in range(len(VkTools.result)):
            dating_user = int(VkTools.result[i]['id'])
            response = work_bd.from_bd(user_id)

            if dating_user not in response:
                            dat_user = str(VkTools.result[i]['id'])
                            name_dat_user = str(VkTools.result[i]['name'])
                            link_dat_user = str('https://vk.com/id'+dat_user)
                            self.worksheet(user_id, dat_user, name_dat_user, link_dat_user)
                            # Делаем запись в БД               worksheet_id это найденые анкеты
                            work_bd.to_bd(user_id, dat_user)
                            break
            else:
                            pass

                        

        
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
                    self.selection(user_id, response)
                    

                else:
                    self.message_send(user_id=event.user_id, message='Неверная команда. Напишите "Привет" чтобы начать.')






if __name__ == '__main__':
    
        tools = VkTools(acces_token)
        bot = BotInterfase(comunity_token)
        
        
        BotInterfase.handler(bot)
        
    