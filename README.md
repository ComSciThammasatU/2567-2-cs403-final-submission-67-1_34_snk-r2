[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/w8H8oomW)
**<ins>Note</ins>: Students must update this `README.md` file to be an installation manual or a README file for their own CS403 projects.**

**รหัสโครงงาน:** 67-1_34_snk-r2

**ชื่อโครงงาน (ไทย):** เว็บแอปพลิเคชันสำหรับการจัดการคำสั่งซื้อเค้กออนไลน์

**Project Title (Eng):** WEB-APPLICATION FOR MANAGING ONLINE CAKE ORDER

**อาจารย์ที่ปรึกษาโครงงาน:** ผศ. ดร.ศาตนาฏ กิจศิรานุวัตร

**ผู้จัดทำโครงงาน:** 
1. นางสาวณัฐกานต์ วงศ์จิรสกุล 6309680046 nattakarn.won@dome.tu.ac.th
2. นายกฤติภูมิ ผิวเหมาะ 6309682075 kitipoom.phe@dome.tu.ac.th
   
Manual / Instructions for your projects starts here !

โปรเจกต์นี้เป็นเว็บแอปสำหรับร้านเค้ก พัฒนาด้วย Django และเสริมด้วยระบบวิเคราะห์ความคิดเห็น (Sentiment Analysis)

## โฟลเดอร์ย่อยในโปรเจกต์

1. `cake/` — เว็บแอปหลักที่พัฒนาด้วย Django
2. `senti/` — sentiment model ที่ให้บริการวิเคราะห์ความคิดเห็น โดยนำโมเดลจาก https://github.com/HRNPH/how2deploy มาปรับใช้งานกับเว็บแอปนี้
3. `final_reports/` – โฟลเดอร์นี้เก็บเอกสารรายงานทั้งหมดของโปรเจกต์ 
4. `demo/` – โฟลเดอร์นี้เก็บวิดีโอสำหรับสาธิตขั้นตอนการติดตั้งและใช้งานระบบ 

---

##  สิ่งที่ต้องติดตั้ง

- Python 3.10  (python 3.11ขึ้นไป ไม่รองรับ  tensorflow)

---

##  ไลบรารีที่จำเป็นหลังติดตั้ง Python แล้ว

ติดตั้งด้วยคำสั่ง:

```
pip install Django python-dotenv Pillow tensorflow numpy pythainlp fastapi uvicorn pydantic requests pandas
```

---

##  การใช้งานระบบสำหรับวิเคราะห์ความคิดเห็น (sentiment model)

ต้องมีไฟล์ต่อไปนี้ (ตาม path ด้านล่าง):

```
senti/how2deploy-master/finished/model/weight/model.h5
senti/how2deploy-master/finished/model/weight/tokenizer.pickle
```

จำเป็นต้องเข้าไปแก้ไข path ให้ตรงกับตำแหน่งที่เก็บไฟล์จริงในเครื่อง โดยแก้ที่ไฟล์:  
`senti/how2deploy-master/finished/model.py`
หลังแก้ path ที่อยู่ไฟล์แล้วให้ รัน model.py

เมื่อแก้ path เรียบร้อยแล้ว ให้รันไฟล์ `main.py` เพื่อเริ่มต้นเซิร์ฟเวอร์ของ sentiment API:

```
cd senti/how2deploy-master/finished
python main.py
```

---

##  การใช้งาน Django Web App

เริ่มจากการ ไปที่ /cake ที่เป็นส่วนของ django
กรณีต้องการใช้ระบบ otp
ในส่วนของ .env ให้ใส่ตัว api key ของบริการ Thaibulksms เพื่อทำการส่ง sms

### สำหรับสร้าง superuser:

```
ให้ cd ไปที่ cake แล้วสามารถพิมพ์คำสั่ง
python manage.py createsuperuser
ใช้เพื่อสร้างผู้ดูแลระบบของเว็บแอปพลิเคชั่น (แม่ค้า)
```

### สำหรับรันเว็บเซิร์ฟเวอร์:

```
ให้ cd ไปที่ cake แล้วสามารถพิมพ์คำสั่ง
python manage.py runserver
เพื่อทำการ run ตัวเว็บแอปพลิเคชั่นขึ้นมา โดยที่อยู่ของเว็บจะแสดงใน console
หรือเข้าเว็บได้ที่: http://127.0.0.1:8000
```

---

##  หมายเหตุ

- Django และ Sentiment model แยกกันรัน
- ให้รันทั้ง `cake/` และ `senti/how2deploy-master/finished/model.py`
- ตรวจสอบให้แน่ใจว่า path ของโมเดลใน `senti/how2deploy-master/finished/model.py` ถูกต้อง

