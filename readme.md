## 开发记录

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
