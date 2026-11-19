# Discord botunu yazabilmek için Discord kütüphanesini ekliyoruz.
import discord
# Komutları daha rahat tanımlamak için commands kısmını kullanıyoruz.
from discord.ext import commands
# Veritabanı işlemlerini yapan sınıfı diğer dosyadan alıyoruz.
from logic import DB_Manager
# Token ve veritabanı ayarlarını config dosyasından alıyoruz.
from config import DATABASE, TOKEN

# Botun hangi Discord olaylarını kullanacağını ayarlıyoruz.
intents = discord.Intents.default()
# Mesaj olaylarını açıyoruz.
intents.messages = True
# Botun mesaj içeriklerini okuyabilmesini açıyoruz.
intents.message_content = True

# Botu oluşturuyoruz ve komutların ! ile başlamasını ayarlıyoruz.
bot = commands.Bot(command_prefix='!', intents=intents)
# Veritabanı işlemleri için yönetici nesnesi oluşturuyoruz.
manager = DB_Manager(DATABASE)

# Discord olaylarından birini dinlemek için event tanımlıyoruz.
@bot.event
# Bot Discorda bağlanınca bu fonksiyon çalışıyor.
async def on_ready():
    # Botun giriş yaptığını terminalde gösteriyoruz.
    print(f'Bot hazır! {bot.user} olarak giriş yapıldı.')

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='start')
# !start komutu çalışınca burası devreye giriyor.
async def start_command(ctx):
    await ctx.send("Merhaba! Ben bir proje yöneticisi botuyum.\nProjelerinizi ve onlara dair tüm bilgileri saklamanıza yardımcı olacağım! =)")
    await info(ctx)

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='info')
# Kullanılabilir komutları gösteren fonksiyon.
async def info(ctx):
    await ctx.send("""
Kullanabileceğiniz komutlar şunlardır:

!new_project - yeni bir proje eklemek
!projects - tüm projelerinizi listelemek
!update_projects - proje verilerini güncellemek
!skills - belirli bir projeye beceri eklemek
!delete - bir projeyi silmek

Ayrıca, proje adını yazarak projeyle ilgili tüm bilgilere göz atabilirsiniz!""")

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='new_project')
# Yeni proje ekleme komutunun işlemleri burada.
async def new_project(ctx):
    await ctx.send("Lütfen projenin adını girin!")

    # Gelen cevabın komutu kullanan kişiden ve aynı kanaldan olmasını kontrol ediyor.
    def check(msg):
        # Mesajı yazan kişi ve kanal doğru mu diye kontrol ediyoruz.
        return msg.author == ctx.author and msg.channel == ctx.channel

    name = await bot.wait_for('message', check=check)
    data = [ctx.author.id, name.content]
    await ctx.send("Lütfen projeye ait bağlantıyı gönderin!")
    link = await bot.wait_for('message', check=check)
    data.append(link.content)

    # Veritabanındaki proje durumlarını alıyoruz.
    statuses = [x[0] for x in manager.get_statuses()]
    await ctx.send("Lütfen projenin mevcut durumunu girin!", delete_after=60.0)
    await ctx.send("\n".join(statuses), delete_after=60.0)
    
    status = await bot.wait_for('message', check=check)
    # Girilen durum listede var mı kontrol ediyoruz.
    if status.content not in statuses:
        await ctx.send("Seçtiğiniz durum listede bulunmuyor. Lütfen tekrar deneyin!", delete_after=60.0)
        return

    # Seçilen durumun veritabanındaki ID bilgisini buluyoruz.
    status_id = manager.get_status_id(status.content)
    data.append(status_id)
    # Proje bilgilerini veritabanına kaydediyoruz.
    manager.insert_project([tuple(data)])
    await ctx.send("Proje kaydedildi")

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='projects')
# Kullanıcının kayıtlı projelerini listeleyen fonksiyon.
async def get_projects(ctx):
    # Komutu kullanan kişinin Discord ID bilgisini alıyoruz.
    user_id = ctx.author.id
    # Bu kullanıcıya ait projeleri veritabanından getiriyoruz.
    projects = manager.get_projects(user_id)
    # Kullanıcının projesi varsa aşağıdaki işlemler yapılıyor.
    if projects:
        text = "\n".join([f"Project name: {x[2]} \nLink: {x[4]}\n" for x in projects])
        await ctx.send(text)
    else:
        await ctx.send('Henüz herhangi bir projeniz yok!\nBir tane eklemeyi düşünün! !new_project komutunu kullanabilirsiniz.')

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='skills')
# Projeye beceri ekleme işlemini yapan fonksiyon.
async def skills(ctx):
    # Komutu kullanan kişinin Discord ID bilgisini alıyoruz.
    user_id = ctx.author.id
    # Bu kullanıcıya ait projeleri veritabanından getiriyoruz.
    projects = manager.get_projects(user_id)
    # Kullanıcının projesi varsa aşağıdaki işlemler yapılıyor.
    if projects:
        # Projelerin isimlerini ayrı bir listeye alıyoruz.
        projects = [x[2] for x in projects]
        await ctx.send('Bir beceri eklemek istediğiniz projeyi seçin')
        await ctx.send("\n".join(projects))

        # Gelen cevabın komutu kullanan kişiden ve aynı kanaldan olmasını kontrol ediyor.
        def check(msg):
            # Mesajı yazan kişi ve kanal doğru mu diye kontrol ediyoruz.
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send('Bu projeye sahip değilsiniz, lütfen tekrar deneyin! Beceri eklemek istediğiniz projeyi seçin')
            return

        # Veritabanındaki becerileri listeye alıyoruz.
        skills = [x[1] for x in manager.get_skills()]
        await ctx.send('Bir beceri seçin')
        await ctx.send("\n".join(skills))

        skill = await bot.wait_for('message', check=check)
        if skill.content not in skills:
            await ctx.send('Görünüşe göre seçtiğiniz beceri listede yok! Lütfen tekrar deneyin! Bir beceri seçin')
            return

        # Seçilen beceriyi projeye ekliyoruz.
        manager.insert_skill(user_id, project_name.content, skill.content)
        await ctx.send(f'{skill.content} becerisi {project_name.content} projesine eklendi')
    else:
        await ctx.send('Henüz herhangi bir projeniz yok!\nBir tane eklemeyi düşünün! !new_project komutunu kullanabilirsiniz.')

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='delete')
# Seçilen projeyi silme işlemini yapan fonksiyon.
async def delete_project(ctx):
    # Komutu kullanan kişinin Discord ID bilgisini alıyoruz.
    user_id = ctx.author.id
    # Bu kullanıcıya ait projeleri veritabanından getiriyoruz.
    projects = manager.get_projects(user_id)
    # Kullanıcının projesi varsa aşağıdaki işlemler yapılıyor.
    if projects:
        # Projelerin isimlerini ayrı bir listeye alıyoruz.
        projects = [x[2] for x in projects]
        await ctx.send("Silmek istediğiniz projeyi seçin")
        await ctx.send("\n".join(projects))

        # Gelen cevabın komutu kullanan kişiden ve aynı kanaldan olmasını kontrol ediyor.
        def check(msg):
            # Mesajı yazan kişi ve kanal doğru mu diye kontrol ediyoruz.
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send('Bu projeye sahip değilsiniz, lütfen tekrar deneyin!')
            return

        # Silmek istediğimiz projenin ID bilgisini buluyoruz.
        project_id = manager.get_project_id(project_name.content, user_id)
        # Seçilen projeyi veritabanından siliyoruz.
        manager.delete_project(user_id, project_id)
        await ctx.send(f'{project_name.content} projesi veri tabanından silindi!')
    else:
        await ctx.send('Henüz herhangi bir projeniz yok!\nBir tane eklemeyi düşünün! !new_project komutunu kullanabilirsiniz.')

