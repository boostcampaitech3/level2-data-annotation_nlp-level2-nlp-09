import pickle

# dict 생성하기
label_to_num = {'no_relation':0,
                'per:title':1,
                'org:member_of':2,
                'org:alternate_names':3, 
                'org:top_members/employees':4, 
                'org:hostile':5, 
                'org:friendly':6, 
                'org:property':7, 
                'eve:place':8, 
                'eve:date':9
} 

num_to_label = {0:'no_relation',
                1:'per:title',
                2:'org:member_of',
                3:'org:alternate_names', 
                4:'org:top_members/employees', 
                5:'org:hostile', 
                6:'org:friendly', 
                7:'org:property', 
                8:'eve:place', 
                9:'eve:date'
} 

# 데이터 저장
with open('ruw_label_to_num.pkl', 'wb') as f:
	pickle.dump(label_to_num, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('ruw_num_to_label.pkl', 'wb') as f:
	pickle.dump(num_to_label, f, protocol=pickle.HIGHEST_PROTOCOL)

print("========== pkl 데이터 생성 완료 ==========")