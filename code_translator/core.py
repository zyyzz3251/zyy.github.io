"""
代码互译系统核心引擎

数学模型:
  源码 Σ₁* 
     ↓  词法分析（σ₁）
  记号流 Tok₁*
     ↓  语法分析（parse₁）
  源AST AST₁
     ↓  AST映射（F）
  目标AST AST₂
     ↓  代码生成（Emit）
  目标代码 Σ₂*
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class TokenType(Enum):
    """记号类型"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    LITERAL = "LITERAL"
    PUNCTUATION = "PUNCTUATION"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    EOF = "EOF"


@dataclass
class Token:
    """记号"""
    type: TokenType
    value: str
    line: int = 1
    column: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        return f"Token({self.type.value}, {repr(self.value)}, L{self.line}:{self.column})"


@dataclass
class ASTNode:
    """抽象语法树节点"""
    node_type: str
    value: Any = None
    children: List['ASTNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        return f"AST({self.node_type}, children={len(self.children)})"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'type': self.node_type,
            'value': self.value,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata
        }


class Lexer:
    """词法分析器 (σ₁)"""
    
    def __init__(self, language: str = "python"):
        self.language = language
        self.keywords = self._get_keywords(language)
        self.operators = self._get_operators(language)
        self.punctuation = self._get_punctuation()
        
    def _get_keywords(self, language: str) -> set:
        keywords_map = {
            "python": {"def", "class", "if", "else", "elif", "for", "while", "return", 
                      "import", "from", "as", "try", "except", "finally", "with", "pass",
                      "lambda", "None", "True", "False", "and", "or", "not", "in", "is"},
            "javascript": {"function", "class", "if", "else", "for", "while", "return",
                         "const", "let", "var", "async", "await", "try", "catch", "finally",
                         "true", "false", "null", "undefined", "new", "this", "super"},
        }
        return keywords_map.get(language, set())
    
    def _get_operators(self, language: str) -> List[str]:
        return ["==", "!=", "<=", ">=", "&&", "||", "++", "--", "+=", "-=", 
                "*=", "/=", "=", "+", "-", "*", "/", "%", "<", ">", "&", "|", "^", "!"]
    
    def _get_punctuation(self) -> set:
        return {"(", ")", "{", "}", "[", "]", ";", ",", ".", ":"}
    
    def tokenize(self, source_code: str) -> List[Token]:
        """词法分析: σ₁(p) -> Tok₁*"""
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            col = 1
            i = 0
            
            while i < len(line):
                if line[i].isspace():
                    i += 1
                    col += 1
                    continue
                
                if i < len(line) - 1 and line[i:i+2] == "//":
                    tokens.append(Token(TokenType.COMMENT, line[i:], line_num, col))
                    break
                
                if line[i] in ('"', "'"):
                    quote = line[i]
                    j = i + 1
                    while j < len(line) and line[j] != quote:
                        j += 1
                    j += 1
                    tokens.append(Token(TokenType.LITERAL, line[i:j], line_num, col))
                    col += j - i
                    i = j
                    continue
                
                if line[i].isdigit():
                    j = i
                    while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                        j += 1
                    tokens.append(Token(TokenType.LITERAL, line[i:j], line_num, col))
                    col += j - i
                    i = j
                    continue
                
                if line[i].isalpha() or line[i] == '_':
                    j = i
                    while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                        j += 1
                    word = line[i:j]
                    token_type = TokenType.KEYWORD if word in self.keywords else TokenType.IDENTIFIER
                    tokens.append(Token(token_type, word, line_num, col))
                    col += j - i
                    i = j
                    continue
                
                found = False
                for op in sorted(self.operators, key=len, reverse=True):
                    if line[i:i+len(op)] == op:
                        tokens.append(Token(TokenType.OPERATOR, op, line_num, col))
                        col += len(op)
                        i += len(op)
                        found = True
                        break
                
                if found:
                    continue
                
                if line[i] in self.punctuation:
                    tokens.append(Token(TokenType.PUNCTUATION, line[i], line_num, col))
                    col += 1
                    i += 1
                    continue
                
                i += 1
                col += 1
        
        tokens.append(Token(TokenType.EOF, "", len(lines), len(lines[-1]) if lines else 1))
        return tokens


