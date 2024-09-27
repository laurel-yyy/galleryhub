# 非正式readme 

## 1. Start
### 1.1 git 
https://docs.github.com/en/get-started/getting-started-with-git/set-up-git 

如果没下就搞一下Git和ssh
（另外感觉网上这种教程比较多

### 1.2 导入环境
我们最好统一环境，不然后面可能有麻烦，可能会直接白干


conda管理环境比较方便，而且老师讲了conda那就用conda把（）

miniconda下载 https://blog.csdn.net/ming12131342/article/details/140233867

要配的环境基本就是conda python3.6 + django

可以直接导入我的

按照下面这个顺序
```
git init
git clone git@github.com:laurel-yyy/galleryhub.git
```
进入有environment.yml的目录，创建一个叫django_env的conda环境
```
conda env create -f environment.yml -n django_env
```
另外如果后面需要导出conda环境可以用
```
conda env export > environment.yml
```
激活环境试一下能不能正常使用
```
conda activate django_env
```
进入有manage.py的目录
```
python manage.py runserver
```
能看到那个绿绿的logo就是成功了。

然后随便创建一个文件，比如去template目录下创建一个kjahsdkj.html，试一下git push能不能正常用

```
git add <文件名>
git commit -m '随便写什么'
git push origin main
```

### 1.3 dependency（持续更新）
    django
    Pillow


## 2. 开发注意事项

### 2.1 格式
尽量PEP-8，不太离谱就行其实（）复杂的函数写注释，和已有example风格尽量统一。

### 2.2 进度
基础功能ylj推荐顺序是
+ 数据库模型
+ 用户管理员登录登出
+ 开发界面
+ 交互功能实现
+ 完善权限
+ 前端美化

后面可以根据个人感觉随便加。

前端写最简单的就可以了，最后再改。但是除了登录注册别的都需要继承base。

加了功能之后要把接口记录在
 [UML共享](https://lucid.app/lucidchart/dc818aea-4b89-472b-a969-b0ae45f560bb/edit?view_items=3cpbG59Okvto&invitationId=inv_ae39550e-00ba-408d-937b-35542d821cc8)
 这里，黑色是设计的彩色是已经完成的。


### 2.3 测试注意事项
现在已经加了几个测试用user。
alice bob root， alice管理员，bob是普通游客，root是超级管理员，密码全是123456

也建好了四个馆，画，tag，作者 example

最好不要动model和setting里面user/auth相关。这个migrate有时候很智障，可能它识别不出来。

翻车了也没关系，db.sqlite删了重新手动创建以上instance就行了。(^_^)

另外，最好做完一小步就检查一下是不是对的，django 不好 debug。 gpt也会胡说八道。
