import smtplib
import math, random
import os

def _send_mail(to_address, msg):
    user = os.environ.get("GMAIL_USER", "facialvotingsystem@gmail.com")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        raise RuntimeError("GMAIL_APP_PASSWORD environment variable is not set")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(user, password)
    s.sendmail(user, to_address, msg)
    s.quit()

def mai(emails, Uniquepass):
    global mail
    mail = emails
    usermail = emails
    msg = Uniquepass
    _send_mail(usermail, msg)
    print("Sent successfully")

def otp(un, votev, email_ver):
    digits = "0123456789"
    OTP = "".join([digits[math.floor(random.random() * 10)] for _ in range(4)])
    print("This is OTP generated:", OTP)
    
    usermail = email_ver
    msg = OTP
    _send_mail(usermail, msg)
    print("Sent successfully")
    
    return OTP

def report(username, Userid, votecardnum, emailid, Consti):
    data = {
        "Name": username,
        "Userid": Userid,
        "Votercardno": votecardnum,
        "Constituency": Consti,
        "Status": "Vote casted"
    }
    Report = f"\nName: {data['Name']}\nUserid: {data['Userid']}\nVotercardno: {data['Votercardno']}\nConstituency: {data['Constituency']}\nStatus: {data['Status']}"
    usermail = emailid
    msg = Report
    print(msg)
    
    _send_mail(usermail, msg)
    print("Sent successfully")
