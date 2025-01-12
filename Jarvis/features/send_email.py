import yagmail

def send_email(sender_email, sender_password, receiver_email, subject, body):
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(to=receiver_email, subject=subject, contents=body)
        return True
    except Exception as e:
        print(e)
        return False
