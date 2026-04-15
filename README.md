# He thong Diem Danh Khuon Mat - MVP cho Do An Sinh Vien

## 1. Phan tich bai toan

### Mo ta bai toan
Can xay dung ung dung desktop giup quan ly sinh vien, dang ky khuon mat, diem danh bang webcam va luu lich su diem danh de tra cuu, thong ke, xuat bao cao.

### Muc tieu he thong
- Quan ly thong tin sinh vien theo lop.
- Dang ky du lieu khuon mat cho tung sinh vien.
- Diem danh tu dong hoac ban tu dong bang camera.
- Luu lich su diem danh theo ngay gio.
- Ho tro xem lich su, loc du lieu, xuat CSV.

### Yeu cau chuc nang
- Quan ly sinh vien: them, sua, xoa, tim kiem, xem danh sach.
- Dang ky khuon mat: mo webcam, chup nhieu anh, luu dataset.
- Diem danh: nhan dien khuon mat, ghi nhan thoi gian, tranh trung lap trong cung ngay.
- Lich su diem danh: loc theo ngay, lop, ma SV.
- Bao cao: xuat CSV, thong ke so lan co mat.

### Yeu cau phi chuc nang
- Chay tot tren Windows + VS Code.
- Giao dien don gian, de demo.
- Co the mo rong dan tu MVP len ban day du.
- Du lieu luu local, khong can server.

### Use case chinh
- Giang vien dang nhap va quan ly sinh vien.
- Giang vien dang ky khuon mat cho sinh vien moi.
- Giang vien mo man hinh diem danh de quet khuon mat.
- He thong ghi nhan lich su va xuat bao cao.

### Quy trinh hoat dong
1. Tao lop hoc, them sinh vien.
2. Dang ky khuon mat bang webcam.
3. Tao vector dac trung khuon mat tu anh dataset.
4. Mo webcam diem danh.
5. He thong nhan dien sinh vien va ghi vao bang diem danh.
6. Xem lich su va xuat bao cao.

### Goi y luong xu ly
`Webcam -> Phat hien khuon mat -> Ma hoa khuon mat -> So khop voi du lieu da dang ky -> Hien thi ten -> Ghi diem danh vao SQLite -> Xem lich su / xuat CSV`

### Goi y ERD
- `classes (1) -> (n) students`
- `students (1) -> (n) face_samples`
- `students (1) -> (n) attendance`
- `users (1) -> (n) attendance` theo vai tro thao tac

## 2. De xuat cong nghe toi uu cho sinh vien

### Lua chon khuyen nghi
- Ngon ngu: Python 3.11
- Giao dien: Tkinter
- Camera + xu ly anh: OpenCV (`opencv-python`)
- Co so du lieu: SQLite
- Xuat bao cao: `pandas`
- Nhan dien khuon mat:
  - MVP de demo: OpenCV Haar Cascade + so khop histogram/anh mau co ban
  - Nang cap sau: `face_recognition`

### Vi sao chon bo nay
- Nhe, de cai, de demo tren may Windows.
- Tkinter co san trong Python, khong can setup phuc tap nhu PyQt.
- SQLite khong can cai server, phu hop do an.
- OpenCV rat pho bien, nhieu tai lieu va de mo webcam.
- Kien truc nay cho phep nang cap len `face_recognition` ma khong phai viet lai toan bo app.

## 3. Thiet ke co so du lieu

### Bang `classes`
| Cot | Kieu | Rang buoc |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| class_code | TEXT | UNIQUE, NOT NULL |
| class_name | TEXT | NOT NULL |
| created_at | TEXT | NOT NULL |

### Bang `students`
| Cot | Kieu | Rang buoc |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| student_code | TEXT | UNIQUE, NOT NULL |
| full_name | TEXT | NOT NULL |
| class_id | INTEGER | FK -> classes(id) |
| date_of_birth | TEXT | NULL |
| gender | TEXT | NULL |
| face_image_path | TEXT | NULL |
| embedding_path | TEXT | NULL |
| created_at | TEXT | NOT NULL |
| updated_at | TEXT | NOT NULL |

### Bang `face_samples`
| Cot | Kieu | Rang buoc |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| student_id | INTEGER | FK -> students(id), NOT NULL |
| image_path | TEXT | NOT NULL |
| captured_at | TEXT | NOT NULL |

### Bang `attendance`
| Cot | Kieu | Rang buoc |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| student_id | INTEGER | FK -> students(id), NOT NULL |
| attendance_date | TEXT | NOT NULL |
| check_in_time | TEXT | NOT NULL |
| status | TEXT | NOT NULL |
| note | TEXT | NULL |
| created_at | TEXT | NOT NULL |

