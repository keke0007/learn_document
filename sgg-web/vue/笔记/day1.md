一、简单介绍
上课的时候:整理面试题
贾成豪  哈尔滨   jiachenghao0330 微信

二、后台管理系统特点

1:一般是没有注册只有登录[员工的账号与密码,boss:超级管理员]
2:项目结构一般左右结构
3:增删改查的业务
4:用户访问权限[菜单、按钮]*******



2.1后台管理系统项目模版的介绍?

vue2后台管理系统项目模版:
https://gitee.com/panjiachen/vue-admin-template.git

vue3后台管理系统项目模版:
https://gitee.com/jch1011/vue3_admin_project.git
https://www.bilibili.com/video/BV1Xh411V7b5/?spm_id_from=333.337.search-card.all.click







三、模版源码的阅读?

3.1配置项目路由-商品管理模块



3.2登录业务查看?
模板中没有登录、获取用户信息、退出登录请求
---模版中这些接口替换成你们公司真的接口！！！


form组件表单表单校验流程:
1:form组件添加model属性->告诉form组件表单的数据收集在那个对象的身上
2:form组件添加rules属性->书写表单校验的规则
3:el-form-item表单相组件添加prop属性,属性值即为校验字段的名字



