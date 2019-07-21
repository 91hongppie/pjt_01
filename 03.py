import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint


with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력 => reader에 파일이 들어있음
    movieCd=[]
    movieNm=[]
    # 한줄씩 읽는다.
    for row in reader:
        movieCd.append(row['peopleNm'])
        movieNm.append(row['movieNm'])
    pprint(movieNm)
    result = {}
    for peopleNm in movieCd:
        key = config('KEY')
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={peopleNm}'
        api_data = requests.get(url).json()
        repRoleNm = api_data.get('peopleListResult').get('peopleList')[0].get('repRoleNm') # 영화인 분야 
        filmoNames = api_data.get('peopleListResult').get('peopleList')[0].get('filmoNames') # 필모
        # print(repRoleNm, filmoNames)
        for j in range(0, len(movieNm)):    
            if movieNm[j] in filmoNames: # 감독이름 정보 안에 해당 영화제목이 있으면 if문 실행
                directors = api_data.get('peopleListResult').get('peopleList')[0].get('peopleCd') # api_data에서 감독 코드 추출
                url2 = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?key={key}&peopleCd={directors}' # 감독 코드를 입력하여 영화인 정보를 가져온다.
                api_data2 = requests.get(url2).json() # json 형태로
                peopleCd = api_data2.get('peopleInfoResult').get('peopleInfo').get('peopleCd')
                peopleNm = api_data2.get('peopleInfoResult').get('peopleInfo').get('peopleNm')
                # pprint(api_data)
                movies = api_data2.get('peopleInfoResult').get('peopleInfo')
                code = movies.get('peopleCd')
                result[code]={
                    'peopleCd' : peopleCd,
                    'peopleNm' : peopleNm,
                    'repRoleNm' : repRoleNm,
                    'filmoNames' : filmoNames
                }
# pprint(result)
with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 데이터들의 필드 이름을 미리 정한다.
    fieldnames = ('peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
    for movie in result.values():
        writer.writerow(movie)