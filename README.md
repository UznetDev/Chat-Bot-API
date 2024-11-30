https://chatgpt.com/ ning clonini yaratish kerak.

OpeanAI API dan foydalanamiz.
Bizga kerak user ruyxatdan utishi kerag va login orqaliy tekshirilishi kerak, logindan utgandan sung login, parol saqlab qolish kerag va ikki kun ichida shu divacedan girganda login va parolni kiritmasligi kerak. Agar 2 kun ichida saytga kirmasa login va parolni kiritishi kerak. har bir userning uz iga bir profili bo'lishi kerak. va profilda oldingi chatlari ko'rish va yangi chat boshlash imkoniyati bo'lishi kerak.
Harbir userning oldin chatlari bulishi va limitga yitib bormangan chatlarni davomidan foydalan olishi kerag, agar limitga borsa faqat kura olsin. bitta chatdagi barcha yozishmalar shu chatda promt yozilishi uchun ishlatilishi shart, model javob berishda umumiy chatdagi suzlashuvni kura olishi kerag, Admin tomonidan umumiy chatlarni ko'rish va userlarni bloklash imkoniyati bo'lishi kerag. Admin userlarni bloklash va blokdan ochish imkoniyati bo'lishi kerag. admin tomonidan chatlarga limit quyish imkoni bulishi kerag, Admin Panel bulishi kerag admin kunlik foydalanish va umumiy staistikani ko'rishi kerag. user GPT modellarni ikranning tepasidan tanlay olishi kerag. 
Chatlar Mysqlda saqlanishi kerag.
Admin tomonida yangi bitt pdf faylga RAG orqaliy asoslangan model qushish imkoni bulsin, adminmodel ma'lumotlarini va model faylini kirita oladi va fayli RAG orqaliy vektorga aylantirib saqlanadi va shu vektorga asoslangan model yaratilid, user modelni tanlab ishlata oladi.
Model nomlash admin tominda kiritilgandan so'ng modelni ishga tushirish imkoni bulsin, modelni ishga tushirgandan so'ng modelni uchirish imkoniham qushilsin. modelni user tanlab ishlata olsin. Asosiy admin username va parol .env faylida saqlansin.
Frontend kurinishi https://chatgpt.com/ ga uxshash bulsin.
proyekt tuliq ishlashi uchun faqat main.py fayl run qilinishi kerag va barcha kerakliy fayllar ishga tushsin, mysqldagi barcha kerakliy tablelar mavjud bulmasa yaratilsin va fron qismiham FasAPI ining uzida ishga tushsin. kerakliy kutubxonalarni requirements.txt fayliga yozish kerag. agar user asosiy '/'pagega kursa va oldin login bulgan bulsa avtomatik yangi chat yaratilsin va user promt yozgandagina chat saqlansin aks holda ruyxatdan utish suralsin. umumiy proyiktni tushunib ol va ketma ketlikda yozib berishni boshla. Frontent qismi static va template orqaliy FastAPI ga bog'langan bulishi kerag.



Bu projectni yaratish uchun qanday texnologiyalar ishlatilishi kerag:
FastApi
Mysql, mysql.connector
LangChain
Frontent uchun kerakliy kutubxonalar soddaroq kutubxonalardan foydalanish kerag masan VueJs, ReactJs,AngularJs yokiy Html, Css va JavaScriptning uzi.
openai



Projectni structurasi:
main.py: asosiy ishga tushuruvchi fayl.
.env: barcha kerakliy maxfiy keylar masan openai keylari, mysql keylari, langchain keylari.
db/database.py: Database classi joylashgan fayl mysql uchun shudan foydalaniladi va brcha mysql blan ishlash methodlari shunda yoziladi.
loader.py: barcha kerakliy modullarni ishga tushurish uchun masalan openai, langchain, db.database.Database va hokazo.
file/: Botga RAG orqaliy berilgan pdf fayllarni saqlash joyi.
data/config.py: kerakliy uzgarmas parametirlarni saqlash va .env faylidan oqib olish uchun kerakliy fayl.
routes/registrate.py: user ruyxatdan utishi uchun kerakliy fayl.
routes/login.py: user login qilishi uchun kerakliy fayl.
routes/profile.py: user profilini ko'rish va yangi chat boshlash uchun kerakliy fayl.
routes/admin/: barcha admin panel fayllari
functions/functions.py: kerakliy funksiyalar joylashgan fayl.
templates/: kerakliy frontend fayllar joylashgan fayl.



