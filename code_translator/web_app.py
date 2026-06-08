"""
代码互译系统 - Web 服务
支持在浏览器中直接使用的完整 Web 应用
"""

from flask import Flask, render_template, request, jsonify
from code_translator.core import CodeTranslator, Lexer, SimplePythonParser, ASTMapper
import json
import traceback
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 翻译历史记录
translation_history = []


@app.route('/', methods=['GET'])
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def translate():
    """
    完整代码转译 API
    
    请求:
    {
        "source_code": "源代码",
        "source_lang": "python",
        "target_lang": "javascript"
    }
    
    返回:
    {
        "success": true,
        "target_code": "目标代码",
        "stats": {...},
        "tokens": [...],
        "ast": {...}
    }
    """
    try:
        data = request.get_json()
        source_code = data.get('source_code', '')
        source_lang = data.get('source_lang', 'python')
        target_lang = data.get('target_lang', 'javascript')
        
        if not source_code.strip():
            return jsonify({
                'success': False,
                'error': '源代码不能为空'
            }), 400
        
        # 创建转译器
        translator = CodeTranslator(source_lang, target_lang)
        
        # 词法分析
        lexer = Lexer(source_lang)
        tokens = lexer.tokenize(source_code)
        
        # 语法分析
        parser = SimplePythonParser(tokens)
        source_ast = parser.parse()
        
        # AST 映射
        mapper = ASTMapper(source_lang, target_lang)
        target_ast = mapper.map(source_ast)
        
        # 代码生成
        target_code = translator.translate(source_code)
        
        # 统计数据
        stats = {
            'source_lines': len(source_code.split('\n')),
            'target_lines': len(target_code.split('\n')),
            'token_count': len([t for t in tokens if t.type.value != 'EOF']),
            'ast_nodes': count_ast_nodes(source_ast),
            'timestamp': datetime.now().isoformat()
        }
        
        # 记录历史
        history_item = {
            'source_lang': source_lang,
            'target_lang': target_lang,
            'source_code': source_code[:100] + ('...' if len(source_code) > 100 else ''),
            'target_code': target_code[:100] + ('...' if len(target_code) > 100 else ''),
            'timestamp': stats['timestamp']
        }
        translation_history.append(history_item)
        if len(translation_history) > 50:
            translation_history.pop(0)
        
        return jsonify({
            'success': True,
            'target_code': target_code,
            'stats': stats,
            'tokens': [
                {
                    'type': t.type.value,
                    'value': t.value,
                    'line': t.line
                }
                for t in tokens if t.type.value != 'EOF'
            ],
            'ast': source_ast.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/lexical-analysis', methods=['POST'])
def lexical_analysis():
    """词法分析 API"""
    try:
        data = request.get_json()
        source_code = data.get('source_code', '')
        language = data.get('language', 'python')
        
        if not source_code.strip():
            return jsonify({'success': False, 'error': '代码不能为空'}), 400
        
        lexer = Lexer(language)
        tokens = lexer.tokenize(source_code)
        
        tokens_data = [
            {
                'type': t.type.value,
                'value': t.value,
                'line': t.line,
                'column': t.column
            }
            for t in tokens if t.type.value != 'EOF'
        ]
        
        return jsonify({
            'success': True,
            'tokens': tokens_data,
            'count': len(tokens_data),
            'stats': {
                'keywords': len([t for t in tokens_data if t['type'] == 'KEYWORD']),
                'identifiers': len([t for t in tokens_data if t['type'] == 'IDENTIFIER']),
                'operators': len([t for t in tokens_data if t['type'] == 'OPERATOR']),
                'literals': len([t for t in tokens_data if t['type'] == 'LITERAL']),
                'punctuation': len([t for t in tokens_data if t['type'] == 'PUNCTUATION'])
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/parse-ast', methods=['POST'])
def parse_ast():
    """语法分析 API"""
    try:
        data = request.get_json()
        source_code = data.get('source_code', '')
        language = data.get('language', 'python')
        
        if not source_code.strip():
            return jsonify({'success': False, 'error': '代码不能为空'}), 400
        
        lexer = Lexer(language)
        tokens = lexer.tokenize(source_code)
        parser = SimplePythonParser(tokens)
        ast = parser.parse()
        
        return jsonify({
            'success': True,
            'ast': ast.to_dict(),
            'node_count': count_ast_nodes(ast),
            'structure': get_ast_summary(ast)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/supported-languages', methods=['GET'])
def supported_languages():
    """获取支持的语言列表"""
    return jsonify({
        'source_languages': ['python', 'javascript', 'java'],
        'target_languages': ['python', 'javascript'],
        'pairs': [
            {'source': 'python', 'target': 'javascript', 'name': 'Python → JavaScript'},
            {'source': 'python', 'target': 'python', 'name': 'Python → Python'},
            {'source': 'javascript', 'target': 'python', 'name': 'JavaScript → Python'},
            {'source': 'javascript', 'target': 'javascript', 'name': 'JavaScript → JavaScript'},
        ]
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """获取转译历史"""
    return jsonify({
        'success': True,
        'history': translation_history[-20:],
        'total': len(translation_history)
    })


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """获取代码示例"""
    examples = {
        'python_function': {
            'name': '函数定义',
            'language': 'python',
            'code': '''def add(a, b):
    """计算两个数的和"""
    return a + b

result = add(1, 2)'''
        },
        'python_class': {
            'name': '类定义',
            'language': 'python',
            'code': '''class Calculator:
    """计算器类"""
    
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        self.result = a + b
        return self.result'''
        },
        'python_loop': {
            'name': '循环和条件',
            'language': 'python',
            'code': '''for i in range(10):
    if i % 2 == 0:
        print(f"偶数: {i}")
    else:
        print(f"奇数: {i}")'''
        },
        'javascript_function': {
            'name': 'JS 函数',
            'language': 'javascript',
            'code': '''function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let result = fibonacci(10);'''
        }
    }
    return jsonify({
        'success': True,
        'examples': examples
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取整体统计信息"""
    return jsonify({
        'success': True,
        'total_translations': len(translation_history),
        'supported_pairs': 4,
        'supported_languages': 3,
        'recent_translations': translation_history[-10:]
    })


@app.route('/api/batch-translate', methods=['POST'])
def batch_translate():
    """批量转译 API"""
    try:
        data = request.get_json()
        codes = data.get('codes', [])
        source_lang = data.get('source_lang', 'python')
        target_lang = data.get('target_lang', 'javascript')
        
        if not codes:
            return jsonify({'success': False, 'error': '未提供代码列表'}), 400
        
        results = []
        for code in codes:
            try:
                translator = CodeTranslator(source_lang, target_lang)
                result = translator.translate(code)
                results.append({
                    'success': True,
                    'target_code': result
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': len([r for r in results if r.get('success')])
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def count_ast_nodes(node):
    """计算 AST 节点数"""
    count = 1
    for child in node.children:
        count += count_ast_nodes(child)
    return count


def get_ast_summary(node, depth=0):
    """获取 AST 摘要"""
    summary = {
        'type': node.node_type,
        'depth': depth
    }
    
    if node.metadata:
        summary['metadata'] = node.metadata
    
    if node.children:
        summary['children'] = [get_ast_summary(child, depth + 1) for child in node.children]
    
    return summary


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': '资源不存在'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': '服务器错误'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