### Bang `users`
| Cot | Kieu | Rang buoc |
|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT |
| username | TEXT | UNIQUE, NOT NULL |
| password | TEXT | NOT NULL |
| full_name | TEXT | NOT NULL |
| role | TEXT | NOT NULL |
| created_at | TEXT | NOT NULL |

### SQL tao bang
Xem file `sql/schema.sql`

## 4. Kien truc thu muc project

```text
Big-projject/
|-- app/
|   |-- controllers/
|   |-- db/
|   |-- models/
|   |-- services/
|   |-- ui/
|   |-- utils/
|   `-- main.py
|-- data/
|   |-- dataset/
|   `-- attendance.db
|-- reports/
|-- sql/
|   `-- schema.sql
|-- requirements.txt
|-- run.py
`-- README.md
```

## 5. Chia module nho
- `app/db/database.py`: ket noi SQLite, tao bang.
- `app/services/student_service.py`: CRUD sinh vien.
- `app/services/face_service.py`: chup anh, luu dataset, mo hinh nhan dien.
- `app/services/attendance_service.py`: ghi va loc lich su diem danh.
- `app/ui/*.py`: tung man hinh Tkinter.
- `app/main.py`: ghep toan bo ung dung.

## 6. Giao dien de xuat

### Dang nhap
- 1 khung o giua man hinh.
- 2 o nhap: ten dang nhap, mat khau.
- Nut `Dang nhap`.
- Co the bo qua o MVP neu can demo nhanh.

### Dashboard
- Thanh menu ben trai.
- Khu noi dung ben phai.
- The thong ke nhanh: tong sinh vien, tong lop, so luot diem danh hom nay.

### Quan ly sinh vien
- Form ben trai: ma SV, ho ten, lop, ngay sinh, gioi tinh.
- Bang danh sach ben phai.
- Cac nut: Them, Sua, Xoa, Lam moi, Tim kiem.

### Dang ky khuon mat
- Combo chon sinh vien.
- Khung preview webcam.
- Nut `Bat dau chup`, `Dung`, `Tao du lieu nhan dien`.
- Danh sach anh da chup.

### Diem danh
- Preview webcam lon.
- Khung ket qua nhan dien.
- Bang cac ban ghi vua diem danh.
- Thong bao trung lap neu sinh vien da diem danh trong ngay.

### Lich su diem danh
- Thanh loc: ngay, lop, ma SV.
- Bang du lieu.
- Nut `Xuat CSV`.

## 7. Roadmap thuc hien theo tuan
- Tuan 1: Tao project, database, giao dien khung, dang nhap gia lap.
- Tuan 2: CRUD sinh vien, lop hoc, tim kiem.
- Tuan 3: Dang ky khuon mat, chup dataset bang webcam.
- Tuan 4: Nhan dien khuon mat va ghi diem danh.
- Tuan 5: Loc lich su, thong ke, xuat CSV.
- Tuan 6: Hoan thien demo, chup man hinh, viet bao cao.

## 8. Loi thuong gap
- Camera khong mo duoc: doi chi so camera `0/1`, dong ung dung khac dang chiem webcam.
- Khong cai duoc `face_recognition`: dung MVP voi OpenCV truoc, sau do cai Visual C++ Build Tools de nang cap.
- Unicode duong dan Windows: tranh dat project trong thu muc qua la, uu tien duong dan ngan.
- SQLite bi khoa file: dam bao dong app dung cach, khong mo file db bang cong cu khac khi dang chay.

## 9. Cach demo do an
1. Dang nhap bang tai khoan mac dinh `admin/admin123`.
2. Tao lop hoc va them 2-3 sinh vien.
3. Dang ky khuon mat cho tung sinh vien.
4. Mo man hinh diem danh va quet webcam.
5. Xem lich su va xuat CSV.

## 10. Huong dan viet bao cao do an
- Chuong 1: Dat van de, ly do chon de tai.
- Chuong 2: Co so ly thuyet ve OpenCV, SQLite, Tkinter.
- Chuong 3: Phan tich he thong, use case, ERD.
- Chuong 4: Cai dat he thong, giao dien, source code tieu bieu.
- Chuong 5: Demo, ket qua dat duoc, han che va huong phat trien.

## 11. MVP hien tai trong repo
- CRUD sinh vien.
- Quan ly lop hoc co ban.
- Dang ky khuon mat bang webcam, luu anh vao `data/dataset`.
- Tao du lieu dac trung khuon mat don gian.
- Diem danh co che nhan dien co ban + fallback de demo.
- Xem lich su va xuat CSV.

## 12. Chay project

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Neu chua cai duoc `face_recognition`, ung dung van chay voi che do MVP bang OpenCV.
