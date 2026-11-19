# portfoy_bot_project
Portföy Bot Projesi
Bu proje, kullanıcıların Discord üzerinden kendi projelerini ekleyebilmelerini, projelerini görüntüleyebilmelerini, projelerine beceriler ekleyebilmelerini, proje bilgilerini güncelleyebilmelerini ve projelerini silebilmelerini sağlayan bir Discord botudur. Proje Python programlama dili kullanılarak geliştirilmiştir. Verilerin saklanması ve yönetilmesi için SQLite veritabanı kullanılmıştır. Projenin temel amacı, kullanıcıların portföylerini düzenli bir şekilde yönetmelerini kolaylaştırmaktır.

Projede bulunan bot.py dosyası, Discord botunun çalışmasını sağlayan ana dosyadır. Bu dosyada discord kütüphanesi botun Discord ile bağlantı kurmasını sağlamak için kullanılırken, commands modülü botun komutlarını tanımlamak için kullanılmıştır. from logic import DB_Manager satırı, veritabanı işlemlerini gerçekleştiren sınıfı başka bir dosyadan projeye dahil eder. from config import DATABASE, TOKEN satırı ise botun token bilgisine ve veritabanı dosyasının adına ulaşılmasını sağlar.

intents = discord.Intents.default() satırı botun kullanacağı varsayılan olay izinlerini oluşturur. intents.messages = True mesaj olaylarının kullanılmasını sağlarken, intents.message_content = True botun mesaj içeriklerini okuyabilmesine izin verir. bot = commands.Bot(command_prefix='!', intents=intents) satırı bot nesnesini oluşturur ve komutların ! işaretiyle başlamasını sağlar. manager = DB_Manager(DATABASE) satırı ise veritabanı işlemlerini yönetmek için bir nesne oluşturur.

on_ready() fonksiyonu, bot Discord'a başarıyla bağlandığında çalışır. Bu fonksiyon içerisindeki print() komutu botun giriş yaptığını terminal ekranına yazdırır. bot.user ifadesi ise botun Discord üzerindeki kullanıcı bilgilerini gösterir. Böylece botun düzgün şekilde çalışmaya başladığı anlaşılır.

!start komutu, kullanıcı botu ilk çalıştırdığında botun kendisini tanıtmasını sağlar. Bu komut içerisinde ctx parametresi, komutun gönderildiği kanal ve kullanıcı gibi bilgileri taşır. ctx.send() fonksiyonu Discord kanalına mesaj göndermek için kullanılır. await ifadesi, asenkron işlemin tamamlanmasını bekler. info(ctx) çağrısı ise kullanıcıya botun diğer komutları hakkında bilgi verilmesini sağlar.

!info komutu, botun kullanılabilir komutlarını ve bu komutların ne işe yaradığını kullanıcıya açıklar. Böylece kullanıcı botun özelliklerini öğrenebilir ve hangi komutu kullanması gerektiğini anlayabilir.

!new_project komutu, kullanıcının yeni bir proje eklemesini sağlar. Bu komut çalıştırıldığında kullanıcıdan proje adı, proje bağlantısı ve proje durumu gibi bilgiler istenir. ctx.author komutu kullanan kişiyi, ctx.channel ise komutun gönderildiği kanalı belirler. check fonksiyonu, gelen mesajın doğru kullanıcıdan ve doğru kanaldan gönderilip gönderilmediğini kontrol eder. bot.wait_for() fonksiyonu ise kullanıcıdan cevap gelmesini bekler. Alınan bilgiler bir araya getirilerek veritabanına gönderilir ve proje kaydedilir.

!projects komutu, kullanıcının daha önce eklediği projeleri görüntülemesini sağlar. Kullanıcının Discord ID bilgisi alınarak veritabanında o kullanıcıya ait projeler aranır. get_projects() fonksiyonu projeleri getirir. if koşulu, kullanıcının kayıtlı projesi olup olmadığını kontrol eder. Projeler bulunursa ekrana düzenli bir şekilde yazdırılır, bulunmazsa kullanıcıya henüz proje eklemediği bildirilir.

!skills komutu, kullanıcının projelerine beceri eklemesini sağlar. Öncelikle kullanıcının mevcut projeleri listelenir ve hangi projeye beceri eklemek istediği sorulur. Daha sonra eklenebilecek beceriler veritabanından alınır. Kullanıcının seçimi kontrol edilir ve geçerli bir beceri seçilmişse proje ile beceri ilişkilendirilerek veritabanına kaydedilir. Bu sayede projelerde kullanılan teknolojiler ve beceriler düzenli olarak tutulabilir.

