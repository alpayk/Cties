# Cties
Ülke Listesi
=================
Ülke listesi çekmek için. Bu listeyi cihazda uzun süreli cache' leyebilirsin bro.

URL: https://cties.herokuapp.com/country_list

Örnek Data: [{"id": 1, "name": "Afghanistan"}, {"id": 2, "name": "Albania"}, ...]

Soru Çekme
=================
Random soru getirir. Ülke id' lerinden birini URL sonuna ekleyerek sadece o ülkeye ait soruları getirebilirsin.

URL1: https://cties.herokuapp.com/question
URL2: https://cties.herokuapp.com/question/<ülke_id>

Örnek Data: {"options": [{"id": 1319, "name": "Lakhenpur"}, {"id": 5175, "name": "Sultanpur"}, {"id": 9435, "name": "Reserva"}, {"id": 40760, "name": "Kayseri"}, {"id": 41716, "name": "Falmouth-Penryn"}], "url": "https://www.google.com/maps/@38.7207494,35.4823757,3a,75y,88.09h,92.6t/data=!3m7!1e1!3m5!1sJ4YsSn9Um_0Y_YKK82x26A!2e0!6s%2F%2Fgeo2.ggpht.com%2Fcbk%3Fpanoid%3DJ4YsSn9Um_0Y_YKK82x26A%26output%3Dthumbnail%26cb_client%3Dmaps_sv.tactile.gps%26thumb%3D2%26w%3D203%26h%3D100%26yaw%3D11.282314%26pitch%3D0%26thumbfov%3D100!7i16384!8i8192", "id": 1, "text": "Buras\u0131 hangi \u015fehir?"}

Verification
=================
Verilen cevabı kontrol etmek için. question_id' yi üstteki api' den aldığın cevapta veriyorum. Seçeneklerin de her birinin id' leri var. soru ve cevabı bu servise gönderirsen doğrulayıp sana yanıt verecek.

URL: https://cties.herokuapp.com/verify/<question_id>/<answer_id>

Örnek Data: https://cties.herokuapp.com/verify/1/40760   -->   Correct / Incorrect
