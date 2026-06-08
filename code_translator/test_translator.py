"""
代码互译系统 - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_translator.core import (
    Token, TokenType, ASTNode, Lexer, SimplePythonParser,
    ASTMapper, PythonCodeGenerator, JavaScriptCodeGenerator,
    CodeTranslator
)


class TestLexer(unittest.TestCase):
    """测试词法分析器"""
    
    def setUp(self):
        self.lexer = Lexer("python")
    
    def test_tokenize_def(self):
        tokens = self.lexer.tokenize("def hello():")
        self.assertEqual(tokens[0].type, TokenType.KEYWORD)
        self.assertEqual(tokens[0].value, "def")
    
    def test_tokenize_identifiers(self):
        tokens = self.lexer.tokenize("x = 42")
        identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(identifiers), 1)
    
    def test_tokenize_numbers(self):
        tokens = self.lexer.tokenize("x = 42")
        literals = [t for t in tokens if t.type == TokenType.LITERAL]
        self.assertTrue(any(t.value == "42" for t in literals))
    
    def test_tokenize_class(self):
        tokens = self.lexer.tokenize("class MyClass:")
        keywords = [t for t in tokens if t.type == TokenType.KEYWORD]
        self.assertTrue(any(t.value == "class" for t in keywords))


class TestParser(unittest.TestCase):
    """测试语法分析器"""
    
    def test_parse_function(self):
        lexer = Lexer("python")
        tokens = lexer.tokenize("def hello(name):")
        parser = SimplePythonParser(tokens)
        ast = parser.parse()
        
        self.assertEqual(ast.node_type, "Program")
        func = ast.children[0]
        self.assertEqual(func.node_type, "FunctionDef")
        self.assertEqual(func.metadata["name"], "hello")
    
    def test_parse_class(self):
        lexer = Lexer("python")
        tokens = lexer.tokenize("class Calculator:")
        parser = SimplePythonParser(tokens)
        ast = parser.parse()
        
        cls = ast.children[0]
        self.assertEqual(cls.node_type, "ClassDef")
        self.assertEqual(cls.metadata["name"], "Calculator")


class TestASTMapper(unittest.TestCase):
    """测试AST映射"""
    
    def test_map_function(self):
        source_ast = ASTNode("FunctionDef")
        source_ast.metadata["name"] = "hello"
        
        mapper = ASTMapper("python", "javascript")
        target_ast = mapper.map(source_ast)
        
        self.assertEqual(target_ast.node_type, "FunctionDeclaration")
    
    def test_map_class(self):
        source_ast = ASTNode("ClassDef")
        source_ast.metadata["name"] = "MyClass"
        
        mapper = ASTMapper("python", "javascript")
        target_ast = mapper.map(source_ast)
        
        self.assertEqual(target_ast.node_type, "ClassDeclaration")


class TestCodeGenerator(unittest.TestCase):
    """测试代码生成器"""
    
    def test_python_generator(self):
        ast = ASTNode("Program")
        func = ASTNode("FunctionDeclaration")
        func.metadata["name"] = "add"
        func.metadata["params"] = ["a", "b"]
        ast.children = [func]
        
        generator = PythonCodeGenerator()
        code = generator.generate(ast)
        
        self.assertIn("def add", code)
    
    def test_javascript_generator(self):
        ast = ASTNode("Program")
        func = ASTNode("FunctionDeclaration")
        func.metadata["name"] = "add"
        func.metadata["params"] = ["a", "b"]
        ast.children = [func]
        
        generator = JavaScriptCodeGenerator()
        code = generator.generate(ast)
        
        self.assertIn("function add", code)


class TestCodeTranslator(unittest.TestCase):
    """测试完整转译"""
    
    def test_translate_python_to_javascript(self):
        source = "def add(a, b):\n    return a + b"
        translator = CodeTranslator("python", "javascript")
        result = translator.translate(source)
        
        self.assertIn("function add", result)
    
    def test_translate_class(self):
        source = "class Calculator:\n    pass"
        translator = CodeTranslator("python", "javascript")
        result = translator.translate(source)
        
        self.assertIn("class Calculator", result)
    
    def test_translate_python_to_python(self):
        source = "def hello():\n    pass"
        translator = CodeTranslator("python", "python")
        result = translator.translate(source)
        
        self.assertIn("def hello", result)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_complete_pipeline(self):
        source = """def calculate(x, y):
    return x + y

class MathTools:
    def multiply(self, a, b):
        return a * b"""
        
        translator = CodeTranslator("python", "javascript")
        result = translator.translate(source)
        
        self.assertIn("function calculate", result)
        self.assertIn("class MathTools", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