Mysql jadvalda saqlash holtiga misollar:

user:
id: maxsus id
username: user ismi
password: user paroli
email: user emaili
date: user ro'yxatdan o'tgan vaqt

admin:
id: maxsus id
username: admin ismi
password: admin paroli
email: admin emaili
date: admin ro'yxatdan o'tgan vaqt

chat:
id: maxsus id
user_id: user idsi
date: chat yaratilgan vaqt


chat_history:
id: maxsus id
chat_id: chat idsi chat.id ga bog'lanadi
role: user yoki assistant
content: savol yoki javob
date: vaxt
rank: chatda nechinchi xabarlegi

model:
id: maxsus id
name: model nomi
file: model fayli
vector: model vektori
date: model yaratilgan vaqt



Xafsizlik:
user parolini hash qilib saqlash kerag.
user emaili vaqtida tasdiqlanishi kerag.
user parolini unutganda parolni tiklash imkoni bulsin.
user profilini o'zgartirish imkoni bulsin.
user profilini o'chirish imkoni bulsin.
admin userlarni chatlarini chop etish imkoni bulsin.

1. Asosiy structura
2. Database
3. Routes
4. Functions
5. Frontend

Barchasi bir biriga moslansin:


Database ga misol:






FastAPi va Mysql blan registratsiya tizim tuzib ber, login va registratsiya bulishi kerak va utgandan sung asosiy page ga utishi va ikiungacah login parolsiz shu divicedan kira olishi kerag.
user parolini hash qilib saqlash kerag.

Structura:
main.py: asosiy ishga tushuruvchi fayl.
.env: barcha kerakliy maxfiy keylar masan openai keylari, mysql keylari, langchain keylari.
db/database.py: Database classi joylashgan fayl mysql uchun shudan foydalaniladi va brcha mysql blan ishlash methodlari shunda yoziladi.
loader.py: barcha kerakliy modullarni ishga tushurish uchun masalan openai, langchain, db.database.Database ni db uzgaruvchiga ishga tushurish va hokazo.
routes/: kerakliy routlar uchun fayl
.env: barcha kerakliy maxfiy keylar masan openai keylari, mysql keylari, langchain keylari.
data/config.py: kerakliy uzgarmas parametirlarni saqlash va .env faylidan oqib olish uchun kerakliy fayl.
functions/: kerakliy funksiyalar joylashgan fayl.

Admin panelham bulishi kerag, admin ma'lumotlari .env faylida saqlansin.

Mysql jadvalda saqlash holtiga misollar:
user:
id: maxsus id
username: user ismi
password: user paroli
email: user emaili
date: user ro'yxatdan o'tgan vaqt

Mysql clasiga misol:
class Database:
    def __init__(self, host, user, password, database):
        """
        Initialize the Database object with connection parameters.

        Parameters:
        host (str): The hostname of the MySQL server.
        user (str): The username to connect to the MySQL server.
        password (str): The password to connect to the MySQL server.
        database (str): The name of the database to connect to.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.reconnect()

    def reconnect(self):
        """
        Reconnect to the MySQL database. If the connection fails, log the error and attempt to reconnect.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)

    def create_table_ban(self):
        """
        Create the 'ban' table if it does not already exist.
        """
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS ban (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cid bigint(20) NOT NULL UNIQUE,
                admin_cid bigint(20),
                date varchar(255)
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)

    def add_user_ban(self, cid, date, admin_cid):
        """
        Add a user to the 'ban' table.

        Parameters:
        cid (int): The user's chat ID.
        date (str): The date the user was banned.
        admin_cid (int): The admin's chat ID who banned the user.
        """
        try:
            sql = """
            INSERT INTO `ban` (`cid`,`admin_cid`,`date`) VALUES (%s,%s,%s)
            """
            values = (cid, admin_cid, date)
            self.cursor.execute(sql, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)

    def select_all_users_ban(self):
        """
        Select all users from the 'ban' table.

        Returns:
        list: A list of tuples containing all banned users.
        """
        try:
            sql = """
            SELECT * FROM `ban`
            """
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)

    Qolgan barcha methodlar: