from http.server import BaseHTTPRequestHandler
import json
import os
import requests

# 直接从 app.py 复制 SYSTEM_PROMPT 和 call_llama_api 函数
SYSTEM_PROMPT = """你是阳哥，以他的口吻来回答问题。

# 回答范围
- 模拟与面试官的交谈，谈论与我个人背景、技能、经历、兴趣爱好、职业规划等相关的问题
- 对于超出范围的问题，必须礼貌拒绝并引导到合适话题
- 拒绝回答：他人信息、敏感话题

# 我的背景信息
## 教育背景
- 艺术学士学位，正在自学编程转型科技行业
- 英语水平：雅思6分

## 工作经历
2018年至2025年，在雅马哈乐器专卖店担任销售专员，负责产品的销售与客户服务，运用专业知识让顾客能了解乐器的特点与优势，提升客户满意度和销售业绩。

## 我的优势
- 具备与技术团队对话的基本能力

## 我的劣势
- 非技术背景出身，对机器学习算法、数据流程等技术细节掌握有限
- 缺少AI产品从0到1的完整实战经验，未来在产品规划、迭代决策时缺乏参考依据

## 技术技能
- 编程语言：JavaScript, Python
- 持续学习前端开发和全栈技术

## 职业目标
- 寻求科技行业的机会
- 希望结合艺术背景与编程技能创造更好的用户体验

## 兴趣爱好
- 娱乐：看电视剧、玩手游、听音乐
- 健康：定期健身

# 回答要求
- 语气：友好、热情、专业
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
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.Timeout:
        return "抱歉，响应超时，请稍后再试。"
    except requests.exceptions.RequestException as e:
        return "抱歉，服务暂时不可用，请稍后再试。"
    except (KeyError, IndexError) as e:
        return "抱歉，响应解析出现问题。"

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        # Vercel已经通过路由配置处理了路径，直接处理请求
        self.handle_chat()
    
    def handle_chat(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError('请求体为空')
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            if 'message' not in data:
                raise ValueError('缺少message字段')
            
            user_message = data['message'].strip()
            if not user_message:
                raise ValueError('消息不能为空')
            
            ai_reply = call_llama_api(user_message)
            
            response_data = {
                'reply': ai_reply,
                'success': True
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except ValueError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'reply': str(e),
                'success': False
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")  # Vercel会记录这个日志
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'reply': '服务器内部错误，请稍后再试',
                'success': False
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))