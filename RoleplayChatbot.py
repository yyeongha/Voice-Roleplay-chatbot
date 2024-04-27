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

def check_context(scenario, response):
    # 간단한 문맥 분석 로직
    # 여기서는 시나리오 키워드를 포함하는지 검사합니다.
    if scenario.lower() not in response.lower():
        return f"입력이 주어진 상황극 시나리오와 맞지 않습니다. {scenario}에 대한 내용을 포함해주세요."
    return response

def start_role_play():
    scenario = input("상황극을 시작할 시나리오를 입력해주세요: ")
    print("상황극이 시작되었습니다. 'exit'를 입력하면 상황극을 종료합니다.")
    
    while True:
        user_input = listen_and_transcribe()
        if user_input.lower() == "exit":
            print("Ending the role-play.")
            break

        if user_input == "음성 인식에 실패했습니다." or user_input.startswith("음성 인식 서비스 요청에 실패했습니다:"):
            print(user_input)
            continue
        
        gpt_response = chat_with_gpt(scenario, user_input)
        context_checked_response = check_context(scenario, gpt_response)
        print(f"ChatGPT: {context_checked_response}")

# 상황극 시작
start_role_play()
