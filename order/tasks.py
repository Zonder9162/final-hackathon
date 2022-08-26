# from config.celery import app
# from django.core.mail import send_mail

# @app.task
# def order_created(order_id):
#     """
#     Task to send e-mail notification when an order is successfully created.
#     """
#     order = .objects.get(id=order_id)
#     subject = 'Order nr. {}'.format(order.id)
#     message = 'You have successfully placed an order.\
#                 Your order id is {}.'.format(order.id)
#     mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
#     return mail_sent