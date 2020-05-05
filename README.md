## 介绍
这是一个自动打卡的flask小程序,基于curl命令

[这里记录了开发的思路和一些问题](http://harumonia.top/index.php/archives/225/)

## 运行
1. 于文件夹下添加一个secure.py文件,录入redis内容

    ```python
    import redis
    
    r = redis.Redis(host='****', port=6379, decode_responses=True)
    ```
2. flask run


## 使用方法
### S1 获取curl命令

进入浏览器,进入开发者界面,然后进行一次成功的打卡交互.

这时可以在开发者界面的"网络(network)"中发现一个post交互,进行如图的操作(Copy as cURL),就可以得到curl命令

curl例子: curl 'https://pdc.njucm.edu.cn/pdc/formDesignApi/dataFormSave?wid=****&userId=****' -H 'User-Agent: Mozill...

![图片.png](https://i.loli.net/2020/05/04/2aFN3uyjLB6TizK.png)

### S2 录入

将得到的cURL录入到网页的表单中

第二个选项是选择打卡的时间,if输入3,就是每天3点进行打卡.

__默认一次录入一条,如果一天中需要多次打卡的,多次录入即可__

### S3 检查
第一次录入之后,在到点时检查一下是否正确执行了,over

