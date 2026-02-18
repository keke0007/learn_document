# 案例3：用户行为分析

## 案例描述
分析用户行为数据，包括用户访问日志、页面浏览记录、用户注册信息等，进行用户活跃度分析和行为路径分析。

## 数据准备

### 1. 用户访问日志 (user_logs.txt)
```
2024-01-15 09:15:23,U001,page_view,/home,10
2024-01-15 09:16:45,U001,page_view,/products,25
2024-01-15 09:18:12,U001,click,button_buy,5
2024-01-15 10:20:30,U002,page_view,/home,8
2024-01-15 10:22:15,U002,page_view,/products,30
2024-01-15 10:25:40,U002,page_view,/cart,15
2024-01-15 11:30:20,U003,page_view,/home,12
2024-01-15 11:32:50,U003,page_view,/products,20
2024-01-15 14:15:10,U001,page_view,/home,5
2024-01-15 14:16:30,U001,page_view,/products,18
2024-01-16 09:10:15,U002,page_view,/home,10
2024-01-16 09:12:30,U002,page_view,/products,22
2024-01-16 09:15:45,U002,click,button_add_cart,3
2024-01-16 10:30:20,U004,page_view,/home,15
2024-01-16 10:32:10,U004,page_view,/products,28
2024-01-16 10:35:25,U004,page_view,/cart,12
2024-01-16 10:37:50,U004,click,button_checkout,8
2024-01-17 08:20:15,U001,page_view,/home,8
2024-01-17 08:22:30,U001,page_view,/products,25
2024-01-17 08:25:45,U001,click,button_buy,4
2024-01-17 09:15:20,U003,page_view,/home,10
2024-01-17 09:17:35,U003,page_view,/products,30
2024-01-17 09:20:50,U003,page_view,/cart,20
2024-01-17 09:23:15,U003,click,button_checkout,6
```

### 2. 用户信息表 (users.txt)
```
U001,张三,男,25,北京,2023-06-15,Gold
U002,李四,女,28,上海,2023-07-20,Silver
U003,王五,男,32,广州,2023-05-10,Gold
U004,赵六,女,26,深圳,2023-08-05,Silver
U005,孙七,男,30,北京,2023-09-12,Bronze
```

## 建表语句

```sql
-- 创建用户访问日志表
CREATE TABLE IF NOT EXISTS user_logs (
    log_time TIMESTAMP,
    user_id STRING,
    action_type STRING,
    page_url STRING,
    duration INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- 创建用户信息表
CREATE TABLE IF NOT EXISTS users (
    user_id STRING,
    user_name STRING,
    gender STRING,
    age INT,
    city STRING,
    register_date DATE,
    vip_level STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

## 加载数据

```sql
LOAD DATA LOCAL INPATH '/path/to/user_logs.txt' INTO TABLE user_logs;
LOAD DATA LOCAL INPATH '/path/to/users.txt' INTO TABLE users;
```

## 查询案例

### 1. 用户活跃度分析
```sql
-- 每日活跃用户数（DAU）
SELECT 
    DATE(log_time) as log_date,
    COUNT(DISTINCT user_id) as dau,
    COUNT(*) as total_actions
FROM user_logs
GROUP BY DATE(log_time)
ORDER BY log_date;

-- 用户访问频次分布
SELECT 
    user_id,
    COUNT(*) as visit_count,
    SUM(duration) as total_duration,
    AVG(duration) as avg_duration
FROM user_logs
GROUP BY user_id
ORDER BY visit_count DESC;

-- 用户活跃度分级
SELECT 
    CASE 
        WHEN visit_count >= 10 THEN '高活跃'
        WHEN visit_count >= 5 THEN '中活跃'
        ELSE '低活跃'
    END as activity_level,
    COUNT(*) as user_count,
    AVG(visit_count) as avg_visits,
    AVG(total_duration) as avg_duration
FROM (
    SELECT 
        user_id,
        COUNT(*) as visit_count,
        SUM(duration) as total_duration
    FROM user_logs
    GROUP BY user_id
) t
GROUP BY 
    CASE 
        WHEN visit_count >= 10 THEN '高活跃'
        WHEN visit_count >= 5 THEN '中活跃'
        ELSE '低活跃'
    END;
```

### 2. 行为类型分析
```sql
-- 行为类型统计
SELECT 
    action_type,
    COUNT(*) as action_count,
    COUNT(DISTINCT user_id) as user_count,
    AVG(duration) as avg_duration,
    SUM(duration) as total_duration
FROM user_logs
GROUP BY action_type
ORDER BY action_count DESC;

-- 页面访问统计
SELECT 
    page_url,
    COUNT(*) as page_views,
    COUNT(DISTINCT user_id) as unique_visitors,
    AVG(duration) as avg_duration
FROM user_logs
WHERE action_type = 'page_view'
GROUP BY page_url
ORDER BY page_views DESC;
```

### 3. 用户行为路径分析
```sql
-- 用户访问路径（使用窗口函数）
SELECT 
    user_id,
    log_time,
    page_url,
    action_type,
    ROW_NUMBER() OVER (PARTITION BY user_id, DATE(log_time) ORDER BY log_time) as step,
    LAG(page_url, 1) OVER (PARTITION BY user_id, DATE(log_time) ORDER BY log_time) as prev_page
