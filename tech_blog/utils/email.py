from django.core.mail import EmailMessage


def register_email(email, name):
    subject = 'Tech_Blog'
    body = f'Hello {name} \n\n' \
        'Welcome to Tech_Blog.\n' \
        'Please feel free to contact us. \n\n'\
        'Thanks & Regards \n'\
        'techblog.application@gmail.com'
    email = EmailMessage(subject, body, to=[email])
    email.send()


def forgot_password_email(email, name, password):
    subject = 'Tech_Blog New Password'
    body = f'Hello {name} \n\n' \
           'Welcome to Tech_Blog.\n' \
           f'Your temporary password is {password} \n\n' \
           'Thanks & Regards \n' \
           'techblog.application@gmail.com'
    email = EmailMessage(subject, body, to=[email])
    email.send()

