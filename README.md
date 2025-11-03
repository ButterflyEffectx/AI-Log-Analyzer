# 🧠 AI Log Analyzer  
**Intelligent Log Analysis System for Security Incident Detection**

---

## 📌 Project Overview
AI Log Analyzer เป็นโปรเจกต์ที่พัฒนาขึ้นเพื่อ **วิเคราะห์ Log ความปลอดภัย** และตรวจจับเหตุการณ์ที่อาจเป็นภัยคุกคาม เช่น **Brute-force login attacks**  
ระบบสามารถรวบรวม log จากหลายแหล่ง จัดเก็บ วิเคราะห์ และสรุปผลด้วย **AI Summarization Model (OpenAI API)** เพื่อช่วยให้ผู้ดูแลระบบมองเห็นภัยคุกคามได้ชัดเจนขึ้นแบบเรียลไทม์  

---

## 🧩 System Workflow
1. **Victim VM (Kali Linux / Ubuntu)**  
   - จำลองการโจมตีแบบ SSH brute-force  
   - สร้าง log การโจมตีจริง  

2. **API Collector**  
   - รับ log จาก Host ผ่าน API  
   - ส่งต่อไปเก็บในฐานข้อมูล PostgreSQL  

3. **PostgreSQL Database**  
   - จัดเก็บ log และ metadata ทั้งหมด  
   - ใช้เป็นแหล่งข้อมูลหลักให้ Analyzer  

4. **Host Analyzer (AI + Heuristic Engine)**  
   - ดึง log มาวิเคราะห์  
   - ใช้ rule-based และ AI summarization เพื่อสรุปเหตุการณ์  

5. **Streamlit Dashboard**  
   - แสดงผลลัพธ์แบบ Interactive  
   - สรุปเหตุการณ์, แจ้งเตือน, และแนะนำการตอบสนอง  

---

## ⚙️ Technologies Used
| Category | Tools / Frameworks |
|-----------|--------------------|
| **Operating Systems** | Kali Linux, Ubuntu/Debian |
| **Backend & API** | Python (FastAPI), PostgreSQL (Render) |
| **Frontend/UI** | Streamlit |
| **AI & ML** | OpenAI API |
| **Security Testing** | SSH Brute-force Simulation, Log Analysis |
| **Others** | Docker (optional), RESTful API |

---

## 🔍 Features
- ตรวจจับและสรุปเหตุการณ์ **Brute-force Login** อัตโนมัติ  
- วิเคราะห์และตีความ log ด้วย **AI Summarization Model**  
- แสดงข้อมูลผ่าน **Interactive Streamlit Dashboard**  
- รองรับการแจ้งเตือน (Alert) และ Action เช่น Block IP หรือ Reset Password  
- ออกแบบให้ขยายไปใช้กับ **Web Server Logs / Firewall Logs** ได้  

---

## 🧪 Example Workflow
1. จำลองการโจมตี SSH brute-force จากเครื่อง VM  
2. API Collector เก็บ log และส่งเข้าฐานข้อมูล PostgreSQL  
3. Host Analyzer ประมวลผลด้วย heuristic + AI summarization  
4. Dashboard แสดงสรุปการโจมตี พร้อมคำแนะนำเชิงปฏิบัติ  

---

## 🧰 Skills Demonstrated
- Cybersecurity: Log Monitoring, Threat Detection  
- Data Engineering: API Data Pipeline, Log Management  
- Artificial Intelligence: Summarization, NLP-based Analysis  
- Software Development: Python, API Integration, Dashboard UI  

---

## 📎 Author
**Peeraphat Mikanuch**  
Computer Science, Maejo University  
📧 ifx.pmn@gmail.com  
📱 083-049-7720  

---

> “AI Log Analyzer aims to empower security monitoring with intelligent automation — bridging data engineering and cybersecurity together.”
