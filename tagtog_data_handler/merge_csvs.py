import os
import pandas as pd  

def save_merge_csvs():
    """
    검증 편의상 폴더(사람) 별로 나누어 놨던 csv 파일들을 하나로 합침
    """
    sentence = []
    subject_entity = []
    object_entity = []
    label = []
    csvs_dir = "../annotation_csvs_split_by_person"
    for csv in os.listdir(csvs_dir):
        df = pd.read_csv(os.path.join(csvs_dir, csv)).sample(frac=1, random_state=42)
        sentence.extend(df["sentence"])
        subject_entity.extend(df["subject_entity"])
        object_entity.extend(df["object_entity"])
        label.extend(df["label"])
    merged_df = pd.DataFrame({
        "sentence": sentence,
        "subject_entity": subject_entity,
        "object_entity": object_entity,
        "label":label
    })
    merged_df.to_csv(f"../merged_csvs/merged_dataset.csv", encoding="utf-8-sig")

def save_pilot_csv():
    """
    파일럿 태깅을 위해 각 사람이 태깅한 데이터에서 40개씩 데이터를 가져온 후 합침
    가시성을 위해 엔티티에 <sub 엔티티>로 표시
    """
    sentence = []
    subject_entity = []
    object_entity = []
    csvs_dir = "../annotation_csvs_split_by_person"
    for csv in os.listdir(csvs_dir):
        df = pd.read_csv(os.path.join(csvs_dir, csv)).sample(n= 40, random_state=0)
        sentence.extend(df["sentence"])
        subject_entity.extend(df["subject_entity"])
        object_entity.extend(df["object_entity"])
    merged_df = pd.DataFrame({
        "sentence": sentence,
        "subject_entity": subject_entity,
        "object_entity": object_entity
    })
    merged_df = visualize_entity(merged_df)
    merged_df.to_csv(f"../merged_csvs/pilot.csv", encoding="utf-8-sig")


def visualize_entity(merged_df):
    for i in range(len(merged_df)):
        sub_word_dict = eval(merged_df.at[i,"subject_entity"])
        sub_word_start = sub_word_dict["start_idx"]
        sub_word_end = sub_word_dict["end_idx"]
        ob_word_dict = eval(merged_df.at[i,"object_entity"])
        ob_word_start = ob_word_dict["start_idx"]
        ob_word_end = ob_word_dict["end_idx"]
        sent = merged_df.at[i,"sentence"]
        added_len = len("<sub >")
        if sub_word_start < ob_word_start:
            sent = sent[:sub_word_start] + "<sub "+ sent[sub_word_start:sub_word_end + 1] + ">" + sent[sub_word_end+1:]
            ob_word_start += added_len
            ob_word_end += added_len
            sent = sent[:ob_word_start] + "<obj "+ sent[ob_word_start:ob_word_end + 1] + ">" + sent[ob_word_end+1:]
        else:
            sent = sent[:ob_word_start] + "<obj "+ sent[ob_word_start:ob_word_end + 1] + ">" + sent[ob_word_end+1:]
            sub_word_start += added_len
            sub_word_end += added_len
            sent = sent[:sub_word_start] + "<sub "+ sent[sub_word_start:sub_word_end + 1] + ">" + sent[sub_word_end+1:]
        merged_df.at[i,"sentence"] = sent
        merged_df.at[i,"subject_entity"] = sub_word_dict["type"]
        merged_df.at[i,"object_entity"] = ob_word_dict["type"]
    return merged_df

if __name__ == "__main__":
    save_merge_csvs()
    save_pilot_csv()
