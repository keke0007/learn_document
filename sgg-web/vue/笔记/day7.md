一、完成SPU管理模块
1.1完成添加SPU的业务?


二、完成添加SKU的业务?

2.1 静态 + 数据的渲染

2.2收集新增SKU的数据发请求
{
  "category3Id":"",//三级分类的ID
  "spuId":"",//SPU的ID
  "tmId":"",//SPU归属于哪一个品牌

  "skuName": "",//SKU名字
  "price":"",//SKU价格
  "weight": "",//SKU重量
  "skuDesc": "",//SKU商品的描述
  "skuDefaultImg": "", //默认图片的地址

  "skuAttrValueList": [ //收集平台属性的数据
    {
      "attrId":"",//平台属性的ID
      "valueId":"",//平台属性值的ID
    }
  ],
 "skuSaleAttrValueList": [//收集销售属性
    {

      "saleAttrId":"",//销售属性的ID

      "saleAttrValueId":"",//属性值的ID
    }
  ],

}