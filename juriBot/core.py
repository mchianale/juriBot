from mistralai import Mistral
# tools
from juriBot.tools import queryInformationsBySimilarity
# other
from fastapi import HTTPException
import logging
import functools
import json

logging.basicConfig(level=logging.INFO)
       

class JuriBot:
    def __init__(self, mistral_model : str, api_key : str, n_results : int = 5):
        self.mistral_client = Mistral(api_key=api_key)
        self.mistral_model = mistral_model

        # system prompt
        system_prompt_file = open('juriBot/system_prompt.txt', 'r')
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_file.read()
        }
        system_prompt_file.close()

        # tools
        self.tools = json.load(open('juriBot/tools.json', encoding='utf-8'))['tools']
        self.names_to_functions = {
            'queryInformationsBySimilarity': functools.partial(queryInformationsBySimilarity, n_results=n_results)
        }
        self.tool_choice = 'any'


    
    def chat(self, user_query : str, history_messages : list):
        # current messages
        messages = [self.system_prompt] + history_messages + [{"role" : "user", "content" :  user_query}]
        check_points = -1
        # called the llm
        try:
            chat_response = self.mistral_client.chat.complete(
                model = self.mistral_model,
                messages = messages,
                tools=self.tools,
                tool_choice=self.tool_choice
            )
 
            # if the juriBot called a tool
            if chat_response.choices[0].message.tool_calls:
                # udpate messages
                messages.append(chat_response.choices[0].message)
                # run the tool
                tool_call = chat_response.choices[0].message.tool_calls[0]
                function_name = tool_call.function.name
                function_params = json.loads(tool_call.function.arguments)
                function_result = self.names_to_functions[function_name](**function_params)
              
                # add to messages
                messages.append({"role":"tool", "content": str(function_result), "tool_call_id": tool_call.id})   
                
                #update checkpoints 
                check_points -= 2
                # recall the llm
                try:
                    chat_response = self.mistral_client.chat.complete(
                        model = self.mistral_model,
                        messages = messages
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

            messages.append({"role":"assistant", "content": chat_response.choices[0].message.content})
            check_points -= 1
            return messages[check_points:]
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    """async def stream(self, user_query: str, history_messages: list):
        # Current messages
        messages = [self.system_prompt] + history_messages + [{"role": "user", "content": user_query}]

        try:
            
            # Call the LLM in streaming mode
            chat_response = self.mistral_client.chat.stream(
                model=self.mistral_model,
                messages=messages,
                tools=self.tools,
                tool_choice="none",
            )
            logging.info(f'before chat_response: {chat_response}')
            # Process streamed chunks from the LLM
            content = ""
            for chunk in chat_response:
                if not chunk.data.choices[0].finish_reason == 'tool_calls':
                    content += chunk.data.choices[0].delta.content
                    yield chunk.data.choices[0].delta.content
                else:
                    break
            if not content:
                messages.append(chunk.data.choices[0].message)
                # run the tool
                tool_call = chunk.data.choices[0].message.tool_calls[0]
                function_name = tool_call.function.name
                function_params = json.loads(tool_call.function.arguments)
                function_result = self.names_to_functions[function_name](**function_params)
              
                # add to messages
                messages.append({"role":"tool", "name":function_name, "content": str(function_result), "tool_call_id": tool_call.id})
                # recall the llm
                try:
                    chat_response = self.mistral_client.chat.complete(
                        model = self.mistral_model,
                        messages = messages
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")"""

      