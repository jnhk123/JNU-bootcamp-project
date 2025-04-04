import pandas as pd

import requests

def get_address_info(address):
    url = "https://dapi.kakao.com/v2/local/search/address?query="+address
    headers = {
        "Authorization": "KakaoAK {API KEY 입력}",
        "Accept": "application/json",
        # 필요한 다른 헤더도 추가할 수 있습니다.
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        documents = response.json()['documents']
        if len(documents) > 0:
            return response.json()['documents'][0]
        else:
            return None
    else:
        return None

def pre_processing():
    parking = pd.read_csv('./parking.csv', encoding='cp949')
    # 복사
    df = parking[['주차장명', '주차장구분', '소재지도로명주소', '소재지지번주소', '주차구획수', '요금정보', '주차기본시간', '주차기본요금', '추가단위시간', '추가단위요금', '1일주차권요금적용시간', '1일주차권요금', '월정기권요금']].copy()
    # 주소 컬럼 생성: 두 컬럼 모두 값이 있으면 소재지도로명주소를 우선 사용
    df['주소'] = df['소재지도로명주소'].combine_first(df['소재지지번주소'])
    df['구'] = df['주소'].str.extract('(광산구|동구|서구|북구|남구)')
    df[['x', 'y']] = df.apply(creating_coordinates, axis=1)
    #
    df.to_csv('processedParking.csv', index=False, encoding='cp949')
    return 'processedParking.csv';

def creating_coordinates(df):
    result = get_address_info(df['주소']);
    if result is not None:
        return pd.Series([result['x'], result['y']], index=['x', 'y'])
    else:
        pd.Series([None, None], index=['x', 'y'])








