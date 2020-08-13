import requests
import json
import os
import shutil

current_path = os.getcwd()

def make_folder(name:str):
    try:
        print(current_path)
        os.makedirs(current_path+'\\'+ name,exist_ok = True)
        print("directory", name ,"created")
    except OSError as error:  
        print(error)  
        print("directory", name , "can't be created")

def download_image(image_url:str,filename:str):
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filename,'wb') as f:
            f.write(image_response.content)

def get_details(url:str):
    url = url+"?__a=1"
    response = requests.get(url)
    response = json.loads(response.text)
    if "user" in response['graphql']:
        user_id = response['graphql']['user']['id']
        
# making folder to save images 
        folder_name = response['graphql']['user']['full_name']
        if not folder_name:
            folder_name = user_id
        make_folder(folder_name)
        
        print(folder_name)
        # profile image
        profile_image_url  = response['graphql']['user']['profile_pic_url_hd']
# download that image
        download_image(profile_image_url,f"{current_path}\{folder_name}\profile_image.jpg")
    return user_id,folder_name

def download(url:str):
    user_id,folder_name = get_details(url)
    max_id = None
    for i in range(0,3):
        if max_id:
            parameters = {'query_id':17888483320059182,
                        'id':user_id,
                        'first':12,
                        'after':max_id}
        else:
            parameters = {'query_id':17888483320059182,
                        'id':user_id,
                        'first':12}
        url = "https://instagram.com/graphql/query/"
        
        response = requests.get(url,params=parameters)
        response = json.loads(response.text)
        max_id = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        if "user" in response['data']:
            images_list = response['data']['user']['edge_owner_to_timeline_media']['edges']
            for i in images_list:
                download_image(i['node']['display_url'],f"{current_path}\{folder_name}\{i['node']['id']}.jpg")






if __name__ == "__main__":
    insta_id = input('Enter required Instagram ID :')
    if insta_id[0] == '@':
        insta_id = insta_id[1:]
    url = f'https://www.instagram.com/{insta_id}/'
    download(url)
