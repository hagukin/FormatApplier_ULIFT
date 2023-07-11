#### 김하국 작성 ####

########## File Structure #########
# formatApplier.exe
# config
# └─cfg.json
# in
# └─code files / texts (Optional)
# out
####################################

import typing
from collections.abc import Mapping
import re

import json
from os import listdir
from os.path import isfile, join

class FormatConfig():
    DEFAULT_CONFIG: dict = {
        "toggle" : {
            "color_formatting" : True,
            "blank_formatting" : True,
            "indent_formatting" : True,
        },
        "colors" : {
            "python" : {
                "built_in_functions" : {
                    "print" : "lemon",
                    "len" : "lemon",
                    "__init__" : "lemon",
                    "__next__" : "lemon",

                    "range" : "mint",
                    "type" : "mint",
                    "tuple" : "mint",
                    "list" : "mint",
                    "set" : "mint",
                    "dict" : "mint",
                    "map" : "mint",
                },
                "keywords" : {
                    "for" : "pink",
                    "in" : "pink",
                    "if" : "pink",
                    "elif" : "pink",
                    "else" : "pink",
                    "break" : "pink",
                    "with" : "pink",
                    "import" : "pink",
                    "as" : "pink",
                    "try" : "pink",
                    "except" : "pink",
                    "finally" : "pink",

                    "def" : "blue",
                    "lambda" : "blue",
                    "class" : "blue",
                },
                "f_string_tag" : "blue",
                "string" : "orange",
                "comment" : "green",
                "f_string_bracket" : "pink",
                "f_string_bracket_inner" : "light-gray",
                "bracket" : "pink",
                "number" : "mint",
                "default" : "light-gray",
            },
        },
        "blanks" : {
            "python" : {
                "blank_indicator" : "_",
                "tag_name" : "blank",
                "specifiers" : {
                    "id" : None,
                    "size":'5'
                }
            }
        },
        "indents" : {
            "python" : {
                "indent_size" : 4,
                "replace_with" : "&emsp;"
            }
        },
        "encoding":"utf-8",
    }

    def __init__(self):
        self._config = None
        self.init_config()

    @property
    def config(self) -> dict:
        return self._config

    def read_config(self) -> None:
        with open(".\\config\\cfg.json", 'r') as f:
            data = json.load(f)
        self._config = json.dumps(data)
        return

    def init_config(self) -> None:
        try:
            self.read_config()
            if self._config == None or type(self._config) != dict:
                raise Exception("cfg.json을 찾는 데 실패했습니다, 기본값을 사용합니다.")
        except:
            self._config = FormatConfig.DEFAULT_CONFIG
            with open(".\\config\\cfg.json", mode='w+', encoding=self.config["encoding"]) as cfg:
                json.dump(self._config, cfg, indent=4)


class FormatApplier():
    IN_PATH = ".\\in\\"
    OUT_PATH = ".\\out\\"

    def __init__(self, lang: str):
        self._lang = lang
        self._config = FormatConfig().config

    @property
    def lang(self) -> str:
        return self._lang
    
    @property
    def config(self) -> dict:
        return self._config
    
    def export_code(self, code: list[str], textfile_name: str) -> None:
        try:
            with open(FormatApplier.OUT_PATH + textfile_name, mode='w+', encoding=self.config["encoding"]) as export:
                for line in code:
                    export.write(line)
        except Exception as e:
            print(f"파일 export 중 문제가 발생했습니다 - {e.__str__()}")
        return
    
    def run(self) -> None:
        file_paths: list[str] = [f for f in listdir(FormatApplier.IN_PATH) if isfile(join(FormatApplier.IN_PATH, f))]
        for file_name in file_paths:
            if file_name[-8:] == ".gitkeep":
                continue # ignore gitkeep
            with open(FormatApplier.IN_PATH + file_name, "rt", encoding="UTF8") as file:
                code: list[str] = file.readlines()
                textfile_name = file_name[:file_name.index(".")+1] + "txt"
                self.export_code(self.apply_format(code), textfile_name)
        print("작업이 완료되었습니다.")
        return
    
    def apply_color_format(self, line: str) -> str:
        # line의 idx번 문자부터 색상 포맷을 추가한다
        raise NotImplementedError()
    
    def apply_blank_format(self, line: str) -> str:
        # line의 idx번 문자부터 빈칸 포맷을 추가한다
        raise NotImplementedError()
    
    def apply_indent_format(self, line: str) -> str:
        # line의 idx번 문자부터 인덴트 포맷을 추가한다
        raise NotImplementedError()
    
    def return_overlapped(self, line: str) -> list[bool]:
        # 각 구간 별 어떤 태그를 적용중인지를 리스트로 반환.
        overlapped = [""] * len(line)
        new_line = line
        tag_opened = -1
        for i in range(len(new_line)-1):
            if tag_opened == -1 and new_line[i] == "<":
                tag_opened = i
            if new_line[i:i+2] == "</" and tag_opened != -1:
                tag_end = new_line.find(">",i)
                for j in range(tag_opened, i):
                    overlapped[j] = new_line[i+2:tag_end] # 태그명으로 저장
        return overlapped
    
    def find_all_numbers(self, line: str) -> list[any]:
        # 어떤 문자열 내의 모든 부동소수점, 정수 값들을 찾아 반환한다
        found = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
        return found
    
    def apply_format(self, code: list[str]) -> list[str]:
        raise NotImplementedError()


