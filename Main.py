import requests
from PIL import Image
from io import BytesIO
import urllib.request

def downloading_progress(blocks_read,block_size,total_size):
    if not blocks_read:
        print ("Connected!")
    if total_size <0:
        print ("Read %d blocks"  % blocks_read)
    else:
        print("Downloading... %d KB of %d KB" % (blocks_read*block_size/1024.0,total_size/1024.0))

def action_select():
    selected_action = int(input("\n'1' : description \n'2' : View Image\n'3' : Download Watchface\nany : EXIT\n"))
    if selected_action == 1:
        print(item_des_list[selected_item_sub])
        action_select()
    elif selected_action == 2:
        selected_item_image_name = item_image_list[selected_item_sub].split("|")[0]
        selected_item_image_response = requests.get(img_add + selected_item_image_name)
        selected_item_image = Image.open(BytesIO(selected_item_image_response.content))
        selected_item_image.show()
        action_select()
    elif selected_action == 3:
        print("Downloading...")
        selected_item_filename = item_filename_list[selected_item_sub]
        urllib.request.urlretrieve(download_add + selected_item_filename, selected_item_title + '.watch', downloading_progress)
        print("finished!")
    else:
        print("???")
        exit()

search_add = 'http://www.watchawear.com/index.php?option=com_jsonexport&table=watchawear_app_main_search&fields=file_id,file_title,images,url_download,size,description,downloads&total=60&search='
download_add = 'http://www.watchawear.com/jdownloads/--_watchmaker_--/watchmaker_watch_faces_free/'
img_add = 'http://watchawear.com/images/jdownloads/screenshots/thumbnails/'

search_text=str(input("Search Something: "))
search_json = requests.get(search_add + search_text).json()


item_title_list = list()
item_image_list = list()
item_filename_list = list()
item_des_list = list()
item_amount = 0
for n in search_json:
    if n.get('type') == 'round':
        current_title = n.get('file_title')
        current_image = n.get('images')
        current_filename = n.get('url_download')
        current_des = n.get('description')
        item_amount += 1

        print(str(item_amount) + " : "+ current_title)

        item_title_list.append(current_title)
        item_image_list.append(current_image)
        item_filename_list.append(current_filename)
        item_des_list.append(current_des)

selected_item_sub = int(input("Select a Watchface: ")) - 1
selected_item_title = item_title_list[selected_item_sub]

print("Selected : "+ selected_item_title)
action_select()