# SQLite veritabanıyla çalışmak için kütüphaneyi ekliyoruz.
import sqlite3
# Veritabanı dosya adını ayarlardan alıyoruz.
from config import DATABASE

# Projelerde kullanılabilecek becerileri listeliyoruz.
skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Discord'])]
# Projelerin durum seçeneklerini belirliyoruz.
statuses = [ (_,) for _ in (['Prototip Oluşturma', 'Geliştirme Aşamasında', 'Tamamlandı, kullanıma hazır', 'Güncellendi', 'Tamamlandı, ancak bakımı yapılmadı'])]

# Veritabanı işlemlerini bu sınıfın içinde topluyoruz.
class DB_Manager:
    # Sınıf oluşturulurken gerekli bilgileri alıyoruz.
    def __init__(self, database):
        # Veritabanı adını nesnede saklıyoruz.
        self.database = database
        
    # Veritabanında gerekli tabloları oluşturuyoruz.
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills(
                            project_id INTEGER,
                            skill_id INTEGER,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT
                        )''')
            conn.commit()

    # Bir SQL sorgusunu birden fazla kayıtla çalıştırmak için yardımcı fonksiyon.
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            # Sorguyu verilen kayıtlarla toplu olarak çalıştırıyoruz.
            conn.executemany(sql, data)
            conn.commit()
    
    # Veritabanından bilgi çekmek için fonksiyon.
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            # SQL sorgusu çalıştırmak için cursor oluşturuyoruz.
            cur = conn.cursor()
            # Sorguyu verilen bilgilerle çalıştırıyoruz.
            cur.execute(sql, data)
            return cur.fetchall()
        
    # Başlangıç becerilerini ve proje durumlarını veritabanına ekliyoruz.
    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)


    # Yeni proje eklemek için fonksiyon.
    def insert_project(self, data):
        sql = """INSERT INTO projects 
                (user_id, project_name, url, status_id) 
                values(?, ?, ?, ?)"""
        self.__executemany(sql, data)


    # Bir projeye beceri eklemek için fonksiyon.
    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id, skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES(?, ?)'
        self.__executemany(sql, data)


    # Proje durumlarını veritabanından getiriyoruz.
    def get_statuses(self):
        sql = "SELECT status_name from status"
        return self.__select_data(sql)
        

    # Durum adına göre ID bilgisini buluyoruz.
    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    # Kullanıcının projelerini listelemek için fonksiyon.
    def get_projects(self, user_id):
        sql = """SELECT * FROM projects WHERE user_id = ?"""
        return self.__select_data(sql, data = (user_id,))
        
    # Proje adı ve kullanıcıya göre proje IDsi buluyoruz.
    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]
        
    # Becerileri veritabanından getiriyoruz.
    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')
    
    # Projeye eklenmiş becerileri buluyoruz.
    def get_project_skills(self, project_name):
        res = self.__select_data(sql='''SELECT skill_name FROM projects 
JOIN project_skills ON projects.project_id = project_skills.project_id 
JOIN skills ON skills.skill_id = project_skills.skill_id 
WHERE project_name = ?''', data = (project_name,) )
        return ', '.join([x[0] for x in res])
    
    # Projenin detay bilgilerini getirmeye yarıyor.
    def get_project_info(self, user_id, project_name):
        sql = """SELECT project_name, description, url, status_name FROM projects 
                 JOIN status ON
                 status.status_id = projects.status_id)
                 WHERE project_name=? AND user_id=?"""
        return self.__select_data(sql=sql, data = (project_name, user_id))


    # Projede seçilen bilgiyi güncellemek için fonksiyon.
    def update_projects(self, param, data):
        sql = f"""UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?"""
        self.__executemany(sql, [data]) 


    # Kullanıcının seçtiği projeyi silmek için fonksiyon.
    def delete_project(self, user_id, project_id):
        sql = """DELETE FROM projects WHERE user_id = ? AND project_id = ? """
        self.__executemany(sql, [(user_id, project_id)])
    
    # Projeye bağlı beceri kaydını silmek için fonksiyon.
    def delete_skill(self, project_id, skill_id):
        sql = """DELETE FROM skills WHERE skill_id = ? AND project_id = ? """
        self.__executemany(sql, [(skill_id, project_id)])


# Dosya doğrudan çalıştırılırsa test bölümü devreye giriyor.
if __name__ == '__main__':
    # Veritabanı yöneticisini oluşturuyoruz.
    manager = DB_Manager(DATABASE)
    # Gerekli tabloları oluşturmaya çalışıyoruz.
    manager.create_tables()
    # Başlangıç beceri ve durum kayıtlarını ekliyoruz.
    manager.default_insert()
    # Örnek proje kaydı ekleyerek test ediyoruz.
    manager.insert_project([(1, 'My First Project', 'https://example.com', 1)])
    # Yöntemlerinizi burada test edin!

