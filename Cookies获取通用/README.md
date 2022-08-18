# web 获取cookie
## 输出为cookies.json文件，会自动下载
## pyinstaller 编译静态文件
### 先执行一遍，会生成 .spec 的配置文件
### 修改配置文件里面Analysis的datas
例如：datas=[('./static','static'),('./templates','templates')],
windows 是双斜杠
### 最后执行 pyinstaller -F xxx.spec