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
        
    key = config('KEY')
    result = {}
    for i in movieCd:
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={i}'
        api_data = requests.get(url).json()

        # pprint(api_data)  

        # 주간/주말 박스오피스 데이터 리스트로 가져오기.
        movies = api_data.get('movieInfoResult').get('movieInfo')
        
        # pprint(movies)


        # 영화 대표코드 / 영화명 / 누적관객수

#         # 영화정보가 담긴 딕셔너리 영화 대표 코드를 추출
#     for movie in movies:
#         code = movie.get('movieCd')
#         url2 = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={code}'
#         api_data2 = requests.get(url2).json()
        Nm = api_data2.get('movieInfoResult').get('movieInfo').get('movieNm')
        En = api_data2.get('movieInfoResult').get('movieInfo').get('movieNmEn')
        Grade = api_data2.get('movieInfoResult').get('audits')[0].get('watchGradeNm') if api_data2.get('movieInfoResult').get('audits') else None
        Dt = api_data2.get('movieInfoResult').get('movieInfo').get('openDt')
        showTm = api_data2.get('movieInfoResult').get('movieInfo').get('showTm')
        genre = api_data2.get('movieInfoResult').get('genres')[0].get('genre')
        peopleNm = api_data2.get('movieInfoResult').get('movieInfo').get('directors')[0].get('peopleNm')
        api_data2 = requests.get(url2).json()
#         if code not in result: 
#                 # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
#                 # 그게 가장 마지막 주 자료다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
#             result[code] = {
#                 'movieCd' : movie.get('movieCd'),
#                 'movieNm' : movie.get('movieNm'),
#                 'movieNmEn' : En,
#                 'watchGradeNm' : 'Grade',
#                 'openDt' : 'openDt',
#                 'showTm' : 'showTm',
#                 'genre' : 'genre'
#             }
#     pprint(result)

# with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
#     fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     for value in result.values():
#         print(value)
#         writer.writerow(value)