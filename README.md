# FormatApplier
하이그래프 코드 태그 자동화 툴  
  
## Supported languages
* Python  
  
추가 예정  
  
## How to use
1. in 폴더에 코드가 담긴 파일을 추가합니다. (파일 형태는 자유)  
2. 프로그램을 실행합니다.  
3. out 폴더에 태그가 추가 완료된 .txt 파일이 생성됩니다.  
  
프로그램의 세부적인 설정은 config 폴더의 cfg.json을 수정해 조작할 수 있습니다.  
설정을 초기화하려면 cfg.json 파일을 삭제하고 프로그램을 다시 실행하시면 됩니다.  
  
## Updates
#### 20230707  
* 파이썬 지원  
* 파이썬 내장함수, 키워드, fstring, string, 주석 color 태그 자동화  
* 빈칸 태그 자동화  
#### 20230710
* 파이썬 수 literal, 중괄호 자동화
* indent 자동화
  
## Standards
### 0. 공통
#### 빈칸 태그
빈칸은 _(언더바) 1쌍과, 그 사이에 적힌 정수값으로 표기합니다.  
함수명을 빈칸으로 사용하는 경우, 빈칸 바로 옆에 소괄호를 붙여 작성합니다  
```python
x = _1_("Hello World")
```  
그 밖의 모든 경우, 빈칸 바로 뒤에는 띄어쓰기가 와야 합니다  
```python
y = _2_ + 55 # O, 정상동작
y = _2_+ 55 # X, _2_와 + 사이가 붙어있음.
```
만약 빈칸을 표시할 때 _(언더바) 대신 다른 기호를 사용하고 싶다면,  
cfg.json["blanks"][원하는 언어명]["blank_indicator"] 에서 수정이 가능합니다.  
또 blank 태그 내부에서 사용하는 specifiers를 추가하거나 값을 수정하는 것도 가능합니다.  

### 인덴트
인덴트는 공백 4칸 / 탭 1번으로 처리합니다.  
따라서 in에 코드를 입력할 때 해당 형식에 맞추어 입력하는 것이 권장됩니다.  
인덴트 간격은 cfg.json["indents"][원하는 언어명]["indent_size"] 에서 수정이 가능합니다.  

### 1. Python
#### 색상 태그
현재 색상 태그 자동화를 지원하는 대상은 다음과 같습니다.  
* 주석
* 문자열
* 내장함수
* 키워드  
* 중괄호 (단, fstring 내의 중괄호 제외)
* 정수, 실수 리터럴  
만약 어떤 대상의 태그 색상을 변경하거나,  
혹은 어떤 특정한 함수/키워드를 자동화 대상에 추가하고 싶다면  
cfg.json["colors"][원하는 언어명][...] 에서 수정이 가능합니다.  
  
### 2. Javascript
지원 예정

### 3. C
지원 예정
  

