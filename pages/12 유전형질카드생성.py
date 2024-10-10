import streamlit as st
from openai import OpenAI

import requests

from io import BytesIO



# 가이드를 사이드바에서 입력 받기

st.sidebar.title("API 설정")

api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")



# Streamlit 페이지 제목 설정

st.title("가상의 사람 카드 만들기")

st.header("자기소개")



# 사용자 입력 받기

name = st.text_input("이름을 이니셜로 입력하세요. 예) J.Y.S.")

gender = st.radio("성별:", ('남자', '여자'))



# 유전자 관련 형질 입력 받기

eye_type = st.radio("눈 형질 (우성/열성):", ('쌍꺼풀', '외꺼풀'))

earlobe_type = st.radio("귀 형질 (우성/열성):", ('분리형', '부착형'))

forehead_type = st.radio("이마선 형질 (우성/열성):", ('V자형', 'M자형'))

hair_type = st.radio("머리카락 형질 (우성/열성):", ('곱슬형', '직모형'))

dimples = st.radio("보조개:", ('있다', '없다'))



generate_button = st.button("사람 카드 생성")



# API 키가 입력되었는지 확인

if api_key:

    # OpenAI 클라이언트 초기화

    client = OpenAI(api_key=api_key)



    if generate_button and all([name, gender, eye_type, earlobe_type, forehead_type, hair_type, dimples]):

        # 이미지 생성 프롬프트

        prompt = f"{gender} 아이의 중앙 일러스트레이션과 유전자 형질로는 눈({eye_type}), 귀({earlobe_type}), 이마선({forehead_type}), 머리카락({hair_type}), 보조개({dimples})을 포함한 극 사실주의 사진. 카드 하단에 '{name}'이라는 이름이 크게 표시됩니다."



        with st.spinner("사람 카드를 생성중입니다. 잠시만 기다려주세요..."):

            try:

                # OpenAI API를 사용하여 이미지 생성

                response = client.images.generate(

                    model="dall-e-3",

                    prompt=prompt,

                    size="1024x1792",

                    quality="standard",

                    n=1,

                )



                # 생성된 이미지 URL 가져오기

                image_url = response.data[0].url



                # 이미지 출력

                st.image(image_url, caption=f"{name}의 사람 카드")



                # 이미지 다운로드 준비

                response = requests.get(image_url)

                image_bytes = BytesIO(response.content)



                # 이미지 다운로드 버튼

                st.download_button(label="이미지 다운로드",

                                   data=image_bytes,

                                   file_name=f"{name}_tarot_card.jpg",

                                   mime="image/jpeg")

            except Exception as e:

                st.error("현재 사용 중인 키로 오류가 발생했습니다. " + str(e))

    else:

        st.warning("모든 필드를 채워주세요!")

else:

    st.error("API 키가 입력되지 않았습니다. API 키를 입력한 후 다시 시도하세요.")