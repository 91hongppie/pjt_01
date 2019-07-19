import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력 => reader에 파일이 들어있음
    movieCd=[]
    # 한줄씩 읽는다.
    for row in reader:
        movieCd.append(row['movieCd'])
        
    result = {}
    for i in movieCd:
        key = config('KEY')
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={i}'
        api_data = requests.get(url).json()

        # pprint(api_data)  
        # 주간/주말 박스오피스 데이터 리스트로 가져오기.
        movies = api_data.get('movieInfoResult').get('movieInfo')
        for movie in movies:
            code = movies.get('movieCd')
            result[code]={
                'movieCd' : movies.get('movieCd'),
                'movieNm' : movies.get('movieNm'),
                'movieNmEn' : movies.get('movieNmEn'),
                'watchGradeNm' : movies.get('audits')[0].get('watchGradeNm') if movies.get('audits') else None,
                'openDt' : movies.get('openDt'),
                'showTm' : movies.get('showTm'),
                'genre' : movies.get('genres')[0].get('genre'),
                'peopleNm' : movies.get('directors')[0].get('peopleNm') if movies.get('directors') else None
        }

with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 데이터들의 필드 이름을 미리 정한다.
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'watchGradeNm', 'openDt', 'showTm', 'genre', 'peopleNm')
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
    for movie in result.values():
        writer.writerow(movie)