# E-shopping system
模擬線上購物網站，產品僅提供電影，沒版權，沒通路，主要給我 high

## 功能
### 後台 - 登入系統/會員管理系統 - 用 FLASK ADMIN 來做
- POST `/admin/login` 管理員登入
- POST `/admin/logout` 管理員登出
- POST `/admin/signup` 管理員註冊

### 前台 - product page
- POST `/signup` 註冊會員
- POST `/login` 登入會員
- POST `/logout` 登出會員
- GET `/products` 取得產品列表
- GET `/product/{product_id}` 取得產品資訊
- POST `/cart` 加入單項產品至購物車
- GET `/cart` 取得購物車內容
- POST `/order` 結帳
- GET `/order` 取得訂單列表
- POST `/product/{product_id}/favorite` 加入產品至會員收藏

## database table schema
- customer
  - customer_id 客戶編號 VARCHAR(50) (PK)
  - customer_name 客戶名稱 VARCHAR(255), NOT NULL
  - hashed_password VARCHAR(255), NOT NULL
  - email 客戶信箱 VARCHAR(255), NOT NULL

- customer_login_history
  - id 流水號 INT (PK)
  - customer_id 客戶編號 VARCHAR(50), NOT NULL
  - login_time 登入時間 DATETIME, NOT NULL
  - login_status 登入狀態 VARCHAR(10), NOT NULL
  - ip_address VARCHAR(10)

- product
  - product_id 商品編號 VARCHAR(40) (PK)
  - product_name 商品名稱 VARCHAR(255), NOT NULL
  - type 商品類別 VARCHAR(10)
  - store_pcs 商品數量 INT, NOT NULL
  - price 商品價格 INT, NOT NULL
  - description 商品描述 VARCHAR(255)
  - movie_time 電影片長 VARCHAR(10)

- product_type
  - id INT (PK)
  - type_name VARCHAR(10), NOT NULL

- order
  - order_id 訂單編號 VARCHAR(50) (PK)
  - customer_id 客戶編號 VARCHAR(50) (FK)
  - total_price 總價格 INT, NOT NULL
  - order_time 訂購時間 DATETIME, NOT NULL

- order_items
  - id 流水號 (PK)
  - order_id 訂單編號 (FK) VARCHAR(50), INDEX, NOT NULL
  - product_id 商品編號 (FK) VARCHAR(40), NOT NULL
  - quantity 購買數量 INT, NOT NULL
  - price 產品總價 INT, NOT NULL 

![](./system-data-model.png)