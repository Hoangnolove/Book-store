# 📚 Bookstore Web Application (Django)

## 📑 Mục lục

1. [Mô tả dự án](#-mô-tả-dự-án)
2. [Tiến độ hiện tại](#-tiến-độ-hiện-tại)

   * [Đã hoàn thành](#-đã-hoàn-thành)
   * [Đang phát triển / Dự kiến](#-đang-phát-triển--dự-kiến)
3. [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
4. [Hướng dẫn cài đặt & chạy thử](#-hướng-dẫn-cài-đặt--chạy-thử)

   * [Clone repository](#1️⃣-clone-repository)
   * [Tạo môi trường ảo](#2️⃣-tạo-môi-trường-ảo-khuyến-nghị)
   * [Cài đặt thư viện](#3️⃣-cài-đặt-thư-viện)
   * [Migrate database](#4️⃣-migrate-database)
   * [Tạo tài khoản admin](#5️⃣-tạo-tài-khoản-admin)
   * [Chạy server](#6️⃣-chạy-server)
5. [Cấu trúc thư mục chính](#-cấu-trúc-thư-mục-chính)
6. [Tác giả](#-tác-giả)
7. [License](#-license)

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
* **Database:**  SQL Server 
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

* **Nhóm5 - CNTT K22C**
* **Nguyễn Lê Hoàng**
* **Hoàng Đức Hạnh**
* **Hoàng Duy Hanh**
* **Nguyễn Trung Kiên**
* **Lưu Đức Huân**

---

## 📄 License

Dự án được phát hành dưới giấy phép **MIT License**.