class Parser(ABC):
    """语法分析器基类"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, "")
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, "")
    
    def peek(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return Token(TokenType.EOF, "")
    
    @abstractmethod
    def parse(self) -> ASTNode:
        pass


class SimplePythonParser(Parser):
    """简化的Python语法分析器"""
    
    def parse(self) -> ASTNode:
        """解析为AST"""
        statements = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.KEYWORD:
                if self.current_token.value == "def":
                    statements.append(self._parse_function())
                elif self.current_token.value == "class":
                    statements.append(self._parse_class())
                else:
                    statements.append(self._parse_statement())
            else:
                statements.append(self._parse_statement())
        
        root = ASTNode("Program")
        root.children = statements
        return root
    
    def _parse_function(self) -> ASTNode:
        self.advance()
        name = "func"
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
        
        params = []
        if self.current_token.type == TokenType.PUNCTUATION and self.current_token.value == "(":
            self.advance()
            while self.current_token.type != TokenType.EOF and not (self.current_token.type == TokenType.PUNCTUATION and self.current_token.value == ")"):
                if self.current_token.type == TokenType.IDENTIFIER:
                    params.append(self.current_token.value)
                self.advance()
            if self.current_token.type == TokenType.PUNCTUATION:
                self.advance()
        
        func_node = ASTNode("FunctionDef")
        func_node.metadata["name"] = name
        func_node.metadata["params"] = params
        return func_node
    
    def _parse_class(self) -> ASTNode:
        self.advance()
        name = "Class"
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
        
        class_node = ASTNode("ClassDef")
        class_node.metadata["name"] = name
        return class_node
    
    def _parse_statement(self) -> ASTNode:
        stmt = ASTNode("Statement")
        while self.current_token.type != TokenType.EOF:
            self.advance()
        return stmt


class ASTMapper:
    """AST映射器 (F)"""
    
    def __init__(self, source_lang: str, target_lang: str):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.type_mapping = self._build_type_mapping()
    
    def _build_type_mapping(self) -> Dict[str, str]:
        return {
            "FunctionDef": "FunctionDeclaration",
            "ClassDef": "ClassDeclaration",
        }
    
    def map(self, source_ast: ASTNode) -> ASTNode:
        """映射AST: F(AST₁) -> AST₂"""
        target_ast = ASTNode(
            self.type_mapping.get(source_ast.node_type, source_ast.node_type),
            source_ast.value
        )
        target_ast.metadata = source_ast.metadata.copy()
        
        for child in source_ast.children:
            target_ast.children.append(self.map(child))
        
        return target_ast


class CodeGenerator(ABC):
    """代码生成器基类"""
    
    def __init__(self):
        self.output_lines: List[str] = []
        self.indent_level = 0
        self.indent_string = "    "
    
    def add_line(self, code: str = ""):
        if code:
            self.output_lines.append(self.indent_string * self.indent_level + code)
        else:
            self.output_lines.append("")
    
    def indent(self):
        self.indent_level += 1
    
    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)
    
    @abstractmethod
    def generate(self, ast: ASTNode) -> str:
        pass
    
    def get_code(self) -> str:
        return "\n".join(self.output_lines)


class PythonCodeGenerator(CodeGenerator):
    """Python代码生成器"""
    
    def generate(self, ast: ASTNode) -> str:
        self._generate_node(ast)
        return self.get_code()
    
    def _generate_node(self, node: ASTNode):
        if node.node_type == "Program":
            for child in node.children:
                self._generate_node(child)
        elif node.node_type == "FunctionDeclaration":
            name = node.metadata.get("name", "func")
            params = node.metadata.get("params", [])
            params_str = ", ".join(params)
            self.add_line(f"def {name}({params_str}):")
            self.indent()
            self.add_line("pass")
            self.dedent()
        elif node.node_type == "ClassDeclaration":
            name = node.metadata.get("name", "Class")
            self.add_line(f"class {name}:")
            self.indent()
            self.add_line("pass")
            self.dedent()
        
        for child in node.children:
            self._generate_node(child)


class JavaScriptCodeGenerator(CodeGenerator):
    """JavaScript代码生成器"""
    
    def generate(self, ast: ASTNode) -> str:
        self._generate_node(ast)
        return self.get_code()
    
    def _generate_node(self, node: ASTNode):
        if node.node_type == "Program":
            for child in node.children:
                self._generate_node(child)
        elif node.node_type == "FunctionDeclaration":
            name = node.metadata.get("name", "func")
            params = node.metadata.get("params", [])
            params_str = ", ".join(params)
            self.add_line(f"function {name}({params_str}) {{")
            self.indent()
            self.add_line("// function body")
            self.dedent()
            self.add_line("}")
        elif node.node_type == "ClassDeclaration":
            name = node.metadata.get("name", "Class")
            self.add_line(f"class {name} {{")
            self.indent()
            self.add_line("constructor() {}")
            self.dedent()
            self.add_line("}")
        
        for child in node.children:
            self._generate_node(child)


class CodeTranslator:
    """代码互译器"""
    
    def __init__(self, source_lang: str, target_lang: str):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.lexer = Lexer(source_lang)
        self.parser = SimplePythonParser([])
        self.mapper = ASTMapper(source_lang, target_lang)
        self.generator = self._get_generator(target_lang)
    
    def _get_generator(self, lang: str) -> CodeGenerator:
        generators = {
            "python": PythonCodeGenerator,
            "javascript": JavaScriptCodeGenerator,
        }
        return generators.get(lang, PythonCodeGenerator)()
    
    def translate(self, source_code: str) -> str:
        """完整转译流程: Emit ∘ F ∘ parse₁ ∘ σ₁ (p) = q"""
        tokens = self.lexer.tokenize(source_code)
        self.parser = SimplePythonParser(tokens)
        source_ast = self.parser.parse()
        target_ast = self.mapper.map(source_ast)
        target_code = self.generator.generate(target_ast)
        return target_code


if __name__ == "__main__":
    source_code = """def hello(name):
    return name

class MyClass:
    pass"""
    
    translator = CodeTranslator("python", "javascript")
    result = translator.translate(source_code)
    print(result)
