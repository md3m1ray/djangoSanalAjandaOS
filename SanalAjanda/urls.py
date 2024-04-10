# SanalAjanda/SanalAjanda/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('kayit', views.kayit, name='kayit'),
    path('', views.giris, name='giris'),
    path('ana_sayfa', views.ana_sayfa, name='ana_sayfa'),
    # path('ayarlar', views.ayarlar, name='ayarlar'),
    path('sifremi-sifirla/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('sifremi-sifirla/yeniden-gonderildi/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('sifremi-sifirla/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('sifremi-sifirla/basarili/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('notlari-gonder/', views.notlari_mail_ile_gonder, name='notlari_gonder'),
    path('cikis/', views.cikis_yap, name='cikis'),
    path('ayarlar/', auth_views.PasswordChangeView.as_view(template_name='ayarlar.html'),
         name='password_change'),
    path('ayarlar/basarili/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/sifre_degistir_basarili.html'),
         name='password_change_done'),
    path('not-sil/<int:not_id>/', views.not_sil, name='not_sil'),
]
