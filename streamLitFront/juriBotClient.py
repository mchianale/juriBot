import requests

class JuriBotClient:
    def __init__(self, chat_url : str):
        self.chat_url = chat_url
    
    def call_chat(self, user_query : str, history_messages : list):
        """try:
            response = requests.get(self.chat_url, json={"user_query" : user_query, "history_messages" : history_messages})
            if response.status_code
            return {"status_code" : 200, "response" : response.json()}
        except Exception as e:
            return {"status_code" : 500, "error" : e}"""
        
        response = requests.get(self.chat_url, json={"user_query" : user_query, "history_messages" : history_messages})
        if response.status_code == 200:
            return {"status_code" : 200, "response" : response.json()}
        return {"status_code" : response.status_code, "error" : response.json()['detail']}


