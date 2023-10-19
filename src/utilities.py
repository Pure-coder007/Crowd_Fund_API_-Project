import random
from .models import User, get_user_by_id
from flask_mail import Mail, Message

import random
from flask_mail import Mail, Message

mail = Mail()

def send_otp(app, email, otp):
    with app.app_context():
        msg = Message('Verification Token', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your verification token is {otp}'
        mail.send(msg)


def approved_mail(email):
    msg = Message(' Congratulations your request has been approved, you can now receive donations', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Congratulations your request has been approved, you can now receive donations 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    mail.send(msg)

def send_mail(email):
    msg = Message('Verification Email', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You just successfully registered on speedyhelp as a donator. Thank you 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    mail.send(msg)

def approved_mail_donators(email):
    msg = Message('Thank you for your donations ❤❤❤', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Thank you for your donations on speedyhelp ❤❤❤'
    mail.send(msg)


def received(email):
    msg = Message('You have just received an anonymous donation', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    mail.send(msg)

def received_admin(username):
    msg = Message(f'{username} received an anonymous donation', sender='Anonymous@gmail.com', recipients=['admin@gmail.com'])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    mail.send(msg)
