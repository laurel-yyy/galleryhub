# 非正式readme 

## Start
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

