import vk_api
from config import acces_token
from vk_api.exceptions import ApiError
from vk_api import VkTools



# VK Function

class VkTools():
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):
        try:
            info = self.ext_api.method('users.get',
                                      {'user_id': user_id,
                                       'fields': 'bdate,city,sex,relation'
                                      }
                                      )
        except ApiError:
            return
        return info
       


    def users_search(self, city_title, age_from, age_to, sex, offset = None):
        try:
            profiles = self.ext_api.method('users.search',
                                    {'hometown': city_title,
                                    'age_from': age_from,
                                    'age_to': age_to,
                                    'sex': sex,
                                    'count': 10,
                                    'status': 6,
                                    'offset': offset,
                                    'sort': 1
                                    }
                                    )
        except ApiError:
            return
    
        profiles = profiles['items']
        
        
        result = []
        
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                           'id': profile['id']
                           })
        return result




    def photos_get (self, user_id):
        try:
            photos = self.ext_api.method('photos.getAll',
                                     {'album_id': 'profile',
                                      'owner_id': user_id,
                                      'count': 100,
                                      'extended': 1,
                                      'photo_sizes': 1
                                     }
                                     )
        except ApiError:
            return 'нет доступа к фото'

        users_photos = []

        try:
            photos =  photos['items'] 
        except KeyError:
            return None

        for photo in photos:
            users_photos.append([photo['likes']['count'],   'photo' + str(photo['owner_id']) + '_' + str(photo['id'])])

    
        sort_result = []
        for element in users_photos:
            if element != ['нет фото.'] and users_photos != 'нет доступа к фото':
                sort_result.append(element)
        return sorted(sort_result, reverse=True)
      


        
    


if __name__ == '__main__':
    tools = VkTools(acces_token)
    

    #profiles = tools.users_search('москва', 20, 25, 2)
    #print(profiles)

    #photos = tools.photos_get(679141813)
    #print(photos)
