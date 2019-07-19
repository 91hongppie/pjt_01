import requests
import csv
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint


# key = config('395c9e0d5f86760d61028514ba45cf81')
key =  config('KEY')
targetDt = '20120101'

base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?'
base_url += f'key={key}&targetDt={targetDt}'
movie_res =requests.get(base_url)
information = movie_res.json()

movies = information.get('boxOfficeResult').get('weeklyBoxOfficeList')
# print(movies)
Nm = []
Cd = []
audi = []
for i in range(0, len(movies)):
    Nm.append(movies[i]['movieNm'])
    Cd.append(movies[i]['movieCd'])
    audi.append(movies[i]['audiAcc'])

re = []
for i in range(0, len(movies)):
    re.append({Nm[i], Cd[i], audi[i]})

print(re)
# movieCd = []
# for i in range(0, len(movies)):
#     movieCd.append(movies[i]['movieCd'])
# print(movieCd)
# ya = list()
# last = {}
# for i in range (0, len(information['boxOfficeResult']['weeklyBoxOfficeList'])):
#     for key, value in information['boxOfficeResult']['weeklyBoxOfficeList'][i].items():    
#         for j in range(0, len(information['boxOfficeResult']['weeklyBoxOfficeList'][i])):
#             if key == 'movieCd' or key == 'movieNm' or key == 'audiAcc':
#                 last.update({key: value})
#                 ya.append(last)
# print(ya)


# with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('movieCd', 'movieNm', 'audiAcc')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()
#         for avenger in avengers:
#         writer.writerow(avenger)


#         # 딕셔너리를 순회하며 key를 통해 한줄씩(value를) 작성한다.
# for i in range (0, len(information['boxOfficeResult']['weeklyBoxOfficeList'])):
#     for key, value in information['boxOfficeResult']['weeklyBoxOfficeList'][i].items():
#         last.update({key: value})
# print(last)

# with open('boxoffice.csv', newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f)

#     # 한줄씩 읽는다.
#     for row in reader:
#         print(row["movieNm"])
#         print(row['MovieCd'])
#         print(row['audiAcc'])


# with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('movieCd', 'movieNm', 'audiAcc')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()

#         # 딕셔너리를 순회하며 key를 통해 한줄씩(value를) 작성한다.
#     for i in information['boxOfficeResult']['dailyBoxOfficeList']:
#         writer.writerow(i)

# with open('boxoffice.csv', newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f)

#     # 한줄씩 읽는다.
#     for row in reader:
#         print(row["movieNm"])
#         print(row['MovieCd'])
#         print(row['audiAcc'])


# print(information['boxOfficeResult']['dailyBoxOfficeList'][0]['movieNm'])
# print(information['boxOfficeResult']['dailyBoxOfficeList'][0]['movieCd'])
# print(information['boxOfficeResult']['dailyBoxOfficeList'][0]['audiAcc'])
# # with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
# #     fieldnames = ('movie_code', 'movie_name', 'total_audience')
# #     writer = csv.DictWriter(f, fieldnames=fieldnames)
# #     writer.writeheader()
