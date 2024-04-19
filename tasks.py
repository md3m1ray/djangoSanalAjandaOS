import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoSanalAjanda.settings'
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.db import connection
from SanalAjanda.models import Tasks, CustomUser


def send_tomorrows_notes():
    tomorrow = datetime.now() + timedelta(days=1)
    subject = f"Yarının Notları - {tomorrow.strftime('%d/%m/%Y')}"

    with connection.cursor() as cursor:
        cursor.execute('SELECT email FROM "SanalAjanda_customuser" WHERE automatic_notifications = TRUE')
        rows = cursor.fetchall()
        for row in rows:
            user_email = row[0]
            user = CustomUser.objects.get(email=user_email)
            tomorrow_notes = Tasks.objects.filter(user_id=user.id, tarih=tomorrow)
            notlar = "\n".join([note.not_metni for note in tomorrow_notes])

            if tomorrow_notes:
                message = (f"Seçili Tarih: {tomorrow.strftime('%d/%m/%Y')}\nNotlar:\n{notlar}\n\nBu eposta otomatik olarak gönderilmiştir.\n"
                           f"Eposta almak istemiyorsanız bildirim seçeneğini kapatabilirsiniz.\n"
                           f"Saygılarımızla.\nsanalajanda.com")
            else:
                message = ("Yarın İçin Notunuz Bulunmamaktadır.\nBu eposta otomatik olarak gönderilmiştir.\n"
                           f"Eposta almak istemiyorsanız bildirim seçeneğini kapatabilirsiniz.\n"
                           f"Saygılarımızla.\nsanalajanda.com")

            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[user_email], fail_silently=False)


if __name__ == "__main__":
    send_tomorrows_notes()
