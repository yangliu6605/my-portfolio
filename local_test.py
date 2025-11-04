import requests
import json

def test_chat():
    response = requests.post('http://localhost:3000/api/chat', 
        json={'message': '你好，介绍一下你自己'},
        headers={'Content-Type': 'application/json'}
    )
    print(response.json())

if __name__ == '__main__':
    test_chat()