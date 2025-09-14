
# 👗 StyleUp - เว็บไซต์ผู้ช่วยจัดการเสื้อผ้าและการแต่งตัว

**StyleUp** คือโปรเจกต์เว็บแอปพลิเคชันที่ทำหน้าที่เป็น "ตู้เสื้อผ้าอัจฉริยะ" ส่วนตัว  
ช่วยให้ผู้ใช้สามารถจัดเก็บคอลเลกชันเสื้อผ้าของตนเองในรูปแบบดิจิทัล,  
วิเคราะห์สีหลักของเสื้อผ้าแต่ละชิ้นโดยอัตโนมัติ, และรับคำแนะนำในการจับคู่เสื้อผ้าตามหลักทฤษฎีสี (Color Theory)  
เพื่อให้การแต่งตัวในทุก ๆ วันเป็นเรื่องง่ายและสนุกยิ่งขึ้น

---

## คุณสมบัติหลัก (Features)

- **ตู้เสื้อผ้าดิจิทัล:** จัดการเสื้อผ้าทั้งหมดของคุณในที่เดียว สามารถเพิ่มและลบไอเทมได้  
- **อัปโหลดรูปภาพ:** อัปโหลดรูปภาพของเสื้อผ้าแต่ละชิ้นเพื่อการแสดงผลที่ชัดเจน  
- **สกัดสีอัตโนมัติ:** ระบบจะวิเคราะห์และดึงกลุ่มสีหลักของเสื้อผ้าออกมาโดยอัตโนมัติเมื่อทำการอัปโหลด  
- **แนะนำการจับคู่ชุด:** เลือกเสื้อผ้า 1 ชิ้น แล้วระบบจะแนะนำไอเทมอื่น ๆ ในตู้ที่มีสีเข้ากันตามหลักทฤษฎีสี  
- **Responsive Design:** ออกแบบให้ใช้งานได้ดีทั้งบนคอมพิวเตอร์และสมาร์ตโฟน  

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

- **Backend:** [Flask](https://devhub.in.th/blog/flask-python) (Python Framework)  
- **Frontend:** HTML, CSS, Bootstrap 5  
- **Database:** [SQLite](https://devhub.in.th/blog/db-browser-for-sqlite) (Lightweight Database)  
- **Image Processing:** colorgram.py, Pillow  
- **Environment:** [Python Virtual Environment (venv)](https://devhub.in.th/blog/python-virtual-environment-venv)  

---

## 🚀 การติดตั้งและเริ่มใช้งาน (Getting Started)

### 1. เตรียมความพร้อม (Prerequisites)

- ตรวจสอบให้แน่ใจว่าได้ติดตั้ง Python 3.x บนเครื่องของคุณแล้ว

### 2. Clone หรือดาวน์โหลดโปรเจกต์

- นำไฟล์โปรเจกต์ทั้งหมดมาไว้ในโฟลเดอร์ `styleup`

### 3. สร้างและเปิดใช้งาน Virtual Environment

```bash
cd path/to/your/styleup
python3 -m venv env
````

* เปิดใช้งาน Virtual Environment

  * macOS/Linux:

    ```bash
    source env/bin/activate
    ```
  * Windows:

    ```bash
    env\Scripts\activate
    ```

> เมื่อสำเร็จ ที่หน้า Terminal จะมี `(env)` นำหน้า

### 4. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 5. สร้างฐานข้อมูล (Database)

```bash
python -m flask init-db
```

> รันครั้งแรกเพื่อสร้างไฟล์ `database.db` และตารางข้อมูล

### 6. รันโปรเจกต์

```bash
python -m flask run
```

* เปิดเว็บเบราว์เซอร์ไปที่:
  [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 โครงสร้างไฟล์ (Project Structure)

```
styleup/
├── env/                  # Virtual Environment (ไม่ถูก track โดย Git)
├── static/
│   └── uploads/          # เก็บไฟล์รูปภาพเสื้อผ้าที่ผู้ใช้อัปโหลด
├── templates/
│   ├── layout.html       # โครงสร้างหลักของหน้าเว็บ (Navbar, Footer)
│   ├── index.html        # หน้าแรก (แสดงเสื้อผ้าทั้งหมด)
│   ├── add_item.html     # ฟอร์มสำหรับเพิ่มเสื้อผ้า
│   └── recommend.html    # หน้าแสดงผลการแนะนำชุด
├── app.py                # ไฟล์หลักของโปรแกรม
├── database.db           # ไฟล์ฐานข้อมูล SQLite (ถูก ignore โดย Git)
├── schema.sql            # โค้ดสำหรับสร้างตารางในฐานข้อมูล
├── requirements.txt      # รายชื่อ dependencies
├── .gitignore            # ไฟล์บอก Git ไม่ให้ track อะไรบ้าง
└── README.md             # ไฟล์ที่คุณกำลังอ่านอยู่
```

---

## อธิบายแนวคิดหลักในโค้ด (Code Explanation)

### 1. การตั้งค่า Flask และ Route

* `app = Flask(__name__)` → สร้างเว็บแอปพลิเคชัน
* `@app.route('/')` → แสดงหน้าแรกด้วยฟังก์ชัน `index()`
* `@app.route('/add')` → แสดงฟอร์มเพิ่มไอเทมด้วยฟังก์ชัน `add_item()`

### 2. การจัดการฐานข้อมูล (Database)

* ใช้ SQLite (ไม่ต้องติดตั้งเพิ่ม)
* `get_db()` → ฟังก์ชันเชื่อมต่อกับไฟล์ `database.db`
* `db.execute(...)` → รันคำสั่ง SQL เช่น SELECT / INSERT

### 3. การอัปโหลดและสกัดสี (Image Upload & Color Extraction)

* `add_item()` รับไฟล์รูปภาพจากผู้ใช้
* `file.save(filepath)` → เซฟไฟล์ไปที่ `static/uploads/`
* `extract_colors(filepath)` → ใช้ **colorgram.py** วิเคราะห์สีหลักของเสื้อผ้า

### 4. ตรรกะการแนะนำชุด (Recommendation Logic)

* `recommend()` → ใช้กฎทฤษฎีสี (Color Theory)

  1. **Neutral Colors:** สีขาว เทา ดำ → เข้ากับทุกสี
  2. **Complementary Colors:** สีตรงข้ามบนวงล้อสี (ต่างกัน \~180°)
  3. **Analogous Colors:** สีที่อยู่ใกล้กันบนวงล้อสี

---

## แนวทางการพัฒนาต่อยอด (Future Improvements)

* **ระบบสมาชิก (User Accounts):** ผู้ใช้แต่ละคนมีตู้เสื้อผ้าเป็นของตัวเอง
* **บันทึกชุดที่ชอบ (Save Outfits):** เก็บชุดที่ระบบแนะนำหรือเลือกเอง
* **ค้นหาและกรองเสื้อผ้า (Search & Filter):** ค้นหาตามสี, ประเภท, สไตล์
* **แนะนำตามโอกาส (Occasion-based Recommendation):** ใช้ข้อมูลโอกาส เช่น ไปเที่ยว, ทำงาน



