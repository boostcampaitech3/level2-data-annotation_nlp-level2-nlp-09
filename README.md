# RE 데이터 제작(**러시아-우크라이나 전쟁**) - NLP 9조(MnM)
> 네이버 부스트캠프 AI Tech 3기 P-Stage(Level 2) NLP 데이터제작을 위해 작성된 문서입니다. 해당 Competition에서는 실제 [위키피디아 원시 말뭉치](https://ko.wikipedia.org/wiki/%EB%9F%AC%EC%8B%9C%EC%95%84-%EC%9A%B0%ED%81%AC%EB%9D%BC%EC%9D%B4%EB%82%98_%EC%A0%84%EC%9F%81)를 활용하여 직접 **RE Task**에 쓰이는 주석 코퍼스를 만들며, 한국어 및 다른 언어에서의 자연어처리 데이터셋의 유형 및 포맷이 어떠한지, 그리고 데이터셋을 구축하는 일반적인 프로세스가 무엇인지 학습합니다. 

# Table of Contents
1. [MnM Team Introduction](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09#1-mnm-team-introduction)
2. [Project Dataset](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09#2-project-dataset)
3. [Tagging using tagtog](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09#3-tagging-using-tagtog)
4. [Data Validation](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09#4-data-validation)
5. [License](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09#5-license)
---
## 1. MnM Team Introduction

### Wrap-up Report 

<a href="https://colorful-bug-b35.notion.site/NLP-9-MnM-Wrap-up-report-6766623487014f66a5f80da2a710d98c"><img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png" width="50"/></a>
**<<<Click Logo**

### 마스터 클래스 **섬세킹** 발표자료
<a href="https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09/blob/main/%EB%A7%88%EC%8A%A4%ED%84%B0%ED%81%B4%EB%9E%98%EC%8A%A4_%EC%84%AC%EC%84%B8%ED%82%B9_%EB%B0%9C%ED%91%9C.pdf"><img src="https://user-images.githubusercontent.com/33839093/164989270-3f01755b-a906-40c2-987e-b2ab2f776984.png" width="300"></a>
**<<<Click Logo**


### Members
김태일|문찬국|이재학|하성진|한나연|
:-:|:-:|:-:|:-:|:-:
<img src='https://user-images.githubusercontent.com/46811558/162856318-13a478a3-ad96-4e1f-ad24-3e0a92b81eb7.jpg' height=100 width=100px></img>|<img src='https://user-images.githubusercontent.com/46811558/162856364-d71ea54c-31df-433f-8968-93ade6da30b5.jpg' height=100 width=100px></img>|<img src='https://user-images.githubusercontent.com/46811558/157460675-9ee90b62-7a39-4542-893d-00eafdb0fd95.jpg' height=100 width=100px></img>|<img src='https://user-images.githubusercontent.com/46811558/162856411-70847d72-1dbc-4389-b6e5-bcacba95b2ab.jpg' height=100 width=100px></img>|<img src='https://user-images.githubusercontent.com/46811558/162856463-e10110b7-7e68-4469-9418-6165108a3885.jpg' height=100 width=100px></img>
[detailTales](https://github.com/detailTales)|[nonegom](https://github.com/nonegom)|[wogkr810](https://github.com/wogkr810)|[maxha97](https://github.com/maxha97)|[HanNayeoniee](https://github.com/HanNayeoniee)
gimty97@gmail.com|fksl9959@naver.com |jaehahk810@naver.com|maxha97@naver.com |nayeon2.han@gmail.com

### Members' Role
| Member | Role | 
| --- | --- |
| 김태일 | Tagtog 플랫폼에 문장 올리기 |
| 문찬국 | Relation map 작성 |
| 이재학 | 가이드라인 작성 |
| 하성진 | 가이드라인 작성 |
| 한나연 | IAA 계산, 모델 튜닝 |

---

## 2. Project Dataset
> 이번 프로젝트에서는 직접 관계 추출 태스크 데이터셋을 만들고, 만든 데이터셋을 모델에 적용하여 검증하는 것이 목표이다.

### 데이터 설명
2022 러시아의 침공으로 발발한 **러시아-우크라이나 전쟁**을 중심으로 러시아와 우크라이나의 역사와 외교적인 관계를 포함하는 데이터이다. 코퍼스의 개수는 총 35개의 텍스트(40개 중 5개는 데이터 누락) 약 2100문장이다. 데이터는 부스트캠프 측으로부터 **러시아-우크라이나 전쟁** 주제에서 도출된 키워드들을 **위키피디아(CC BY-SA 3.0)** 문서 제목을 기반으로 수집해 제공받았다. 

### 데이터 선정 이유
프로젝트의 결과물인 관계추출 데이터를 통해 인사이트를 얻을 수 있는 주제를 선정하고자 했다. 또한 러시아-우크라이나 전쟁 데이터로 정치적 관계, 국제 정세 등의 정보를 담는 지식 그래프로 확장될 수 있을 것이라고 생각하였다. 또한, 현 학습데이터 기반 관계추출 모델은 시시각각 업데이트되는 관련 주제에 대한 정보에서 관계추출을 통해 지식그래프를 확장하고 지속적으로 인사이트를 도출할 수 있을 것이라 생각했다.

### Relation Map
<a href="https://docs.google.com/spreadsheets/d/1eMPZTpkVTwXyW-D1txj1NZyHt6ZOiw1R/edit#gid=535075484"><img src="https://user-images.githubusercontent.com/46811558/164429000-15b142e6-8b12-47fc-80be-41123c61a9fc.jpg" width="50"/></a>
**<<<Click Logo**

### Guideline
<a href="https://docs.google.com/document/d/1XhR36u-DZoZcP9yVYDDPwrb_AUrtPIc0/edit"><img src="https://user-images.githubusercontent.com/46811558/164429203-a3dfb8f8-0d8d-4889-8ddf-a8abaee08a69.png" width="50"/></a>
**<<<Click Logo**

---
## 3. Tagging Using [tagtog](https://tagtog.net/)
- data upload: sample_txts의 텍스트 파일들의 텍스트를 한줄씩 tagtog에 업로드
```
cd tagtog_data_handler
python data_upload.py
```
- data to csv: tagtog에서 다운로드한 annotation data를 각 폴더별로 csv로 변환
```
cd tagtog_data_handler
python data_to_csv.py
```
- merge csvs: 폴더 별 csv 파일들을 하나로 합쳐서 파일럿 태깅 데이터 셋과 전체 데이터 셋 반환
```
cd tagtog_data_handler
python merge_csvs.py
```
---

## 4. Data Validation

### Fleiss' Kappa
[pilot tagging](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09/tree/main/pilot_tagging)에서 ```calculate_iaa.py```파일을 사용해 Fleiss' Kappa를 계산한다.


| file | # raters | # categories | # subjects | PA | PE | Fleiss' Kappa |
| --- | --- | --- | --- | --- | --- | --- |
|pilot_tagging1.xlsx | 5 | 10 | 100 | 0.7570 | 0.1546 | 0.713 | 
|pilot_tagging2.xlsx | 5 | 10 | 100 | 0.8059 | 0.2243 | 0.75 |


### Model Tuning
1) ‘러시아-우크라이나 전쟁' 데이터셋에 맞게 새로 정의한 10개의 관계에 따라 ```make_pkl.py```파일을 사용해 pkl파일을 생성한다. 
2) ```split_dataset.py```을 사용해 전체 1770개의 데이터를 9:1 비율로 클래스별 분포가 유지하며 train data와 test data로 나눈다. 
이후 모델 학습에서 train data를 다시 9:1 비율로 나누어 각각 train, validation에 사용했다. 

<img src="https://user-images.githubusercontent.com/33839093/164518462-268d2c07-51bd-41f1-83ae-f87438e9e190.png" width="700">

3) roberta-large 모델, Focal loss를 사용해 학습을 진행했다. 자세한 파라미터는 [config](https://github.com/boostcampaitech3/level2-data-annotation_nlp-level2-nlp-09/blob/main/config.json)에, 실험 결과는 [wandb](https://wandb.ai/hannayeoniee/Russia-Ukraine-War/runs/2xmrl3fh?workspace=user-hannayeoniee)에 나타나 있다. 

| dataset | micro-f1 score | auprc |
| --- | --- | --- |
| valid | 87.097 | 89.213 | 
| test | 88.152 | - |

---

## 5. License

```러시아-우크라이나 전쟁``` 데이터셋은 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.ko) 라이선스 하에 공개되어 있습니다.

<a href="https://creativecommons.org/licenses/by-sa/3.0/deed.ko"><img src="https://user-images.githubusercontent.com/33839093/164514617-269f0761-bebd-49f2-8eec-8691b98e5069.png" width="150"/></a>
