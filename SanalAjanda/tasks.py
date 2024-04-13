from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Tasks, CustomUser
from django.conf import settings

def send_tomorrows_notes(request):

    tomorrow = datetime.now() + timedelta(days=1)
    users = CustomUser.objects.all()

    subject = f"Yarının Notları - {tomorrow.strftime('%d/%m/%Y')}"
    for user in users:
        tomorrow_notes = Tasks.objects.filter(user=request.user, tarih=tomorrow)
        message = "\n".join([note.not_metni for note in tomorrow_notes])
        user_email = request.user.email

        if CustomUser.automatic_notifications:
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[user_email], fail_silently=False)


if __name__ == "__main__":
    send_tomorrows_notes()