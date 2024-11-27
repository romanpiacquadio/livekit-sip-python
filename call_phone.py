from flask import Flask, render_template, request
from livekit import api
import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Ensure these environment variables are set
LIVEKIT_URL = os.getenv('LIVEKIT_URL')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')
SIP_TRUNK_ID = os.getenv('SIP_TRUNK_ID')

async def create_sip_participant(phone_number):
    logging.info(f"Attempting to create SIP participant for {phone_number}")
    logging.info(f"LIVEKIT_URL: {LIVEKIT_URL}")
    logging.info(f"LIVEKIT_API_KEY: {LIVEKIT_API_KEY}")
    logging.info(f"LIVEKIT_API_SECRET: {LIVEKIT_API_SECRET}")
    logging.info(f"SIP_TRUNK_ID: {SIP_TRUNK_ID}")
    livekit_api = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    sip_trunk_id = SIP_TRUNK_ID
    
    try:
        response = await livekit_api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                sip_trunk_id=sip_trunk_id,
                sip_call_to=phone_number,
                room_name=f"{phone_number}_{int(asyncio.get_event_loop().time())}",
                participant_identity=f"sip_{phone_number}",
                participant_name="SIP Caller"
            )
        )
        logging.info(f"SIP participant created successfully: {response}")
        await livekit_api.aclose()
        return f"Call initiated to {phone_number}"
    except Exception as e:
        logging.error(f"Error creating SIP participant: {str(e)}")
        logging.error(f"Error type: {type(e).__name__}")
        logging.error(f"Error details: {e.__dict__}")
        await livekit_api.aclose()
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        logging.info(f"Received phone number: {phone_number}")
        return asyncio.run(create_sip_participant(phone_number))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)