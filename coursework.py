from pprint import pprint
import requests
import json
from urllib.parse import urlencode
from progress.bar import Bar
app_id = 51826559
class VKAPICLIENT:
    api_base_url = 'https://api.vk.com/method'
    def __init__(self, token, user_id):
        with Bar('init class atribut', max=100) as bar:
            for i in range(100):
                bar.next()
        self.token = token
        self.user_id = user_id
    def get_common_params(self):
        return{
            'access_token': self.token,
            'v': '5.131',
        }
    def get_photos(self):
        with Bar('get photos url', max=100) as bar:
            for i in range(100):
                bar.next()
        params = self.get_common_params()
        params.update({'owner_id': self.user_id,
                       'album_id': 'wall',
                       'photo_sizes': 1,
                       'extended': 1
                       })
        response = requests.get(f'{self.api_base_url}/photos.getAll', params=params)
        return response.json()
    max_size_List = []
    def get_maxsize_photo(self):
        with Bar('get_maxsize_photo_url', max=100) as bar:
            for i in range(100):
                bar.next() 
        js = self.get_photos()
        items = js["response"]["items"]
        all_url_list = []
        for i in items:
            size_list = []
            size_dict = {}
            for k in (i['sizes']):
                a = k["height"]
                b = k["width"] 
                url = k['url']
                size_list.append([a, b])
                size_dict[f'{[a,b]}'] = url
            maxing = max(size_list)
            all_url_list.append(size_dict[f'{maxing}'])
            self.max_size_List.append(maxing)
        return(all_url_list)
    def get_photo_name(self):
        with Bar('getphotoname', max=100) as bar:
            for i in range(100):
                bar.next()
        js = self.get_photos()
        likes_list = []
        for i in js["response"]['items']:
            c = i['likes']['count']
            likes_list.append(c)
        return likes_list

class YANDEXAPI(VKAPICLIENT):
    base_url = "https://cloud-api.yandex.net"
    def __init__(self, ya_token):
        with Bar('init class atribute', max=100) as bar:
            for i in range(100):
                bar.next()        
        self.token = ya_token
    def create_folder(self):
        with Bar('create folder', max=100) as bar:
            for i in range(100):
                bar.next()        
        url_create_folder = self.base_url + "/v1/disk/resources"
        params_dict = {
            'path': 'vk-photo'
        }
        headers_dict = {
            'Authorization':f'OAuth {self.token}'
        }
        response = requests.put(url_create_folder,
                                params=params_dict, 
                                headers=headers_dict)
        result = 'Папка успешно создана'
        return print(result)

    def download_photo(self, url_maxsize_list, photo_name, photo_quantity):
        with Bar('download photo', max=photo_quantity) as bar:
            for i in range(photo_quantity):
                bar.next()
        self.create_folder()
        url_post = self.base_url + '/v1/disk/resources/upload'
        if len(url_maxsize_list) > photo_quantity:
            url_maxsize_list = url_maxsize_list[:photo_quantity]
        json_info = []
        for i, j in zip(url_maxsize_list, photo_name):
            params = {
            'url':f'{i}',
            'path':f'vk-photo/{j}.jpg' 
            }
            headers = {
            'Authorization':f'OAuth {self.token}'
            }
            requests.post(url_post, params=params,headers=headers)
        result = 'файлы успешно скачаны на яндекс диск'
        return print(result)
    def get_json_info(self,max_size_val,photo_name):
        with Bar('get json file', max=20) as bar:
            for i in range(20):
                bar.next()        
        json_info = []
        for i, j in zip(photo_name, max_size_val):
            js = {}
            js['file_name'] = f'{i}.jpg'
            js['size'] = f'{j}'
            json_info.append(js)
        with open('file.json', 'w') as file:
            json.dump(json_info, file, ensure_ascii=False, indent=4)
        result = 'Файл file.json сохранен в вашу директорию'
        return print(result)

if __name__ == '__main__':
    token_vk = input('Введите токен ВК: ')
    user_id = input('Введите юзер id ВК: ')
    token_yandex = input('Введите токен Яндекс: ')
    photo_quan = input('Введите кол-во скачиваемых изображений (по умолчанию - 5 фото): ')
    if photo_quan == '':
        photo_quan = 5
    else:
        photo_quan = int(photo_quan)

    vk_klient = VKAPICLIENT(token_vk, user_id)
    url_list = vk_klient.get_maxsize_photo()
    max_size_value = []
    b = vk_klient.max_size_List
    for i in b:
        max_size_value.append(f'{i[0]}x{i[1]}')
    max_size_value = max_size_value[:photo_quan]
    ya_klient = YANDEXAPI(token_yandex)
    photo_name = list(vk_klient.get_photo_name())[:photo_quan]
    ya_klient.download_photo(url_list, photo_name, photo_quan)
    ya_klient.get_json_info(max_size_value, photo_name)