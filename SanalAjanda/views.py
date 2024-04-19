from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Tasks
from .forms import UserProfileForm
from django.conf import settings
from django.contrib import messages
from .forms import NotificationPreferenceForm
from django.db.models import Q


def not_sil(request, not_id):
    if request.method == 'POST':
        not_obj = Tasks.objects.get(pk=not_id)
        not_obj.delete()

        return redirect("ana_sayfa")
    else:
        return render(request, 'ana_sayfa.html')


def cikis_yap(request):
    logout(request)
    return redirect('giris')


def kayit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Yeni kullanıcı oluştur
        user, created = CustomUser.objects.get_or_create(email=email)

        # Kullanıcı zaten varsa
        if not created:
            return render(request, 'kayit.html', {'error_message': 'Bu e-posta adresi zaten kayıtlı.'})

        # Parolayı ayarla ve kullanıcıyı oturum açtır
        user.set_password(password)
        user.save()
        return redirect('giris')
    return render(request, 'kayit.html')


def giris(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Kullanıcıyı doğrula
        user = authenticate(request, username=email, password=password)
        user2 = request.user
        if user is not None:
            # Kullanıcı doğrulandıysa oturum aç
            login(request, user)
            return redirect('ana_sayfa')
        if not user2.is_active:
            messages.error(request, "Üyeliğiniz henüz onaylanmamıştır. Lütfen daha sonra tekrar deneyin.")
            return render(request, 'registration/pending_approval.html')
        else:
            # Kullanıcı doğrulanamadıysa hata mesajı döndür
            return render(request, 'giris.html', {'hata': 'Geçersiz kullanıcı adı veya şifre'})
    return render(request, 'giris.html')


def send_password_reset_email(user_email, reset_link):
    subject = 'Şifre Sıfırlama'
    message = f'Lütfen aşağıdaki linke tıklayarak şifrenizi sıfırlayın: {reset_link}'
    recipient_list = [user_email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        if user:
            # Şifre sıfırlama linki oluştur
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = "https://sanalajanda.com/sifremi-sifirla/" + uidb64.decode() + "/" + token
            # E-postayı gönder
            send_password_reset_email(user.email, reset_link)
            return HttpResponse("Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.")


@login_required
def ana_sayfa(request):
    global form2
    not_metni = request.POST.get('not_metni')
    selected_date_input = request.POST.get('selected_date_input')

    if request.method == 'POST':
        if 'form1-submit' in request.POST:

            form2 = NotificationPreferenceForm(instance=request.user)

            if selected_date_input and not_metni:
                Tasks.objects.create(user=request.user, tarih=selected_date_input, not_metni=not_metni)
            secilen_tarih = request.GET.get('secilen_tarih')
            tasks = Tasks.objects.filter(user=request.user, tarih=secilen_tarih)
            return render(request, 'ana_sayfa.html',
                          {'form2': form2, 'tasks': tasks,
                           'secilen_tarih': secilen_tarih, "not_metni": not_metni,
                           "selected_date_input": selected_date_input})

        elif 'form2-submit' in request.POST:
            form2 = NotificationPreferenceForm(request.POST, instance=request.user)
            if form2.is_valid():
                form2.save()
                return redirect('ana_sayfa')

    else:

        form2 = NotificationPreferenceForm(instance=request.user)

    secilen_tarih = request.GET.get('secilen_tarih')
    tasks = Tasks.objects.filter(user=request.user, tarih=secilen_tarih)

    return render(request, 'ana_sayfa.html',
                  {'form2': form2, 'tasks': tasks,
                   'secilen_tarih': secilen_tarih, "not_metni": not_metni, "selected_date_input": selected_date_input})



@login_required
def arama(request):
    query = request.GET.get('q')
    if query:
        # Tarih ve not metni içinde arama yap
        tasks = Tasks.objects.filter(Q(tarih__icontains=query) | Q(not_metni__icontains=query),
                                     user=request.user).order_by('tarih')
    else:
        tasks = None
    return render(request, 'arama_sonucu.html', {'query': query, 'tasks': tasks})


@login_required
def notlari_mail_ile_gonder(request):
    if request.method == 'POST':
        secilen_tarih = request.POST.get('secilen_tarih')
        if secilen_tarih:
            tasks = Tasks.objects.filter(user=request.user, tarih=secilen_tarih)
            notlar = "\n".join([task.not_metni for task in tasks])
            user_email = request.user.email  # Kullanıcının kayıt olduğu mail adresi
            subject = f"{secilen_tarih} Notları"
            message = f"Seçili Tarih: {secilen_tarih}\nNotlar:\n{notlar}"
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[user_email], fail_silently=False)
            return redirect('ana_sayfa')

    return HttpResponse("Seçili bir tarih yok.")


@login_required
def ayarlar(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('ayarlar')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'ayarlar.html', {'form': form})