!delete komutu, kullanıcının istediği projeyi silmesini sağlar. Öncelikle kullanıcının projeleri listelenir ve silmek istediği proje seçilir. Seçilen projenin veritabanındaki ID bilgisi bulunur. Daha sonra silme fonksiyonu çalıştırılarak proje veritabanından kaldırılır. İşlem tamamlandığında kullanıcıya projenin silindiğine dair mesaj gönderilir.

!update_projects komutu, kullanıcının daha önce oluşturduğu projelerde değişiklik yapmasını sağlar. Kullanıcı önce güncellemek istediği projeyi seçer. Ardından projenin hangi bilgisini değiştirmek istediği belirlenir. Proje adı, bağlantısı veya durumu gibi bilgiler güncellenebilir. Kullanıcıdan yeni bilgi alınır ve veritabanındaki eski bilgi yeni bilgiyle değiştirilir. Bu işlem sayesinde kullanıcı projelerini silip yeniden eklemek zorunda kalmadan düzenleyebilir.

Projede bulunan logic.py dosyası, veritabanı işlemlerinin gerçekleştirildiği bölümdür. sqlite3 kütüphanesi Python'un SQLite veritabanıyla bağlantı kurmasını sağlar. DB_Manager sınıfı, projeyle ilgili veritabanı işlemlerini tek bir yapı altında toplar. __init__() fonksiyonu sınıf oluşturulduğunda çalışır ve kullanılacak veritabanının adını self.database değişkeninde saklar.

create_tables() fonksiyonu, veritabanında projeler, beceriler ve proje durumları gibi bilgilerin saklanacağı tabloları oluşturur. SQL dilindeki CREATE TABLE IF NOT EXISTS komutu, tablo daha önce oluşturulmamışsa oluşturulmasını sağlar. Böylece verilerin düzenli bir şekilde saklanabileceği bir yapı hazırlanır.

__executemany() fonksiyonu, birden fazla verinin veritabanına eklenmesi veya üzerinde işlem yapılması için kullanılır. __select_data() fonksiyonu ise veritabanından bilgileri çekmek amacıyla SQL sorgularını çalıştırır. SELECT komutu verileri seçerken, fetchall() sorgu sonucunda bulunan kayıtların alınmasını sağlar.

default_insert() fonksiyonu, sistemde başlangıçta bulunması gereken becerileri ve proje durumlarını veritabanına ekler. INSERT OR IGNORE komutu, aynı kayıt zaten bulunuyorsa tekrar eklenmesini önlemeye yardımcı olur. insert_project() fonksiyonu yeni projelerin veritabanına kaydedilmesini sağlarken, insert_skill() fonksiyonu seçilen beceriyi ilgili projeyle ilişkilendirir.

get_statuses() fonksiyonu projelerin durumlarını listeler. get_status_id() fonksiyonu seçilen proje durumunun veritabanındaki ID bilgisini bulur. get_projects() fonksiyonu kullanıcıya ait projeleri getirirken, get_project_id() seçilen projenin ID bilgisini bulmak için kullanılır. get_skills() fonksiyonu sistemde kayıtlı becerileri getirir. get_project_skills() fonksiyonu ise bir projeye eklenmiş becerileri bulup görüntülemeye yardımcı olur.

get_project_info() fonksiyonu, belirli bir projeye ait bilgileri almak için kullanılır. update_projects() fonksiyonu proje bilgilerinin değiştirilmesini sağlayan SQL UPDATE sorgusunu çalıştırır. delete_project() fonksiyonu seçilen projenin veritabanından silinmesini sağlarken, delete_skill() fonksiyonu beceri kayıtları üzerinde silme işlemi gerçekleştirmek için kullanılır.

Son olarak config.py dosyası, projenin ayarlarını tutmak amacıyla kullanılır. Bu dosyada bulunan TOKEN değişkeni Discord botunun bağlantı kurabilmesi için gerekli token bilgisini, DATABASE değişkeni ise verilerin saklanacağı veritabanı dosyasının adını belirtir. Ayarların ayrı bir dosyada tutulması, kodun daha düzenli olmasını ve gerekli ayarların kolayca değiştirilebilmesini sağlar.

Bu proje sayesinde Python ile Discord botu geliştirme, komut oluşturma, asenkron programlama, kullanıcıdan veri alma, SQLite veritabanı kullanma, SQL sorguları oluşturma ve verileri ekleme, silme, listeleme ve güncelleme gibi temel yazılım geliştirme konuları uygulanmış olur.