# Bir Discord komutunu tanımlıyoruz.
@bot.command(name='update_projects')
# Proje bilgilerini güncelleme işlemini yapan fonksiyon.
async def update_projects(ctx):
    # Komutu kullanan kişinin Discord ID bilgisini alıyoruz.
    user_id = ctx.author.id
    # Bu kullanıcıya ait projeleri veritabanından getiriyoruz.
    projects = manager.get_projects(user_id)
    # Kullanıcının projesi varsa aşağıdaki işlemler yapılıyor.
    if projects:
        # Projelerin isimlerini ayrı bir listeye alıyoruz.
        projects = [x[2] for x in projects]
        await ctx.send("Güncellemek istediğiniz projeyi seçin")
        await ctx.send("\n".join(projects))

        # Gelen cevabın komutu kullanan kişiden ve aynı kanaldan olmasını kontrol ediyor.
        def check(msg):
            # Mesajı yazan kişi ve kanal doğru mu diye kontrol ediyoruz.
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send("Bir hata oldu! Lütfen güncellemek istediğiniz projeyi tekrar seçin:")
            return

        await ctx.send("Projede neyi değiştirmek istersiniz?")
        # Güncellenebilecek proje alanlarını ve veritabanındaki isimlerini eşleştiriyoruz.
        attributes = {'Proje adı': 'project_name', 'Açıklama': 'description', 'Proje bağlantısı': 'url', 'Proje durumu': 'status_id'}
        await ctx.send("\n".join(attributes.keys()))

        attribute = await bot.wait_for('message', check=check)
        if attribute.content not in attributes:
            await ctx.send("Hata oluştu! Lütfen tekrar deneyin!")
            return

        # Durum seçeneği değiştirilecekse bu bölüme giriyoruz.
        if attribute.content == 'Durum':
            # Veritabanındaki proje durumlarını alıyoruz.
            statuses = manager.get_statuses()
            await ctx.send("Projeniz için yeni bir durum seçin")
            await ctx.send("\n".join([x[0] for x in statuses]))
            update_info = await bot.wait_for('message', check=check)
            if update_info.content not in [x[0] for x in statuses]:
                await ctx.send("Yanlış durum seçildi, lütfen tekrar deneyin!")
                return
            update_info = manager.get_status_id(update_info.content)
        else:
            await ctx.send(f"{attribute.content} için yeni bir değer girin")
            update_info = await bot.wait_for('message', check=check)
            update_info = update_info.content

        # Seçilen proje bilgisini yeni değerle güncelliyoruz.
        manager.update_projects(attributes[attribute.content], (update_info, project_name.content, user_id))
        await ctx.send("Tüm işlemler tamamlandı! Proje güncellendi!")
    else:
        await ctx.send('Henüz herhangi bir projeniz yok!\nBir tane eklemeyi düşünün! !new_project komutunu kullanabilirsiniz.')

# Tokenı kullanarak botu Discordda çalıştırıyoruz.
bot.run(TOKEN)