class PythonFormatApplier(FormatApplier):
    def __init__(self, lang: str):
        super().__init__(lang)

    def apply_format(self, code: list[str]) -> list[str]:
        for code_idx in range(len(code)):
            if self.config["toggle"]["color_formatting"]:
                code[code_idx] = self.apply_color_format(code[code_idx])
        for code_idx in range(len(code)):
            if self.config["toggle"]["blank_formatting"]:
                code[code_idx] = self.apply_blank_format(code[code_idx])
        for code_idx in range(len(code)):
            if self.config["toggle"]["color_formatting"]:
                code[code_idx] = self.apply_color_format_number_literal(code[code_idx])
        for code_idx in range(len(code)):
            if self.config["toggle"]["indent_formatting"]:
                code[code_idx] = self.apply_indent_format(code[code_idx])
        return code

    def apply_tag(self, line: str, head_idx: int, tail_idx: int, tag_name: str) -> str: # TODO: tag specifier 입력 자동화
        string = line[:head_idx] + f"<{tag_name}>" + line[head_idx:tail_idx] + f"</{tag_name}>" + line[tail_idx:]
        return string
    
    def apply_tag_head(self, line: str, head_idx: int, tag_name: str) -> str:
        return line[:head_idx] + f"<{tag_name}>" + line[head_idx:]
    
    def apply_tag_tail(self, line: str, tail_idx: int, tag_name: str) -> str:
        return line[:tail_idx] + f"</{tag_name}>" + line[tail_idx:]
    
    def apply_blank_tag(self, line: str, idx: int, tag_name: str, blank_num: int, specifiers: dict) -> str:
        string = line[:idx] + f"<{tag_name} "
        for spec_name, spec_val in specifiers.items():
            if spec_name == "id":
                spec_val = blank_num
            string += spec_name + "=" + f"\'{spec_val}\'"
        string += ">"
        string += f"</{tag_name}>"
        string += line[idx:]
        return string
    
    def apply_color_format_builtin(self, line: str) -> str:
        new_line = line
        for builtin in self.config["colors"]["python"]["built_in_functions"].keys():
            found = new_line.find(builtin)
            while found != -1:
                tag_name = self.config["colors"]["python"]["built_in_functions"][builtin]
                if (found != 0 and new_line[found-1] != " ") or (found+1 < len(new_line) and new_line[found+len(builtin)] != "("):
                    pass # 내장함수를 사용되는 경우가 아닌 경우 (e.g. player_len에서의 len 무시)
                else:
                    new_line = self.apply_tag(new_line, found, found+len(builtin), tag_name)
                found = new_line.find(builtin, int(found) + len(builtin) + (len(tag_name)*2) + 5) # 태그 추가로 인해 늘어난 길이만큼 더한다 = tag_name*2 + 5 (<x> </x>) 
        return new_line
    
    def apply_color_format_keyword(self, line: str) -> str:
        new_line = line
        for keyword in self.config["colors"]["python"]["keywords"].keys():
            found = new_line.find(keyword)
            while found != -1:
                tag_name = self.config["colors"]["python"]["keywords"][keyword]
                add_idx = (len(tag_name)*2) + 5
                if (found != 0 and not new_line[found-1].isspace()) or (found+len(keyword) < len(new_line) and (not new_line[found+len(keyword)].isspace() and new_line[found+len(keyword)] != ":")):
                    add_idx = 0 # 태그 추가 안했으므로
                    pass # 키워드로 사용되는 경우가 아닌 경우 (e.g. will_continue = 1 의 continue 무시)
                else:
                    new_line = self.apply_tag(new_line, found, found+len(keyword), tag_name)
                found = new_line.find(keyword, found + len(keyword) + add_idx) # 태그 추가로 인해 늘어난 길이만큼 더한다 = tag_name*2 + 5 (<x> </x>) 
        return new_line
    
    def apply_color_format_fstring(self, line: str) -> str:
        new_line = line
        search_for = "f\""
        found = new_line.find(search_for)
        while found != -1:
            tag_name = self.config["colors"]["python"]["f_string_tag"]
            new_line = self.apply_tag(new_line, found, found+len("f"), tag_name)
            found = new_line.find(search_for, int(found) + len("f") + (len(tag_name)*2) + 5) # 태그 추가로 인해 늘어난 길이만큼 더한다 = tag_name*2 + 5 (<x> </x>) 
        return new_line
    
    def apply_color_format_f_string_bracket(self, line: str) -> str:
        # f string 내부의 중괄호 및 중괄호 내부의 코드에 대해 태그를 추가한다
        new_line = line
        str_tag = self.config["colors"]["python"]["string"] # 문자열
        br_tag = self.config["colors"]["python"]["f_string_bracket"] # f string 내부의 괄호 색상
        inner_tag = self.config["colors"]["python"]["f_string_bracket_inner"] # 괄호 내부의 코드 색상

        br_begin = new_line.find("{")
        br_end = new_line.find("}")

        while br_begin != -1 and br_end != 1:
            overlapped = self.return_overlapped(new_line)
            if overlapped[br_begin] != str_tag or overlapped[br_end] != str_tag: # NOTE: 좋은 방식은 아님 (string이 아닌 곳에서도 string과 동일한 태그를 사용할 수 있음)
                br_begin = new_line.find("{", br_end+1)
                br_end = new_line.find("}", br_end+1)
                continue
            
            new_line = self.apply_tag_tail(new_line, br_begin, str_tag)
            br_end += 3+len(str_tag) # </x>
            br_begin += 3+len(str_tag)

            new_line = self.apply_tag(new_line, br_begin, br_begin+len("{"), br_tag)
            br_end += (2+len(br_tag))*2 + 1 # <x></x>
            br_begin += (2+len(br_tag))*2 + 1

            new_line = self.apply_tag(new_line, br_begin + 1, br_end, inner_tag)
            br_end += (2+len(inner_tag))*2 + 1

            new_line = self.apply_tag(new_line, br_end, br_end+len("}"), br_tag)
            br_end += (2+len(br_tag))*2 + 1 # <x></x>

            new_line = self.apply_tag_head(new_line, br_end+1, str_tag)
            br_end += 2+len(str_tag) # <x>

            br_begin = new_line.find("{", br_end)
            if br_begin == -1:
                break
            br_end = new_line.find("}", br_begin+1)
        return new_line
    
    def apply_color_format_bracket(self, line: str) -> str:
        new_line = line
        br_begin = new_line.find("{")
        br_end = new_line.find("}", br_begin+1)

        while br_begin != -1 and br_end != 1:
            overlapped = self.return_overlapped(new_line)
            if overlapped[br_begin] or overlapped[br_end]:
                break

            tag_name = self.config["colors"]["python"]["bracket"]

            new_line = self.apply_tag(new_line, br_begin, br_begin+1, tag_name)
            br_end += (2+len(tag_name))*2 + 1
            new_line = self.apply_tag(new_line, br_end, br_end+1, tag_name)
            br_end += (3+len(tag_name))*2 + 1

            br_begin = new_line.find("{", br_end+1)
            if br_begin == -1:
                break
            br_end = new_line.find("}", br_begin+1)
        return new_line
    
    def apply_color_format_string(self, line: str) -> str:
        new_line = line
        str_begin = new_line.find("\"")
        str_end = new_line.find("\"", str_begin+1)

        while str_begin != -1 and str_end != 1:
            tag_name = self.config["colors"]["python"]["string"]
            new_line = self.apply_tag_head(new_line, str_begin, tag_name)
            new_line = self.apply_tag_tail(new_line, str_end+1+(2+len(tag_name)), tag_name)
            str_begin = new_line.find("\"", int(str_begin) + (str_end-str_begin+1) + (len(tag_name)*2) + 5) # string 길이 + 태그 길이
            if str_begin == -1:
                break
            str_end = new_line.find("\"", str_begin+1)
        return new_line
    
    def apply_color_format_comment(self, line: str) -> str:
        new_line = line
        search_for = "#"
        found = new_line.find(search_for)
        if found != -1:
            tag_name = self.config["colors"]["python"]["comment"]
            new_line = self.apply_tag_head(new_line, found, tag_name)
            new_line = self.apply_tag_tail(new_line, len(new_line)-1, tag_name) 
        return new_line
    
    def apply_color_format_number_literal(self, line: str) -> str:
        new_line = line
        numbers: list[any] = self.find_all_numbers(new_line) # 모든 가능한 수 타입 찾아 리스트로 반환

        search_from = 0
        for number in numbers:
            overlapped = self.return_overlapped(new_line)
            search_for = str(number)

            found = new_line.find(search_for, search_from)
            if found == -1:
                print("숫자에 색상 태그를 입히는 과정에서 에러가 발생했습니다.")
                break
            if found > 0 and new_line[found-1].isalpha():
                continue # num1 과 같이 변수명 뒤의 숫자 허용
            if overlapped[found]:
                continue # 태그 중복 방지

            tag_name = self.config["colors"]["python"]["number"]
            new_line = self.apply_tag(new_line, found, found+len(search_for), tag_name)
            search_from = found + 5 + (2*len(tag_name)) + len(search_for)
        return new_line

    def apply_color_format(self, line: str) -> str:
        new_line = self.apply_color_format_builtin(line)
        new_line = self.apply_color_format_keyword(new_line)
        new_line = self.apply_color_format_fstring(new_line)
        new_line = self.apply_color_format_string(new_line)
        new_line = self.apply_color_format_bracket(new_line)
        new_line = self.apply_color_format_f_string_bracket(new_line)
        new_line = self.apply_color_format_comment(new_line)
        return new_line
    
    def apply_blank_format(self, line: str) -> str:
        def specifiers_len(specifiers: dict):
            # <blank id='2' size='5'></blank> 일때 
            # " id='2' size='5'"의 길이를 반환한다
            l = 0
            n = len(specifiers.keys())
            for k, v in specifiers.items():
                if k == "id":
                    v = "." # TODO FIXME: 만약 blank가 10개 이상 있다면 에러가 발생한다!
                l += len(k) # specifier 이름 길이 합
                l += len(v) # value 길이 합
            l += n*3 # = 기호 한 개와 ' 기호 두개
            l += n # 공백문자
            return l

        new_line = line
        search_for = self.config["blanks"]["python"]["blank_indicator"]
        blank_begin = new_line.find(search_for)
        blank_end = new_line.find(search_for, blank_begin+1)
        blank_num = -1

        while blank_begin != -1 and blank_end != 1:
            try:
                blank_num = int(new_line[blank_begin+len(search_for):blank_end])
            except ValueError as e:
                blank_begin = blank_end
                blank_end = blank_end = new_line.find(search_for, blank_end+1)
                continue
            except Exception as e:
                print("코드의 빈칸 태그를 찾는 과정에서 알 수 없는 오류가 발생했습니다.")
                return
            
            new_line = new_line[:blank_begin] + new_line[blank_end+len(search_for):] # 기존 blank indicator 삭제
            tag_name = self.config["blanks"]["python"]["tag_name"]
            specifiers = self.config["blanks"]["python"]["specifiers"]

            new_line = self.apply_blank_tag(new_line, blank_begin, tag_name, blank_num, specifiers)

            search_start = int(blank_begin) + (len(tag_name)*2) + 5 + specifiers_len(specifiers)
            blank_begin = new_line.find(search_for, search_start) # 태그 길이 + 태그 specifiers 길이
            if blank_begin == -1:
                break
            blank_end = new_line.find(search_for, blank_begin+1)
        return new_line
    
    def apply_indent_format(self, line: str) -> str:
        new_line = line
        x = self.config["indents"]['python']["replace_with"] * self.config["indents"]['python']["indent_size"]
        new_line = new_line.replace('\t', x) # 탭
        new_line = new_line.replace(" " * self.config["indents"]['python']["indent_size"], x) # 공백
        return new_line
    
def start() -> int:
    fa = PythonFormatApplier("python")
    fa.run()
    input("종료하시려면 아무 키나 누르십시오.")
    return 0

if __name__ == "__main__":
    start()