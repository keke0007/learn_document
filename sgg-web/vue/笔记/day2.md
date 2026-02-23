一、登录业务接口替换!!!替换为真实项目接口
http://sph-h5-api.atguigu.cn
项目在线的API
http://39.98.123.211:8510/swagger-ui.html
http://39.98.123.211:8170/swagger-ui.html


1.1替换登录、获取用户信息、退出登录接口
https://cn.vitejs.dev/config/server-options.html#server-proxy
---书写登录接口
---配置代理跨域
---配置文件发生变化-重启
server: {
      proxy: {
        '/app-dev': {
          target: 'http://sph-h5-api.atguigu.cn',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/app-dev/, ''),
        },
      }
}


二、品牌管理模块 Element UI 插件

---静态的搭建
table：
    border:可以让表格竖着方向有边框
column
    label:顶部标题
    width:列宽度
    align:center 文字对齐方式
pagination
 layout 调整子组件位置布局

---获取品牌数据并且进行渲染

---分页展示数据的业务

