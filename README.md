# Bookstore – Website Bán Sách (Django)

> Website bán sách trực tuyến được xây dựng bằng **Django Framework**

## Giới thiệu

**Bookstore** là một website bán sách trực tuyến được phát triển bằng **Django**, nhằm hỗ trợ người dùng dễ dàng **xem, tìm kiếm và mua sách online**. Dự án hướng tới việc xây dựng một hệ thống quản lý và bán sách đơn giản, trực quan, phù hợp cho **sinh viên, người yêu sách hoặc các cửa hàng sách nhỏ**.

Hệ thống cho phép quản trị viên **quản lý sản phẩm, danh mục, đơn hàng**, trong khi người dùng có thể **duyệt sách theo thể loại, xem chi tiết sản phẩm và đặt mua** một cách thuận tiện.

<!-- Logo / Ảnh đại diện sẽ được bổ sung sau -->

---

## Mục lục

* [Giới thiệu](#giới-thiệu)
* [Yêu cầu & Cài đặt](#yêu-cầu--cài-đặt)

  * [Yêu cầu](#yêu-cầu)
  * [Cài đặt](#cài-đặt)
* [Cách sử dụng](#cách-sử-dụng)
* [Công nghệ sử dụng](#công-nghệ-sử-dụng)

---

## Yêu cầu & Cài đặt

### Yêu cầu

Trước khi cài đặt dự án, hãy đảm bảo máy của bạn đã có:

* **Python** >= 3.
* **Django** >= 4.x / 5.x
* **Pip** (Python package manager)
* **Git**
* **Trình duyệt web** (Chrome, Edge, Firefox, ...)

---

### Cài đặt

Thực hiện các bước sau để chạy dự án Bookstore trên máy cục bộ:

1. **Clone repository**

   ```bash
   git clone https://github.com/username/bookstore.git
   cd bookstore
   ```

2. **Tạo và kích hoạt môi trường ảo (khuyến nghị)**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate  # Linux / MacOS
   ```

3. **Cài đặt các thư viện cần thiết**

   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình cơ sở dữ liệu**

   * Mặc định sử dụng **SQLite**
   * Có thể chỉnh trong file `settings.py` nếu dùng MySQL / PostgreSQL

5. **Chạy migrate**

   ```bash
   python manage.py migrate
   ```

6. **Tạo tài khoản admin**

   ```bash
   python manage.py createsuperuser
   ```

---

## Cách sử dụng

### Chạy ứng dụng

Chạy server Django bằng lệnh:

```bash
python manage.py runserver
```

Sau đó truy cập trên trình duyệt:

```
http://127.0.0.1:8000/
```

Trang quản trị admin:

```
http://127.0.0.1:8000/admin/
```

---

### Ví dụ sử dụng cơ bản

* Người dùng:

  * Xem danh sách sách
  * Lọc sách theo **thể loại**
  * Xem chi tiết sản phẩm
  * Đặt mua sách

* Quản trị viên:

  * Thêm / sửa / xóa sách
  * Quản lý danh mục (Category)
  * Quản lý đơn hàng

<!-- Ảnh chụp màn hình / GIF sẽ được bổ sung sau -->

---

## Công nghệ sử dụng

Dự án Bookstore được xây dựng với các công nghệ sau:

* **Ngôn ngữ**: Python 3.11.9
* **Backend Framework**: Django 5.2.10
* **Frontend**: HTML, CSS
* **UI Framework**: Bootstrap
* **Cơ sở dữ liệu**: SQL Server
* **Quản lý phiên bản**: Git & GitHub

---

## Ghi chú

* Dự án phục vụ mục đích **học tập và thực hành Django**.
* Có thể mở rộng thêm: giỏ hàng, thanh toán online, phân quyền người dùng.
* Hình ảnh giao diện và logo sẽ được cập nhật sau 📷
