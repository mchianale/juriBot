import streamlit as st
from juriBotClient import JuriBotClient
import ast

# app config
juriBot = JuriBotClient(chat_url="http://localhost:8002/chat")
st.set_page_config(page_title="juriBot", page_icon="🤖")
st.title("juriBot")
st.caption("🚀 Un chatbot spécialisé dans l'interprétation et l'explication des textes juridiques en vigueur relatifs au Code de l'Éducation, propulsé par Mistral AI.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Bonjour, je suis Juribot, un agent conversationnel spécialisé dans le domaine du droit relatifs au Code de l'Éducation, propulsé par l'intelligence artificielle de Mistral. Saisissez votre question juridique ci-dessous, et voyons ensemble si je peux vous apporter une réponse pertinente."}]

for msg in st.session_state.messages:
    if msg["role"] in ['user', 'assistant'] and msg["content"] != "":
        st.chat_message(msg["role"]).write(msg["content"])
    if msg["role"] == "tool":
        documents =  ast.literal_eval(msg["content"])
        for document in documents:
            content = ':'.join(document['document'].split(':')[-1:])
            st.chat_message('⚖️').write(f"**{document['metadata']['id']}**:\n{content}")

if prompt := st.chat_input():
    # write the prompt
    st.chat_message("user").write(prompt)
    response = juriBot.call_chat(
                user_query=prompt,
                history_messages=st.session_state.messages
        )
    
    if response["status_code"] == 200:
        response = response["response"]
        st.session_state.messages += response
    
        for message in response:
            if message["role"] == "tool":
                documents =  ast.literal_eval(message["content"])
                for document in documents:
                    content = ':'.join(document['document'].split(':')[-1:])
                    st.chat_message('⚖️').write(f"**{document['metadata']['id']}**:\n{content}")
                                                
        st.chat_message("assistant").write(st.session_state.messages[-1]['content'])
    else:
        st.error(response["error"], icon="🚨")
    