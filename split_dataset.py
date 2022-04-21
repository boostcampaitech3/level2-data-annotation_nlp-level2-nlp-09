# train_test split
import os
import pandas as pd
from load_data import *


FILE_NAME = "ruw_data/merged_dataset.csv"
SAVE_DIR = "./ruw_data/"

pd_dataset = pd.read_csv(FILE_NAME)
pd_train, pd_test = stratified_choice_train_test_split(pd_dataset, test_size=0.1, random_state=42)

if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)

pd_train.to_csv(os.path.join(SAVE_DIR, "train.csv"), index=False)
pd_test.to_csv(os.path.join(SAVE_DIR, "test.csv"), index=False)

print("========== train test split 완료 ==========")