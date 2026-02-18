# Web 框架案例

## 案例概述

本案例通过实际代码演示 Python Web 框架的使用，包括 Flask、Django、FastAPI。

## 知识点

1. **Flask**
   - 路由和视图
   - 蓝图
   - RESTful API

2. **Django**
   - MVC 架构
   - ORM
   - 中间件

3. **FastAPI**
   - 异步支持
   - 自动文档
   - 类型提示

## 案例代码

### 案例1：Flask 基础

```python
from flask import Flask, request, jsonify, render_template
from flask.blueprints import Blueprint

app = Flask(__name__)

# 路由和视图
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = {'id': user_id, 'name': 'Alice'}
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        'id': 3,
        'name': data.get('name'),
        'email': data.get('email')
    }
    return jsonify(user), 201

# 蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/posts')
def get_posts():
    return jsonify([{'id': 1, 'title': 'Post 1'}])

app.register_blueprint(api_bp)

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### 案例2：Django 基础

```python
# models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User

def user_list(request):
    users = User.objects.all()
    data = [{'id': u.id, 'name': u.name, 'email': u.email} for u in users]
    return JsonResponse(data, safe=False)

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    data = {'id': user.id, 'name': user.name, 'email': user.email}
    return JsonResponse(data)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]

# Django REST Framework
from rest_framework import viewsets, serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### 案例3：FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 数据模型
class User(BaseModel):
    name: str
    email: str

class UserResponse(User):
    id: int
    
    class Config:
        from_attributes = True

# 路由
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/users", response_model=List[UserResponse])
async def get_users():
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
    return users

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id == 1:
        return {"id": 1, "name": "Alice", "email": "alice@example.com"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/users", response_model=UserResponse, status_code=201)
async def create_user(user: User):
    return {"id": 3, **user.dict()}

# 依赖注入
def get_db():
    # 模拟数据库连接
    return "db_connection"

@app.get("/api/data")
async def get_data(db: str = Depends(get_db)):
    return {"data": "some data", "db": db}

# 异步支持
import asyncio

@app.get("/api/async")
async def async_endpoint():
    await asyncio.sleep(1)
    return {"message": "Async response"}
```

### 案例4：RESTful API 设计

```python
# Flask RESTful
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class UserList(Resource):
    def get(self):
        return {'users': [{'id': 1, 'name': 'Alice'}]}
    
    def post(self):
        return {'message': 'User created'}, 201

class User(Resource):
    def get(self, user_id):
        return {'id': user_id, 'name': 'Alice'}
    
    def put(self, user_id):
        return {'id': user_id, 'name': 'Updated'}
    
    def delete(self, user_id):
        return {'message': 'User deleted'}, 204

api.add_resource(UserList, '/api/users')
api.add_resource(User, '/api/users/<int:user_id>')
```

## 验证数据

### 框架性能对比

| 框架 | 请求处理时间 | 并发能力 | 适用场景 |
|-----|------------|---------|---------|
| Flask | 10ms | 中等 | 小型应用 |
| Django | 15ms | 中等 | 全功能应用 |
| FastAPI | 5ms | 高 | 高性能API |

## 总结

1. **Flask**
   - 轻量级
   - 灵活
   - 适合小型应用

2. **Django**
   - 全功能
   - ORM强大
   - 适合大型应用

3. **FastAPI**
   - 高性能
   - 异步支持
   - 自动文档
