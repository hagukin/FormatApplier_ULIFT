# FormatApplier
하이그래프 코드 태그 자동화 툴  

# 하이그래프 태그 자동화 툴

원래 제가 쓰려고 만든 간단한 스크립트이지만 다른 분들이 쓰셔도 좋을 것 같아 공유합니다!

제가 못 찾은 버그가 있을 수 있지만 수동으로 작업하는 것보다는 훨씬 빠르게 작업할 수 있습니다

현재는 파이썬만 지원하지만 유사한 문법 구조를 가진 다른 언어로도 확장할 수 있게 

코드를 제작해 두었습니다.

### 사용방법

1. in 폴더에 태그를 추가할 코드 파일들을 추가합니다. (파일 형식은 자유)
이때 코드가 코딩 컨벤션에 맞게 작성된 상태여야 합니다.
2. formatApplier.py를 실행합니다.
3. out 폴더에 태그가 추가된 .txt 파일들이 생성됩니다.

각종 설정은 config/cfg.json 파일의 값을 수정하거나 값을 추가/삭제해서 변경할 수 있습니다.

태그 자동화를 원하는 함수/키워드를 추가하거나 태그 색상을 수정하거나

태그 specifier 기본값을 변경하는 등의 자잘한 설정들은 코드를 건드리지 않고 조정할 수 있습니다.

설정을 초기화하려면 config/cfg.json 파일을 삭제한 후 프로그램을 재실행하면 됩니다.

### 코딩 컨벤션

실습 문제 제작할 때 사용하는 컨벤션과 동일하게 작성하시면 됩니다.

다음 몇 가지 사항들은 더 주의해서 지켜야 합니다.

1. 빈칸은 _(언더바) 한 쌍과 그 사이에 적힌 정수 값으로 표기합니다.

언더바 이외의 다른 기호를 사용하고 싶은 경우, cfg.json에서 설정 변경이 가능합니다.

```python
print(_1_, _2_)
_3_(500, 300)
```

1. 인덴트는 공백 4칸 또는 탭(\t) 1번으로 처리합니다.

```python
if x:
  print(x) # X (공백 2칸)

if x:
	print(x) # O (탭 1번)

if x:
    print(x) # O (공백 4칸)
```

1. 연산자를 사용할 때 피연산자와 연산자 사이에 띄어쓰기를 사용해야 합니다.

```python
print(i+1, i*3) # X
print(i + 1, i + 3) # O
```

1. 파이썬 내장함수 / 키워드와 중복되는 변수명을 피해야 합니다.

```python
sum = 45 # X, 내장함수 sum과 중복
my_sum = 45 # O
```


### 사용 예시

in

```
# f-string 지원
s = f"텍스트 {var1} 텍스트 {var_2} 텍스트"

# datatype 구별해서 지원
string = "123"
integer = 123

# 실수형 literal 지원
x = 123 - 456
numbers = [-1.345, 1.23, 0, -459, 333, 293.58]

# 인덴트 지원
if True:
    print("hi")
    if False:
        print("hi")
    else:
        print("hi")
else:
    print("hi")

# 중첩 자료구조 지원
nested_datastructure = [
    [1,"2",3],
    (4,5,6),
    {7,8,"9"}
]

# 변수명 내에서의 숫자, 내장함수, 키워드 사용 감지
var1 = 1
var_2 = 2
myprint = 555
my_print = 553
printer = 2134
print(123)
ifnot = 0
if not var1:
    print("X")

# string 내에서의 숫자, 내장함수, 키워드 사용 감지
string = "123 if print()"
```

out

```
<green># f-string 지원</green>
s = <blue>f</blue><orange>"텍스트 </orange><pink>{</pink>var1<pink>}</pink><orange> 텍스트 </orange><pink>{</pink>var_2<pink>}</pink><orange> 텍스트"</orange>

<green># datatype 구별해서 지원</green>
string = <orange>"123"</orange>
integer = <mint>123</mint>

<green># 실수형 literal 지원</green>
x = <mint>123</mint> - <mint>456</mint>
numbers = [<mint>-1.345</mint>, <mint>1.23</mint>, <mint>0</mint>, <mint>-459</mint>, <mint>333</mint>, <mint>293.58</mint>]

<green># 인덴트 지원</green>
<pink>if</pink> True:
&emsp;&emsp;&emsp;&emsp;<lemon>print</lemon>(<orange>"hi"</orange>)
&emsp;&emsp;&emsp;&emsp;<pink>if</pink> False:
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<lemon>print</lemon>(<orange>"hi"</orange>)
&emsp;&emsp;&emsp;&emsp;<pink>else</pink>:
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<lemon>print</lemon>(<orange>"hi"</orange>)
<pink>else</pink>:
&emsp;&emsp;&emsp;&emsp;<lemon>print</lemon>(<orange>"hi"</orange>)

<green># 중첩 자료구조 지원</green>
nested_datastructure = [
&emsp;&emsp;&emsp;&emsp;[<mint>1</mint>,<orange>"2"</orange>,<mint>3</mint>],
&emsp;&emsp;&emsp;&emsp;(<mint>4</mint>,<mint>5</mint>,<mint>6</mint>),
&emsp;&emsp;&emsp;&emsp;<pink>{</pink><mint>7</mint>,<mint>8</mint>,<orange>"9"</orange><pink>}</pink>
]

<green># 변수명 내에서의 숫자, 내장함수, 키워드 사용 감지</green>
var1 = <mint>1</mint>
var_2 = <mint>2</mint>
myprint = <mint>555</mint>
my_print = <mint>553</mint>
printer = <mint>2134</mint>
<lemon>print</lemon>(<mint>123</mint>)
ifnot = <mint>0</mint>
<pink>if</pink> <pink>not</pink> var1:
&emsp;&emsp;&emsp;&emsp;<lemon>print</lemon>(<orange>"X"</orange>)

<green># string 내에서의 숫자, 내장함수, 키워드 사용 감지</green>
string = <orange>"123 if print()"</orange>
```