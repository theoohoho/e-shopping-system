const express = require('express');
const bodyParser = require('body-parser')
const app = express();
const cors = require('cors');

app.use(bodyParser.json())
app.use(cors());

// respond with "hello world" when a GET request is made to the homepage
app.get('/', function (req, res) {
  res.send('hello world');
});


// 管理員登入
app.post('/api/v1/admin/login', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 管理員登出
app.post('/api/v1/admin/logout', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 管理員註冊
app.post('/api/v1/admin/signup', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 註冊會員
app.post('/api/v1/signup', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 登入會員
app.post('/api/v1/login', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 登出會員
app.post('/api/v1/logout', (req, res, next) => {
  res.json({
    "message": "Success"
  })
})
// 取得產品列表
app.get('/api/v1/product', (req, res, next) => {
  res.json({
    "data": [{
      "product_id": "f65b8846-3",
      "product_name": "來去美國2",
      "product_type": "喜剧",
      "description": "",
      "image_url": "https://localhost/xxxx.jpg",
      "movie_runtime": "1h 50m",
      "movie_score": "71.0",
      "price": 710,
      "release_date": "",
      "source_url": "https://localhost/xxxxx",
      "store_pcs": 5
    }],
    "current_page": 0,
    "current_count":0,
    "total_count":0
  })
})
// 取得產品資訊
app.get('/api/v1/product/{product_id}', (req, res, next) => {
  res.json({
    "product_id": "f65b8846-3",
    "product_name": "來去美國2",
    "product_type": "喜剧",
    "description": "",
    "image_url": "https://localhost/xxxx.jpg",
    "movie_runtime": "1h 50m",
    "movie_score": "71.0",
    "price": 710,
    "release_date": "",
    "source_url": "https://localhost/xxxxx",
    "store_pcs": 5
  })
})
// 加入單項產品至購物車
app.post('/api/v1/cart', (req, res, next) => {
  res.json({
    "cart_id": ""
  })
})
// 取得購物車內容
app.get('/api/v1/cart/{cart_id}', (req, res, next) => {
  res.json({
    "data": [{
      "product_id": "",
      "product_name": "",
      "product_qty": 0,
      "product_price": "",
    }],
    "total": 0
  })
})
// 結帳
app.post('/api/v1/order', (req, res, next) => {
  res.json({
    "order_id": "",
    "order_date": "",
    "message": "Success"
  })
})
// 取得訂單列表
app.get('/api/v1/order', (req, res, next) => {
  res.json({
    "data": [{
      "order_id": "",
      "order_amount": "",
      "order_date": ""
    }],
    "current_page": 0,
    "current_count":0,
    "total_count":0
  })
})
// 加入產品至會員收藏
app.post('/api/v1/product/{product_id}/favorite', (req, res, next) => {
  res.json({
    "product_id": "",
    "message": "Success to add a new collect"
  })
})
// 會員收藏列表
app.get('/api/v1/favorite', (req, res, next) => {
  res.json({
    "data": [{
      "product_id": "",
      "product_name": "",
      "product_price": "",
      "product_type": "",
      "image_url": ""
  }],
    "current_page": 0,
    "current_count":0,
    "total_count":0
  })
})



const port = 3000
app.listen(port, () => {
  console.log(`API server is running, please access to http://localhost:${port}`)
})