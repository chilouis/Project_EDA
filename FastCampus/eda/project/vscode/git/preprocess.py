# str.contains ver.
# arxiv 데이터셋에서 모델 키워드를 추출 & 분류
import re
import pandas as pd
from tqdm import tqdm

def process_model_name(model_name):
    # 정규 표현식 패턴
    pattern = r'\s\([^)]+\)'
    if '(' in model_name and ')' in model_name and model_name.find('(') < model_name.find(')'):
        # 괄호가 공백 다음에 있는 경우만 괄호와 그 안의 내용을 제거
        processed_model_name = re.sub(pattern, '', model_name)
    else:
        # 그 외의 경우에는 모델명 그대로 사용
        processed_model_name = model_name
    
    # 모델명의 뒤에 있는 '+' 또는 '++'와 같은 추가 문자열 제거
    processed_model_name = re.sub(r'\s*[+]+\s*$', '', processed_model_name)
    
    return processed_model_name

# 파일 경로 정의
docs1_path = r"C:\Users\ASUS\Desktop\coding\FastCampus\eda\project\vscode\arxiv_cs.csv"
# docs1_path = r"C:\Users\ASUS\Desktop\coding\FastCampus\eda\project\vscode\test_arxiv_cs.csv"
docs2_path = r"C:\Users\ASUS\Desktop\coding\FastCampus\eda\project\vscode\paperswithcode.csv"

# 데이터 불러오기
docs1_df = pd.read_csv(docs1_path, dtype=str)
docs2_df = pd.read_csv(docs2_path, dtype=str)

# 고유 모델 목록 추출
unique_models = set(docs2_df['model'].dropna()) # 1350개

# 모델별 메서드 딕셔너리 생성
model_methods = {}

# 모델별 메서드 할당
for model in unique_models:
    if isinstance(model, str): # 모델값이 (str로서) 존재하면
        matching_rows = docs2_df[docs2_df['model'] == model] # 해당 열 출력
        methods = list(set(matching_rows['method'].tolist())) # 수정
        model_methods[model] = methods # ex {'VGG' : ['Computer Vision']}

# 패턴을 딕셔너리로 저장
pattern_dict = {}
for model in unique_models:
    if isinstance(model, str):
        tmp_model = process_model_name(model)
        pattern = rf'\b\d*{process_model_name(tmp_model)}s?\d*\b'
        pattern_dict[model] = pattern

# 모델 카테고리 목록 정의
model_categories = ['Computer Vision', 'Natural Language Processing', 'Reinforcement Learning', 'Audio', 'Sequential', 'Graphs']

# 카테고리 열 생성
for category in model_categories:
    docs1_df[f'is_{category}'] = False

# 소문자로 변환하여 데이터 사전 처리 : str.contains(case=False) -> 하지말 것 -> 코드상 순서 불일치로 인해 의미상실
# docs1_df['abstract'] = docs1_df['abstract'].str.lower()
# docs1_df['title'] = docs1_df['title'].str.lower()

# 패턴을 사용하여 검색
for model in tqdm(unique_models):
    if isinstance(model, str):
        pattern = pattern_dict[model]
        is_matching_abstract = docs1_df['abstract'].str.contains(pattern,case=False,regex=True)        
        is_matching_title = docs1_df['title'].str.contains(pattern,case=False,regex=True)
        methods = model_methods.get(model, []) # 없다면, [] 반환
        
        for category in model_categories:
            if category in methods:
                docs1_df.loc[is_matching_abstract | is_matching_title, f'is_{category}'] = True

# 수정된 데이터프레임을 CSV 파일로 저장
docs1_df.to_csv(r'C:\Users\ASUS\Desktop\coding\FastCampus\eda\project\vscode\modified.csv', index=False)
