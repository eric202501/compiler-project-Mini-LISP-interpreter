# MINI-LISP Interpreter Project 

Compiler Lisp Interpreter project，支援基本語法與函式呼叫。更多詳細語言介紹可參考 PDF 說明或查看原始碼。

## 功能特色

### Basic Features
- Syntax Validation
- Print
- Numerical Operations
- Logical Operations
- if Expression
- Variable Definition
- Function
- Named Function

### Bonus Features
- Recursion
- Type Checking
- First-class Function

## 技術細節
### 繼承 dict 的 Env 類別
在 interpreter.py 中，Env 類別繼承自 Python 的內建 dict，用來維護變數綁定及其對應值。這樣的設計允許使用字典的所有功能，同時增加了查找父環境的功能。

```python

class Env(dict):
    def __init__(self, parent=None):
        super().__init__(base_func)
        self.parent = parent

    def lookup(self, name):
        if name in self:
            return self[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            print(f"未定義{name}符號")
            exit(0)
```
### 深度優先搜尋 (DFS) 遍歷 AST 樹
在該直譯器中，使用深度優先搜尋 (DFS) 遍歷抽象語法樹 (AST)，並將子節點的數值傳遞回父節點。

```python
def interpret_ast(node, env):
    if isinstance(node, Token):
        # 根據 Token 類型返回對應的值
        if node.type == "NUMBER":
            return int(node.value)
        elif node.type == "BOOL_VAL":
            return node.value == "#t"
        elif node.type == "ID":
            return env.lookup(node.value)
        else:
            print("error 2")
            exit(0)

    if isinstance(node, Tree):
        rule = node.data
        if rule == "start":
            for child in node.children:
                interpret_ast(child, env)
        elif rule == "print_num":
            val = interpret_ast(node.children[0], env)
            return env["print_num"](val)
```

## 使用方式
安裝 Python 3 與 lark

執行：
```bash
python main.py < test.lsp
