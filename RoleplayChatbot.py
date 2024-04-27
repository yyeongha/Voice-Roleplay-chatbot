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
    # 사용자의 입력이 시나리오의 키워드를 포함하고 있는지 확인
    if scenario.lower() not in user_input.lower():
        # 맥락에 맞지 않는 입력에 대해 적절한 응답을 제안합니다.
        prompt = f"주어진 시나리오 '{scenario}'에 대해 사용자가 '{user_input}'라고 하였습니다. 이는 문맥에 맞지 않습니다. 문맥에 맞는 적절한 반응을 제안해 주세요."
        correction_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        corrected_text = correction_response.choices[0].text.strip()
        return False, f"입력하신 내용이 시나리오와 맞지 않습니다. 아마 이렇게 말씀하시려는 것이었나요: '{corrected_text}'"
    return True, user_input


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
