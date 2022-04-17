import requests
from tqdm import tqdm
import os
import json
import argparse


with open("./user_project_info.json", 'r', encoding="UTF-8") as j:
     my_info = json.loads(j.read())
tagtogAPIUrl = "https://www.tagtog.net/-api/documents/v1"
auth = requests.auth.HTTPBasicAuth(
        username=my_info["username"], 
        password=my_info["password"]
        )

def upload_texts(folder_dir, texts_per_folder):
    """
    이 함수는 입력 받은 폴더의 모든 텍스트 파일의 내용들을 한줄씩 tagtog에 업로드해줍니다
    tagtog에 폴더가 나눠져있다면 원하는 폴더 당 몇개씩 할당할 지 texts_per_folder에 정해줍니다
    todo: argparser를 사용하거나 웹에서 가져오거나 해서 폴더 유연하게 할당할 수 있게 하기
    """
    index = 1
    tagtog_folder_list = ["sungjin","nayeon","changuk","jaehak","taeil"]
    for text_file in os.listdir(folder_dir):
        with open(os.path.join(folder_dir, text_file), "r", encoding="utf-8") as f:
            for text in tqdm(f.readlines()):
                folder_ind = index//texts_per_folder
                if folder_ind >= len(tagtog_folder_list):
                    folder_ind = len(tagtog_folder_list) - 1
                params = {
                    "folder": "pool/" + tagtog_folder_list[folder_ind], 
                    "filename":index, 
                    "owner": my_info["owner"], 
                    "project": my_info["project"], 
                    "output": "ann.json"}
                payload = {"text": text}
                requests.post(tagtogAPIUrl, params=params, auth=auth, data=payload)
                index += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_dir", type=str, default="../sample_txts", help="tagtog에 업로드하고 싶은 폴더")
    parser.add_argument("--texts_per_folder", type=int, default=420, help="폴더 당 할당할 라인의 개수 default:420")
    args = parser.parse_args()
    upload_texts(args.folder_dir, args.texts_per_folder)