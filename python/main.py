import pandas as pd
import matplotlib.pyplot as plt

parking = pd.read_csv('./parking.csv', encoding='cp949')

# 슬라이스를 복사본으로 만들어 경고 제거
df = parking[['주차장명', '주차장구분', '소재지도로명주소', '소재지지번주소', '주차구획수']].copy()

# 주소 컬럼 생성: 두 컬럼 모두 값이 있으면 소재지도로명주소를 우선 사용
df['주소'] = df['소재지도로명주소'].combine_first(df['소재지지번주소'])

print(df.head())
