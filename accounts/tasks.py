# from config.celery import app
# from django.core.mail import send_mail


# @app.task
# def send_activation_code(self):
#         from django.core.mail import send_mail
#         self.generate_activation_code()
#         activation_url = f'https://toys-backend2022.herokuapp.com/account/activate/{self.activation_code}/'
#         message = f'Activate your account, following this link {activation_url}'
#         send_mail("Activate account", message, "toys@gmail.com", [self.email])
