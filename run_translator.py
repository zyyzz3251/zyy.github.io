#!/usr/bin/env python3
"""
代码互译系统 - 命令行演示
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from code_translator.core import CodeTranslator, Lexer, SimplePythonParser, ASTMapper


def main():
    print("\n" + "="*70)
    print("  🔄 代码互译系统 - 命令行演示")
    print("="*70)
    
    source_code = """def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y"""
    
    print("\n📝 源代码 (Python):")
    print("-" * 70)
    print(source_code)
    
    print("\n" + "="*70)
    print("步骤1️⃣: 词法分析 (Lexical Analysis)")
    print("="*70)
    
    lexer = Lexer("python")
    tokens = lexer.tokenize(source_code)
    print(f"✅ 生成了 {len([t for t in tokens if t.type.value != 'EOF'])} 个记号")
    print("前8个记号:")
    for i, token in enumerate(tokens[:8]):
        print(f"  {i+1}. {token}")
    
    print("\n" + "="*70)
    print("步骤2️⃣: 语法分析 (Syntax Analysis)")
    print("="*70)
    
    parser = SimplePythonParser(tokens)
    source_ast = parser.parse()
    print(f"✅ AST 根节点: {source_ast.node_type}")
    print(f"✅ 子节点数: {len(source_ast.children)}")
    for i, child in enumerate(source_ast.children):
        print(f"  {i+1}. {child.node_type}", end="")
        if "name" in child.metadata:
            print(f" (名称: {child.metadata['name']})", end="")
        print()
    
    print("\n" + "="*70)
    print("步骤3️⃣: AST 映射 (AST Mapping)")
    print("="*70)
    
    mapper = ASTMapper("python", "javascript")
    target_ast = mapper.map(source_ast)
    print(f"✅ 目标AST 根节点: {target_ast.node_type}")
    print("✅ 映射后的节点类型:")
    for i, child in enumerate(target_ast.children):
        print(f"  {i+1}. {child.node_type}")
    
    print("\n" + "="*70)
    print("步骤4️⃣: 代码生成 (Code Generation)")
    print("="*70)
    
    translator = CodeTranslator("python", "javascript")
    result = translator.translate(source_code)
    
    print("\n📝 目标代码 (JavaScript):")
    print("-" * 70)
    print(result)
    
    print("\n" + "="*70)
    print("✅ 转译完成!")
    print("="*70)


if __name__ == "__main__":
    main()
