import requests
import json
import os
import shutil
def make_folder(name:str):
    try:
        os.makedirs(name,exist_ok = True)
        print("directory", name ,"created")
    except OSError as error:
        print("directory", name , "can't be created")

def download_image(image_url:str,filename:str):
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        print("hello")
        with open(filename,'wb') as f:
            f.write(image_response.content)

def get_details(url:str):
    url = url+"?__a=1"
    response = requests.get(url)
    print(response.status_code)
    response = json.loads(response.text)
    if "user" in response['graphql']:
        print(response['graphql']['user']['full_name'])
        user_id = response['graphql']['user']['id']
        
# making folder to save images 
        folder_name = response['graphql']['user']['full_name']
        make_folder(folder_name)
        # profile image
        print(response['graphql']['user']['profile_pic_url_hd'])
        profile_image_url  = response['graphql']['user']['profile_pic_url_hd']
# download that image
        download_image(profile_image_url,f"{folder_name}\profile_image.jpg")
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
            print(len(response['data']['user']['edge_owner_to_timeline_media']['edges']))
            images_list = response['data']['user']['edge_owner_to_timeline_media']['edges']
            for i in images_list:
                download_image(i['node']['display_url'],f"{folder_name}\{i['node']['id']}.jpg")


# video_download("https://www.instagram.com/p/B72Y46Wl1Qe/")
# download("https://www.instagram.com/rachel_mypark/")
# download("https://www.instagram.com/vvveenaa/")
# url = "https://www.instagram.com/millionsbilliondreams/?__a=1"
url = "https://www.instagram.com/love.connection_/?__a=1"



if __name__ == "__main__":
    insta_id = input('Enter required Instagram ID :')
    if insta_id[0] == '@':
        insta_id = insta_id[1:]
    print(insta_id)
    url = f'https://www.instagram.com/{insta_id}/'
    download(url)
