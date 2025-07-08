from flask import Flask, request
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.form.get("Body")
    response = MessagingResponse()
    msg = response.message()

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply_text = completion.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"Error: {str(e)}"

    msg.body(reply_text)
    return str(response)

app.run(host="0.0.0.0", port=5000)
