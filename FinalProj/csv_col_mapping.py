import pandas as pd

FILE_PATH = 'original_merged_heritage_data.csv'

def __main__():
    df = pd.read_csv(FILE_PATH)

    col_mapping = {
        '종류': 'category',
        '이름1': 'name_hangul',
        '이름2': 'name_hanja',
        '시도': 'city',
        '시군구': 'district',
        '관리주체': 'management_organization',
        '경도': 'longitude',
        '위도': 'latitude',
        '관리번호': 'management_number',
        '국가유산연계번호': 'association_number',
        '시도 번호': 'city_number',
        '지정해제여부': 'canceled',
        '분류1': 'type1',
        '분류2': 'type2',
        '분류3': 'type3',
        '분류4': 'type4',
        '수량': 'quantity',
        '지정일': 'designated_date',
        '주소': 'address',
        '시대': 'era',
        '소유': 'possession',
        '이미지 URL': 'image_URL',
        '내용': 'description'
    }

    print(df.columns)

    df.rename(columns=col_mapping, inplace=True)

    print(df.columns)

    df.to_csv('eng_col_heritage_data.csv')

if __name__ == '__main__':
    __main__()