import openai
from getpass import getpass
import speech_recognition as sr

# OpenAI API 키를 안전하게 입력받습니다.
api_key = getpass('Enter your OpenAI API key: ')
openai.api_key = api_key

# 음성 인식기를 초기화합니다.
recognizer = sr.Recognizer()

def listen_and_transcribe():
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)
        print("Recognizing...")
        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            return "음성 인식에 실패했습니다."
        except sr.RequestError as e:
            return f"음성 인식 서비스 요청에 실패했습니다: {e}"

def chat_with_gpt(scenario, user_input):
    try:
        messages = [
            {"role": "system", "content": f"You are involved in a role-play scenario: {scenario}"},
            {"role": "user", "content": user_input}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message['content'].strip() 
    except Exception as e:
        return f"An error occurred: {e}"

def check_context(scenario, user_input):
    # GPT 모델을 이용해 입력과 시나리오의 맥락적 일치성을 분석합니다 (한국어로 질의).
    context_prompt = f"주어진 시나리오: '{scenario}'에 대해 사용자가 입력한 내용: '{user_input}'. 이 입력이 시나리오의 문맥에 맞습니까? 맞지 않다면, 문맥에 적절한 반응을 제안해 주세요."
    
    context_check = openai.Completion.create(
        model="text-davinci-002",
        prompt=context_prompt,
        max_tokens=250,
        temperature=0.5
    )
    context_response = context_check.choices[0].text.strip()

    # 맥락 분석 결과를 한국어로 제공합니다.
    if "맞지 않다면" in context_response:
        return False, context_response
    return True, user_input

def start_role_play():
    scenario = input("상황극을 시작할 시나리오를 입력해주세요: ")
    print("상황극이 시작되었습니다. '종료'를 입력하면 상황극을 종료합니다.")
    
    while True:
        user_input = listen_and_transcribe()
        if user_input.lower() == "종료":
            print("상황극을 종료합니다.")
            break

        if user_input == "음성 인식에 실패했습니다." or user_input.startswith("음성 인식 서비스 요청에 실패했습니다:"):
            print(user_input)
            continue
        
        # GPT로부터 받은 응답을 맥락 분석
        gpt_response = chat_with_gpt(scenario, user_input)
        context_valid, context_checked_response = check_context(scenario, gpt_response)

        if context_valid:
            print(f"ChatGPT: {context_checked_response}")
        else:
            print(f"ChatGPT 제안: {context_checked_response}")

# 상황극 시작
start_role_play()
