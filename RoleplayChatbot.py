import openai  # OpenAI API를 사용하기 위한 라이브러리
from getpass import getpass  # 사용자 입력을 안전하게 받기 위한 라이브러리
import speech_recognition as sr  # 음성 인식을 위한 라이브러리
import pyttsx3  # 음성 출력 라이브러리 추가

# OpenAI API 키를 안전하게 입력받음 (콘솔에 입력 값이 표시되지 않음)
api_key = getpass('Enter your OpenAI API key: ')
openai.api_key = api_key  # OpenAI API에 키 설정

# 음성 인식기를 초기화
recognizer = sr.Recognizer()

def listen_and_transcribe():
    """마이크로부터 음성을 듣고 텍스트로 변환하는 함수"""
    with sr.Microphone() as source:  # 마이크 사용
        print("Listening...")  # 사용자에게 듣고 있음을 알림
        audio_data = recognizer.listen(source)  # 마이크로부터 음성 데이터 받기
        print("Recognizing...")  # 인식 중임을 알림
        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')  # Google Speech-to-Text API를 사용하여 한국어로 변환
            print(f"Transcribed: {text}")  # 변환된 텍스트 출력
            return text  # 변환된 텍스트 반환
        except sr.UnknownValueError:  # 음성 인식 실패 시 예외 처리
            return "음성 인식에 실패했습니다."
        except sr.RequestError as e:  # API 요청 실패 시 예외 처리
            return f"음성 인식 서비스 요청에 실패했습니다: {e}"

def chat_with_gpt(scenario, user_input):
    """OpenAI ChatGPT 모델을 사용하여 대화를 생성하는 함수"""
    try:
        messages = [
            {"role": "system", "content": f"You are involved in a role-play scenario: {scenario}"},  # 시나리오 정보 제공
            {"role": "user", "content": user_input}  # 사용자 입력 전달
        ]
        
        response = openai.ChatCompletion.create(  # ChatGPT API 호출
            model="gpt-3.5-turbo",  # 사용할 모델 지정
            messages=messages,  # 대화 내용 전달
            max_tokens=150  # 생성할 최대 토큰 수 제한
        )
        return response.choices[0].message['content'].strip()  # ChatGPT 응답 반환 (공백 제거)
    except Exception as e:  # API 호출 실패 시 예외 처리
        return f"An error occurred: {e}"
    
def speak_text(text):
    """텍스트를 음성으로 출력하는 함수"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 말하기 속도 조절 (기본값: 200)
    engine.setProperty('voice', 'korean') # 한국어 음성 설정
    engine.say(text)
    engine.runAndWait()
    
def start_role_play():
    """상황극을 시작하고 진행하는 함수"""
    scenario = input("상황극을 시작할 시나리오를 입력해주세요: ")  # 사용자로부터 시나리오 입력 받기
    print("상황극이 시작되었습니다. '종료'를 입력하면 상황극을 종료합니다.")
    
    while True:  # 상황극 종료 시까지 반복
        user_input = listen_and_transcribe()  # 음성 입력 받아 텍스트로 변환
        if user_input.lower() == "종료":  # 사용자가 '종료' 입력 시 종료
            print("상황극을 종료합니다.")
            break

        if user_input == "음성 인식에 실패했습니다." or user_input.startswith("음성 인식 서비스 요청에 실패했습니다:"):  # 음성 인식 실패 시 예외 처리
            print(user_input)
            continue
        
        # ChatGPT 응답 받아 출력
        gpt_response = chat_with_gpt(scenario, user_input)
        print(f"ChatGPT: {gpt_response}")
        speak_text(gpt_response)  
        
# 상황극 시작 함수 호출
start_role_play()
