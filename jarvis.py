import speech_recognition as sr
import openai

from elevenlabslib import *

openai.api_key = 'YOUR KEY HERE'

elevenLabsAPIKey = 'YOUR KEY HERE'

r = sr.Recognizer()
mic = sr.Microphone()
user = ElevenLabsUser(elevenLabsAPIKey)

voice = user.get_voices_by_name("Jarvis")[0]

conversation = [
        {"role": "system", "content": "Your name is Jarvis and your purpose is to be Adam's AI assistant"},
    ]


while True:
    with mic as source:
        r.adjust_for_ambient_noise(source) #Can set the duration with duration keyword
        print("talk")
        audio = r.listen(source)

    word = r.recognize_google(audio)

    if "draw" in word:
        i = word.find("draw")
        i += 5
        response = openai.Image.create(
            prompt=word[i:],
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        print(word[i:])
        print(image_url)

    else:
        conversation.append({"role": "user", "content": word})

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
        )

        message = response["choices"][0]["message"]["content"]
        conversation.append({"role": "assistant", "content": message})
        # print(message)
        voice.generate_and_play_audio(message, playInBackground=False)
