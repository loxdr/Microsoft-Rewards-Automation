import smtplib

def send_email(body, subject, email, password):
    def sende():
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email, password)
            mes = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(email, email, mes)
    sent = False 
    while sent == False:
        try:
            sende()
            sent = True
        except:
            continue