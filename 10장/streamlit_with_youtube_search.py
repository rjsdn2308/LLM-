import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from datetime import datetime
import pytz

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from youtube_search import YoutubeSearch
from langchain_community.document_loaders import YoutubeLoader
from typing import List

from dotenv import load_dotenv
import os
load_dotenv()


# 모델 초기화
llm = ChatOpenAI(model="gpt-4o-mini")

# 도구 함수 정의
@tool
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수."""
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        result = f'{timezone} ({location}) 현재시각 {now}'
        print(result)
        return result
    except pytz.UnknownTimeZoneError:
        return f"알 수 없는 타임존: {timezone}"
    

@tool
def get_web_search(query: str, search_period: str) -> str:
    """
    웹 검색을 수행하는 함수.
    """
    # 🔥 FIX 1: region 및 time 옵션 안정화
    wrapper = DuckDuckGoSearchAPIWrapper(region="ko-kr", time=search_period)

    print('-------- WEB SEARCH --------')
    print(query)
    print(search_period)

    search = DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        results_separator=';\n'
    )

    docs = search.invoke(query)
    return docs


@tool
def get_youtube_search(query: str) -> List:
    """
    유튜브 검색을 한 뒤, 영상들의 내용을 반환하는 함수.
    """
    print('-------- YOUTUBE SEARCH --------')
    print(query)

    videos = YoutubeSearch(query, max_results=5).to_dict()

    # 1시간 이상의 영상은 스킵 (59:59가 최대 길이)
    videos = [video for video in videos if len(video['duration']) <= 5]

    for video in videos:
        video_url = 'http://youtube.com' + video['url_suffix']

        # 🔥 FIX 2: YoutubeLoader 최신 버전 대응
        loader = YoutubeLoader.from_youtube_url(
            video_url,
            add_video_info=True
        )

        video['video_url'] = video_url
        video['content'] = loader.load()

    return videos


# 도구 바인딩
tools = [get_current_time, get_web_search, get_youtube_search]
tool_dict = {
    "get_current_time": get_current_time, 
    "get_web_search": get_web_search,
    "get_youtube_search": get_youtube_search
}

llm_with_tools = llm.bind_tools(tools)


# 사용자의 메시지 처리하기 위한 함수
def get_ai_response(messages):
    response = llm_with_tools.stream(messages)
    
    gathered = None
    for chunk in response:
        yield chunk
        
        if gathered is None:
            gathered = chunk
        else:
            gathered += chunk
 
    # tool call 처리
    if gathered.tool_calls:
        st.session_state.messages.append(gathered)
        
        for tool_call in gathered.tool_calls:
            selected_tool = tool_dict[tool_call['name']]

            # 🔥 FIX 3: invoke()에 dict 형태로 전달
            tool_msg = selected_tool.invoke(tool_call['args'])

            print(tool_msg, type(tool_msg))
            st.session_state.messages.append(ToolMessage(content=str(tool_msg), name=tool_call['name']))
           
        for chunk in get_ai_response(st.session_state.messages):
            yield chunk


# Streamlit 앱
st.title("💬 GPT-4o Langchain Chat")

# 스트림릿 session_state에 메시지 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage("너는 사용자를 돕기 위해 최선을 다하는 인공지능 봇이다."),
        AIMessage("How can I help you?")
    ]

# 스트림릿 화면에 메시지 출력
for msg in st.session_state.messages:
    if msg.content:
        if isinstance(msg, SystemMessage):
            st.chat_message("system").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, ToolMessage):
            st.chat_message("tool").write(msg.content)


# 사용자 입력 처리
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(prompt))

    response_stream = get_ai_response(st.session_state["messages"])

    # 🔥 FIX 4: write_stream 반환값(None) 저장하지 않도록 변경
    final_text = st.chat_message("assistant").write_stream(response_stream)

    # write_stream은 None을 반환하므로, gathered된 마지막 메시지를 메시지로 저장
    st.session_state["messages"].append(AIMessage(final_text if final_text else ""))
