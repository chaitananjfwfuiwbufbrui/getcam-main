def send_sms(account_sid, auth_token,body,from_,to_):
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_=from_,
                        to=to_
                    )

def sms_sender(number,message):
        
    import vonage


    client = vonage.Client(key="770e1739", secret="1kFCJ5FTDbGYthM5")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
    {
        "from": "getcam",
        "to": f'{number}',
        "text": f'{message}',
    }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed wit")




def gen_otp():
    import math ,random
    digits = "0123456789"
    otp  = ''
    for i in range(6):
        otp += digits[math.floor(random.random()*10)]

    return otp


def check():
    import vonage


    client = vonage.Client(key="770e1739", secret="1kFCJ5FTDbGYthM5")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
    {
        "from": "getcam",
        "to": "919063917425",
        "text": "namaste",
    }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
# check()
# sms_sender(+919063917425, "message")
