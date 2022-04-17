from unicodedata import name
import requests
from tqdm import tqdm
import json
import re
import argparse
import pandas as pd


with open("./user_project_info.json", 'r', encoding="UTF-8") as j:
     my_info = json.loads(j.read())
tagtogAPIUrl = "https://www.tagtog.net/-api/documents/v1"
auth = requests.auth.HTTPBasicAuth(
        username=my_info["username"], 
        password=my_info["password"]
        )
map_url = "https://www.tagtog.net/-api/settings/v1/annotationsLegend?owner=taeil&project=boost_camp_NLP_9_data_annotation"
entity_map = eval(requests.get(map_url, auth=auth).text)


def get_text_ids():
    """
    text 파일들의 파일 id들을 가져옴
    """
    params = {"owner": my_info["owner"], "project": my_info["project"], "search": "*.txt", "output":"csv"}
    response = requests.get(tagtogAPIUrl, params=params, auth=auth)
    matched_ids = re.findall(r"[\S]+.txt", response.text)
    return matched_ids
    
def download_and_preprocess_texts():
    """
    tagtog documents 에 txt 파일들을 id로 가져옴
    가져온 data에 entity가 2개보다 작을 시(정상 데이터는 2개) 경고 알림 후 패스
    """
    sentences = []
    subject_entities = []
    object_entities = []
    labels = []
    matched_ids = get_text_ids()
    for id in tqdm(matched_ids[-10:]): # 테스트 용이라 10개만 찍음
        id_params = {"owner": my_info["owner"], "project": my_info["project"], 'ids':id, "output": "ann.json"}
        text_params = {"owner": my_info["owner"], "project": my_info["project"], 'ids':id, "output": "text"}
        entity_info = requests.get(tagtogAPIUrl, params=id_params, auth=auth)
        text_info = requests.get(tagtogAPIUrl, params=text_params, auth=auth).text.replace("\n","")
        entity_types = [entity_map[entype] for entype in re.findall(r'e_[0-9]+',entity_info.text)]
        entity_words = re.findall(r'"start":[0-9]+,"text":"[^\}]+',entity_info.text)
        if len(entity_types) < 2:
            # 미스 태깅 되었을 때 넘김
            print(f"{id} may have been miss-tagged please check it")
            continue
        for i in range(2):
            type_info = re.split("_", entity_types[i])
            word_info = re.split("[:,]", entity_words[i])
            if type_info[0] == "sub":
                sub_word = word_info[-1]
                sub_start_idx = int(word_info[1])
                sub_end_idx = sub_start_idx + len(sub_word) - 3
                sub_type = type_info[1]
            else:
                obj_word = word_info[-1]
                obj_start_idx = int(word_info[1])
                obj_end_idx = obj_start_idx + len(obj_word) - 3
                obj_type = type_info[1]
        relation = re.search(r'r_[0-9]+', entity_info.text)
        subject_entity = f"{{'word':{sub_word},'start_idx':{sub_start_idx},'end_idx':{sub_end_idx},'type':'{sub_type}'}}"
        subject_entities.append(subject_entity)
        object_entity = f"{{'word':{obj_word},'start_idx':{obj_start_idx},'end_idx':{obj_end_idx},'type':'{obj_type}'}}"
        object_entities.append(object_entity)
        if relation:
            relation = relation.group(0)
        labels.append(relation)
        sentences.append(text_info)
        print(f"sentence:{text_info}\nsubject_entity: {subject_entity}\nobject_entity {object_entity} \nlabel {relation}\n")
    return {
        "sentence":sentences,
        "subject_entity":subject_entities,
        "object_entity":object_entities,
        "label":labels
    }

def save_dataframe(csv_path):
    dict_for_df = download_and_preprocess_texts()
    df = pd.DataFrame(dict_for_df)
    df.to_csv(csv_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=str, default="./sample.csv", help="저장하려는 경로 + csv 파일이름 default: ./sample.csv")
    args = parser.parse_args()
    save_dataframe(args.csv_path)