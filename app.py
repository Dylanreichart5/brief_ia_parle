import os
import azure.cognitiveservices.speech as speechsdk
import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
conversation_history = []
app.secret_key = "your-secret-key-here"
openai.api_key = os.getenv("OPENAI_API_KEY")
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_recognition_language="fr-FR"
speech_config.speech_synthesis_language = "fr-FR"

@app.route("/", methods=["GET", "POST"])
def index():
    conversation_history=[]

    if request.method == "POST":
        if request.form.get("microphone") == "on":
            return redirect(url_for("listen"))

    conversation_history = session["conversation_history"]

    return render_template("index.html", conversation_history=conversation_history)

@app.route("/listen")
# Define a conversation history data structure


@app.route("/listen")
def listen():
    # Use Azure Speech-to-Text to recognize speech from the microphone
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Say something...")
    result = speech_recognizer.recognize_once_async().get()
    question = result.text

    # Use OpenAI to generate an answer to the question
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.7,
        max_tokens=4000
    )
    answer = response.choices[0].text

    # Use Azure Text-to-Speech to synthesize speech from the answer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(answer).get()

    # Append the question-answer pair to the conversation history
    conversation_history.append({'question': question, 'answer': answer})

    # Pass the conversation history to the template
    return render_template("index.html", conversation_history=conversation_history)

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


