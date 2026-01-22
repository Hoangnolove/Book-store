# 📚 Bookstore Web Application (Django)

## 📌 Mô tả dự án

Dự án **Bookstore** là một website bán sách được xây dựng bằng **Django**, cho phép người dùng xem danh sách sách, tìm kiếm theo thể loại, xem chi tiết sản phẩm và đặt hàng. Hệ thống có **dashboard quản trị (Django Admin)** để quản lý dữ liệu một cách thuận tiện.

---

## 🚀 Tiến độ hiện tại

### ✅ Đã hoàn thành

* Xây dựng cấu trúc project Django chuẩn
* Giao diện người dùng:

  * Trang chủ (Home)
  * Danh mục sách (Category)
  * Trang chi tiết sách (Detail)
  * Tìm kiếm sách (Search)
  * Giỏ hàng (Cart)
  * Thanh toán (Checkout)
  * Đăng nhập / Đăng ký
* Chức năng backend:

  * CRUD sản phẩm (Products)
  * CRUD danh mục (Categories)
  * Quản lý đơn hàng (Orders, Order Items)
  * Quản lý địa chỉ giao hàng (Shipping Address)
* Dashboard quản trị:

  * Sử dụng **Django Admin** để quản lý toàn bộ dữ liệu
  * Phân quyền người dùng (Admin / Staff)
* Quản lý source code bằng **Git & GitHub**

### ⏳ Đang phát triển / Dự kiến

* Hoàn thiện giao diện UI/UX
* Thêm thống kê đơn hàng (dashboard nâng cao)
* Tối ưu bảo mật & hiệu năng
* Deploy lên hosting (Render / PythonAnywhere)

---

## 🛠️ Công nghệ sử dụng

* **Python:** 3.11.9
* **Django:** 5.2.10
* **Frontend:** HTML, CSS, Bootstrap
* **Database:**  SQL Server (có thể mở rộng)
* **Version Control:** Git & GitHub

---

## ⚙️ Hướng dẫn cài đặt & chạy thử

### 1️⃣ Clone repository

```bash
git clone https://github.com/Hoangnolove/Book-store.git
cd Book-store
```

### 2️⃣ Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv venv
```

Kích hoạt môi trường ảo:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Cài đặt thư viện

```bash
pip install -r requirements.txt
```

(Nếu chưa có `requirements.txt`)

```bash
pip install django
```

---

### 4️⃣ Migrate database

```bash
python manage.py migrate
```

---

### 5️⃣ Tạo tài khoản admin

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Chạy server

```bash
python manage.py runserver
```

Truy cập:

* 🌐 Website: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* 🔐 Admin Dashboard: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📂 Cấu trúc thư mục chính

```
Book-store/
│── app/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── admin.py
│
│── webbansach/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── manage.py
│── README.md
│── .gitignore
```

---

## 👤 Tác giả

* **Hoàng Nguyễn**

---

## 📄 License

Dự án được phát hành dưới giấy phép **MIT License**.
