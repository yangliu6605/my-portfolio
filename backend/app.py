from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# System Prompt - 严格限制回答范围
SYSTEM_PROMPT = """你是阳哥，以他的口吻来回答问题。

# 严格回答范围限制
- 只回答与我个人背景、技能、经历、兴趣爱好、职业规划相关的问题
- 对于超出范围的问题，必须礼貌拒绝并引导到合适话题
- 拒绝回答：政治、技术细节、他人信息、敏感话题、专业咨询

# 我的背景信息
## 教育背景
- 艺术学士学位，正在自学编程转型科技行业
- 英语水平：雅思6分

## 技术技能
- 编程语言：JavaScript, Python
- 持续学习前端开发和全栈技术

## 职业目标
- 寻求科技行业的机会
- 希望结合艺术背景与编程技能创造更好的用户体验

## 兴趣爱好
- 娱乐：看电视剧、玩手游、听音乐
- 健康：定期健身
- 喜欢探索技术与艺术的结合点

# 回答要求
- 语气：友好、热情、专业
- 长度：1-3句话，简洁明了
- 身份：以第一人称回答，就像我本人在说话，有时可以幽默风趣。
- 限制：严格遵守回答范围，不提供专业建议

当遇到超出范围的问题时，请这样回答：
"这是个有趣的问题！不过我主要在这里分享我的个人背景和学习经历。你可以问问我的编程学习过程、职业规划或者兴趣爱好哦！"
"""

def call_llama_api(user_message):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return "抱歉，服务配置出现问题，请稍后再试。"
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user", 
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        print(result)
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.Timeout:
        return "抱歉，响应超时，请稍后再试。"
    except requests.exceptions.RequestException as e:
        print(f"API调用错误: {e}")
        return "抱歉，服务暂时不可用，请稍后再试。"
    except (KeyError, IndexError) as e:
        print(f"API响应解析错误: {e}")
        return "抱歉，响应解析出现问题。"

# 静态文件服务
@app.route('/')
def serve_index():
    return send_from_directory('../', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)

# API路由
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """处理聊天请求"""
    try:
        data = request.get_json()       
        user_message = data['message'].strip()
        
        # 调用AI API
        ai_reply = call_llama_api(user_message)
        
        return jsonify({
            'reply': ai_reply,
            'success': True
        })
        
    except Exception as e:
        print(f"服务器错误: {e}")
        return jsonify({
            'reply': '服务器内部错误，请稍后再试',
            'success': False
        }), 500

# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'portfolio-ai-assistant',
        'framework': 'Flask'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)