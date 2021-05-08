## 开发进度
### 2021年05月08日
#### 测试了商品ID的数据情况
不容乐观，只通过商品列表api获得的数据结果，远没有orders里面的丰富，所以还是得以orders为主

![](http://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/pasteimageintomarkdown/2021-05-08/66318202450289.png?Expires=4774010692&OSSAccessKeyId=LTAI4G8kArj75ch3irL8mUUJ&Signature=NaztxS3FZV3WWnSsRg7qYJDprsw%3D)


### 2021年05月07日
#### 完成`raw_data`模块的模板化
基于`db_query`母函数，为`raw_data`所有子功能都提供了稳健的服务端`query`功能，并配合前端，基于路由实现自动匹配。


## 开发记录
### 真是妙极了的bug，关于变量重命名， 2021年05月08日21:27:33
之前为了控制就外部变量被屏蔽的提示，直接将函数的`cookie`变量重命名，当时IDE就慢极了，好家伙，原来是把其他变量也重命名了。。这直接导致我的数据库用户更新失效，产生了完全难以估摸的bug。。

![](http://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/pasteimageintomarkdown/2021-05-08/49364871627935.png?Expires=4774080467&OSSAccessKeyId=LTAI4G8kArj75ch3irL8mUUJ&Signature=iccTnCMeC94AfY%2FEDyxiNN7xjYQ%3D)

### 解决`docstring`"没有效果"的问题，2021年05月08日10:04:39
参考：
- [python - Pycharm does not auto-create documentation stubs - Stack Overflow](https://stackoverflow.com/questions/36292999/pycharm-does-not-auto-create-documentation-stubs)

选择`Epytext`：
![](http://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/pasteimageintomarkdown/2021-05-08/8427489537226.png?Expires=4774039530&OSSAccessKeyId=LTAI4G8kArj75ch3irL8mUUJ&Signature=HNZRuco1lMNTJNI6ss2GJOsPxWg%3D)

之前搞`.txt`问题的时候把这里动过了。。。

### 被`axios`倒逼修改`fastapi`的参数，哈哈哈
由于`axios`里的`put`默认是用`data`属性，这导致我的`update_user`接口所依赖的几个子函数都要改成`Form`输入，而非`Query`，哈哈哈，无语

### 关于`cors`问题
参考：
- [CORS (Cross-Origin Resource Sharing) - FastAPI](https://fastapi.tiangolo.com/tutorial/cors/)

不可以直接用`*`去匹配任意`origin`，简单做法如下：
```python
ALLOW_ORIGINS = [
    "http://localhost:3000",
    "http://nanchuan.site:3000"
]
```

### 关于subprocess 运行 SIGNAL 6 的问题

原本是使用以下代码，在`python`里运行`nodejs`的算法文件的：

```python
import subprocess
SCRIPT_PATH = 'xxx'
cookie = 'xxx'

anti_content = subprocess.check_output(['node', SCRIPT_PATH, cookie], encoding='utf-8').strip()
```

搜索了一番，好像都是说内存不足的问题，那没办法， 我这2G的小机子，运行下来就剩两三百兆，如图（这还是在关闭了`mysql`之后的，不然只剩几十兆……）：

![](http://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/pasteimageintomarkdown/2021-05-06/45966396673178.png?Expires=4773903033&OSSAccessKeyId=LTAI4G8kArj75ch3irL8mUUJ&Signature=NEE78sHxBuLNtSJeaKlMXglXit4%3D)


后来又不不抱希望地尝试了`stackoverflow`上的另一种调用方式：
```python
import subprocess
SCRIPT_PATH = 'xxx'
cookie = 'xxx'

anti_content = subprocess.Popen(['node', SCRIPT_PATH, cookie], stdout=subprocess.PIPE, encoding='utf-8').stdout.read().strip()
```

结果竟然可以！

哈哈哈！

**子进程yyds！**

### 关于pm2始终不记录python程序输出的问题
参考：
- [python - PM2 doesn't log Python3 print statements - Stack Overflow](https://stackoverflow.com/questions/37959217/pm2-doesnt-log-python3-print-statements)

解决办法一：
在`pm2`的`json`文件中，加上`  "interpreter_args": "-u"`。

解决办法二：
`python`脚本上，添加`-u`参数。 

### 醉了，拼多多的api设计……
![](http://mark-vue-oss.oss-cn-hangzhou.aliyuncs.com/pasteimageintomarkdown/2021-05-06/11617979774528.png?Expires=4773868684&OSSAccessKeyId=LTAI4G8kArj75ch3irL8mUUJ&Signature=uMcOMbpzW8h2xZ9yd24CSi69bMk%3D)
