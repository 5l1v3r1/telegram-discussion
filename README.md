# Telegram Soru-Cevap Başlatıcı

Aktif olarak soru cevap yapılan gruplarda oluşan karmaşayı önleyip sorulara verilen cevapları düzenli bir halde tutmayı amaçlamaktadır. Telegram'ın kanal mesajlarına eklediği yorum özelliği ile kullanılmaktadır.

Telegram için gereklilikler:
- 1 Telegram botu
- 1 Telegram kanalı 
- 1 Telegram grubu

Üstte belirtilen gereklilikler hali hazırda aktif bir grup olduğu düşünülerek yazılmıştır. Sıfırdan kurulum için 2 adet Telegram grubu gerekmektedir.

Yeni açtığınız Telegram grubu, yeni Telegram kanalına tartışma grubu olarak eklenmelidir. Aynı anda yalnızca 1 grubun kanala bağlanması ve ana grubun kirliliğinin önlenmesi için grupların bu şekilde oluşturulması gerekmektedir.

Yeni Bot ise grup ve kanal arasındaki iletişi sağlayacaktır. Botu oluşturduktan sonra gruplarınıza ve kanalınıza ekleyip yetkilendirin.

```
$ git clone https://github.com/ahmetveburak/telegram-discussion.git
$ cd telegram-discuss
```

- .ini.sample olan dosyaları .ini olarak düzenleyin ve gerekli bilgileri doldurun.

```
# settings.ini
# ID or NAME: -100123456789 veya @ olmadan Grupİsmi 
[discussion]
QA_GROUP: Aktif kullandığınız telegram grubu ID veya İSİM
DISCUSS_CHANNEL: Soru-Cevap'ların yapılacağı kanal ID veya İSİM
DISCUSS_GROUP: Soru-Cevap mesajlarının gideceği grup ID veya İSİM
MSG_COMMAND: Mesajları yönlendirecek alıntı komutu
```

`poetry` varsa:
```
$ poetry install
$ poetry shell
$ python -m telegramdiscuss
```

`poetry` yoksa:
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python -m telegramdiscuss
```

Yeni oluşturduğunuz Bot'un diğer kanal ve gruplara mesaj atabilmesi için session dosyası oluşmalıdır. Bunu için kullanmaya başlamadan önce yeni kanal ve gruplara 1 kez `/activate` mesajı atmanız gerekmektedir.

Bot kullanıma hazırdır. Ana grubunuzda soru-cevap olarak başlatmak istediğiniz mesajı alıntılayıp `/`.`!` veya `.` ile belirlediğiniz komutu yazarak kullanmaya başlayabilirsiniz.