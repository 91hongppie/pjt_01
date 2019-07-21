# pjt_01

## 1. Project

- ### 영화진흥위원회 오픈 API로 영화에 대한 데이터수집 및 가공

  ### 1) 요청 조건 

  #### 	1. 주간(월~일)까지 기간의 데이터를 조회합니다. 

  #### 	2. 조회 기간은 총 50주이며, 기준일(마지막 일자)은 2019년 7월 13일입니다. 

  #### 	3. 다양성 화/상업 화를 모두 포함하여야 합니다. 

  #### 	4. 한국/외국 화를 모두 포함하여야 합니다. 

  #### 	5. 모든 상영지역을 포함하여야 합니다

## 2. 01.py

- #### 50주 차의 정보를 가장 최근 날짜부터 받기위해 설정합니다.

```python
for i in range(50):
    key = config('KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')
```

- #### 가장 최근의 정보부터 50주차 전까지 targetDt 를 입력하여 데이터를 .json 형식으로 받습니다.

```python

url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={key}&targetDt={targetDt}&weekGb=0'
    api_data = requests.get(url).json()
```

- #### movies = 영화에 대한 정보를 받습니다.

- #### 날짜를 거꾸로 돌리며 데이터를 얻기 때문에 중복 방지를 위해 if 문을 삽입합니다.

```python
  movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    #pprint(movies)
    
    for movie in movies:
        code = movie.get('movieCd')
        if code not in result: 

            result[code] = {
                'movieCd' : movie.get('movieCd'),
                'movieNm' : movie.get('movieNm'),
                'audiAcc' : movie.get('audiAcc')
```

- #### fieldnames에 저장할 데이터들의 필드 이름을 정합니다.

- #### 필드 이름을 csv 파일 최상단에 작성합니다.

```python
with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)
```

## 3. 02.py

- #### boxoffice.csv 파일에서 필요한 정보를 추출합니다.

```python
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) 
    movieCd=[]
    for row in reader:
        movieCd.append(row['movieCd'])
```

- #### 추출한 정보를 이용하여 영화에 대한 정보를 얻기위한 url에 입력합니다.

- #### .json 형식으로 받아서 for 문을 이용하여 필요한 정보를 얻습니다.

- #### 누락된 부분이 있는 항목은 if 문을 이용하여 해결합니다.

```python
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
```



## 4. 03.py

- #### movie.csv 에서 감독명과 영화명을 받아옵니다.

- #### url에서 얻은 데이터를 통해 영화인 분야, 필모를 추출합니다.

- #### 영화인의 필모에 해당 영화제목이 들어있으면 if문을 실행합니다.

- #### if 문에서 directors에 감독코드를 추출하여 url2에 입력하고 영화인 코드와 이름 정보를 얻습니다.

```python
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
```

## 5. 시행착오

- #### 01.py에서 정보를 dictrionary로 정리하는데 어려움이 있었습니다.
- #### 02.py에서  boxoffice.csv에서 누락된 정보가 있어서 해결방법을 찾기위한 어려움이 있었습니다.
- #### 03.py에서 감독과 동명이인의 정보가 나와서 if 문으로 해결하고 result에 마지막 정보만 저장되어 해결하는데 많은 시행착오가 있었습니다.