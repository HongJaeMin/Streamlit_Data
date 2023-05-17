import openai
import streamlit as st
from streamlit_chat import message
 

openai.api_key = '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'
 

## OpenAI API로 프롬프트를 받아들이고 응답을 생성한다.
def generate_response(prompt):
    completions = openai.Completion.create( # starting prompt를 제공하여 텍스트를 생성할 수 있음
        engine='text-davinci-003', # 사용할 엔진
        prompt=prompt, # 텍스트를 생성할 프롬프트
        max_tokens=1024, # 최대 토큰 수 
        stop=None, # 텍스트 생성을 중단할 문자열을 지정
        temperature=0, # 생성된 텍스트의 무작위성을 제어
        top_p=1, # ???
    )
    message = completions['choices'][0]['text'].replace('\n', '')
    return message


## 세션 상태로, 첫번째로 실행할 때 시작 메세지를 제공하여 챗봇을 초기화한다.
st.header('공공데이터 Chatbot') 
if 'generated' not in st.session_state: # 봇의 응답
    st.session_state['generated'] = []
if 'past' not in st.session_state: # 사용자의 입력
    st.session_state['past'] = []


with st.form('form', clear_on_submit=True): # https://docs.streamlit.io/library/api-reference/control-flow/st.form
    user_input = st.text_input('You: ', '', key='input') # 사용자가 입력한 텍스트를 제공받고,
    submitted = st.form_submit_button('Send') # st.form_submit_button으로 보낸다.
 

## user_input이 안 비어있으면, generate_response 함수로 응답을 생성하고, output에 저장한다.
if submitted and user_input:
    output = generate_response(user_input) # user_input이 안 비어있으면 generate_response 함수로 응답을 생성하고, output에 저장한다.
    st.session_state.past.append(user_input) # 사용자의 입력을 past에 추가하고,
    st.session_state.generated.append(output) # 봇의 응답을 generated에 추가하여 채팅 기록을 추적한다.
 

## 마지막으로 past/generated 목록을 반복하고
## streamlit_chat 라이브러리의 message로 각 메세지를 표시함으로써 채팅 기록을 표시한다. 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1): # -1, -1, -1 ???
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state['generated'][i], key=str(i))