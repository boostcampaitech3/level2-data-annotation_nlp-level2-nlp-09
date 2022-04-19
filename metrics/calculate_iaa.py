import json
import pandas as pd
import numpy as np
from fleiss import fleissKappa

# 정의한 relation 정보 읽어오기
with open("./relations.json", 'r', encoding="UTF-8") as j:
     relations = json.loads(j.read())

result = pd.read_excel('../tagging_data/pilot_tagging.xlsx', sheet_name='Metric', engine='openpyxl')


labels1 = list(result['member1'])
labels2 = list(result['member2'])
labels3 = list(result['member3'])
labels4 = list(result['member4'])
labels5 = list(result['member5'])

result = pd.DataFrame()
result['member1'] = [relations[label] for label in labels1]
result['member2'] = [relations[label] for label in labels2]
result['member3'] = [relations[label] for label in labels3]
result['member4'] = [relations[label] for label in labels4]
result['member5'] = [relations[label] for label in labels5]


result = result.to_numpy()
num_classes = int(np.max(result))

# fleiss Kappa 계산
transformed_result = []
for i in range(len(result)):
    temp = np.zeros(num_classes)
    for j in range(len(result[i])):
        temp[int(result[i][j]-1)] += 1
    transformed_result.append(temp.astype(int).tolist())

kappa = fleissKappa(transformed_result,len(result[0]))