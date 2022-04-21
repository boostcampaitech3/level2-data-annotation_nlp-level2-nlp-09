import json
import pandas as pd
import numpy as np
from fleiss import fleissKappa

# 정의한 relation 정보 읽어오기
with open("./relations.json", 'r', encoding="UTF-8") as j:
     relations = json.loads(j.read())

# file_dir = '../tagging_data/pilot_tagging.xlsx'  # 1차 파일럿 태깅
file_dir = '../tagging_data/pilot_tagging2.xlsx'  # 2차 파일럿 태깅
result = pd.read_excel(file_dir, sheet_name='Main', engine='openpyxl')  

labels1 = list(result['찬국'])
labels2 = list(result['재학'])
labels3 = list(result['나연'])
labels4 = list(result['태일'])
labels5 = list(result['성진'])

result = pd.DataFrame()
result['member1'] = [relations[label] for label in labels1]
result['member2'] = [relations[label] for label in labels2]
result['member3'] = [relations[label] for label in labels3]
result['member4'] = [relations[label] for label in labels4]
result['member5'] = [relations[label] for label in labels5]


result = result.to_numpy()
num_classes = int(np.max(result)) + 1  # 라벨이 0부터 시작하기 때문

# 평가자들이 relation별로 예측한 개수 
transformed_result = []
for i in range(len(result)):
    temp = np.zeros(num_classes)
    for j in range(len(result[i])):
        temp[int(result[i][j]-1)] += 1
    transformed_result.append(temp.astype(int).tolist())

# fleiss Kappa 계산
kappa = fleissKappa(transformed_result,len(result[0]))