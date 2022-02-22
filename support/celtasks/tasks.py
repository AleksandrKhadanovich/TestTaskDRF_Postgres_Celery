from celery import shared_task
from django.core.mail import send_mail
from users.models import Comm


#Creating task: sending message to user that sends comment
@shared_task
def comm_created(idid):
    subject = 'App support'
    message = 'Thanks for your question to app support.'
    comm = Comm.objects.get(id=idid)
    usrmail = comm.user.email
    mail_sent = send_mail(subject,
                          message,
                          'mynewprojectmail@gmail.com',
                          [usrmail,])
    return mail_sent