FROM user_logs
WHERE action_type = 'page_view'
ORDER BY user_id, log_time;

-- 页面流转分析
SELECT 
    prev_page,
    page_url as current_page,
    COUNT(*) as transition_count
FROM (
    SELECT 
        user_id,
        page_url,
        LAG(page_url, 1) OVER (PARTITION BY user_id, DATE(log_time) ORDER BY log_time) as prev_page
    FROM user_logs
    WHERE action_type = 'page_view'
) t
WHERE prev_page IS NOT NULL
GROUP BY prev_page, page_url
ORDER BY transition_count DESC;
```

### 4. 用户画像分析
```sql
-- 用户行为与用户信息关联
SELECT 
    u.gender,
    u.vip_level,
    COUNT(DISTINCT l.user_id) as user_count,
    COUNT(*) as total_actions,
    AVG(l.duration) as avg_duration,
    SUM(l.duration) as total_duration
FROM user_logs l
JOIN users u ON l.user_id = u.user_id
GROUP BY u.gender, u.vip_level
ORDER BY u.vip_level, u.gender;

-- 城市用户行为分析
SELECT 
    u.city,
    COUNT(DISTINCT u.user_id) as user_count,
    COUNT(DISTINCT l.user_id) as active_user_count,
    COUNT(*) as total_actions,
    AVG(l.duration) as avg_duration
FROM users u
LEFT JOIN user_logs l ON u.user_id = l.user_id
GROUP BY u.city
ORDER BY active_user_count DESC;

-- 年龄段行为分析
SELECT 
    CASE 
        WHEN u.age < 25 THEN '25岁以下'
        WHEN u.age < 30 THEN '25-30岁'
        WHEN u.age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END as age_group,
    COUNT(DISTINCT l.user_id) as active_user_count,
    COUNT(*) as total_actions,
    AVG(l.duration) as avg_duration
FROM user_logs l
JOIN users u ON l.user_id = u.user_id
GROUP BY 
    CASE 
        WHEN u.age < 25 THEN '25岁以下'
        WHEN u.age < 30 THEN '25-30岁'
        WHEN u.age < 35 THEN '30-35岁'
        ELSE '35岁以上'
    END;
```

### 5. 转化漏斗分析
```sql
-- 页面转化漏斗
SELECT 
    page_url,
    COUNT(DISTINCT user_id) as visitors,
    COUNT(*) as page_views
FROM user_logs
WHERE action_type = 'page_view'
GROUP BY page_url
ORDER BY 
    CASE page_url
        WHEN '/home' THEN 1
        WHEN '/products' THEN 2
        WHEN '/cart' THEN 3
        ELSE 4
    END;

-- 行为转化率
SELECT 
    '首页访问' as step,
    COUNT(DISTINCT CASE WHEN page_url = '/home' THEN user_id END) as count
FROM user_logs
WHERE action_type = 'page_view'
UNION ALL
SELECT 
    '产品页访问' as step,
    COUNT(DISTINCT CASE WHEN page_url = '/products' THEN user_id END) as count
FROM user_logs
WHERE action_type = 'page_view'
UNION ALL
SELECT 
    '购物车访问' as step,
    COUNT(DISTINCT CASE WHEN page_url = '/cart' THEN user_id END) as count
FROM user_logs
WHERE action_type = 'page_view'
UNION ALL
SELECT 
    '点击购买' as step,
    COUNT(DISTINCT CASE WHEN action_type = 'click' AND page_url = 'button_buy' THEN user_id END) as count
FROM user_logs
UNION ALL
SELECT 
    '点击结账' as step,
    COUNT(DISTINCT CASE WHEN action_type = 'click' AND page_url = 'button_checkout' THEN user_id END) as count
FROM user_logs;
```

### 6. 时间维度分析
```sql
-- 小时访问分布
SELECT 
    HOUR(log_time) as hour,
    COUNT(*) as action_count,
    COUNT(DISTINCT user_id) as active_users,
    AVG(duration) as avg_duration
FROM user_logs
GROUP BY HOUR(log_time)
ORDER BY hour;

-- 工作日 vs 周末分析
SELECT 
    CASE 
        WHEN DAYOFWEEK(log_time) IN (1, 7) THEN '周末'
        ELSE '工作日'
    END as day_type,
    COUNT(*) as action_count,
    COUNT(DISTINCT user_id) as active_users,
    AVG(duration) as avg_duration
FROM user_logs
GROUP BY 
    CASE 
        WHEN DAYOFWEEK(log_time) IN (1, 7) THEN '周末'
        ELSE '工作日'
    END;
```

## 预期结果

### 每日活跃用户（DAU）
```
log_date   | dau | total_actions
-----------|-----|---------------
2024-01-15 | 3   | 10
2024-01-16 | 3   | 7
2024-01-17 | 3   | 7
```

### 行为类型统计
```
action_type | action_count | user_count | avg_duration | total_duration
------------|--------------|------------|--------------|---------------
page_view   | 18           | 4          | 18.33        | 330
click       | 6            | 4          | 4.33         | 26
```

### 页面访问统计
```
page_url    | page_views | unique_visitors | avg_duration
------------|------------|-----------------|-------------
/products   | 8          | 4               | 25.25
/home       | 6          | 4               | 10.50
/cart       | 4          | 3               | 16.75
```
