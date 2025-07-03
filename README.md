# my-awesome-device-llm-project

本项目旨在构造一个手机、平台等端侧设备本地运行多模态大模型能力的生态，包括运行环境、端侧大模型和前后端APP等，并追踪当前端侧大模型开源模型，尽微薄之力为端侧大模型应用提供一些开源实现参考。

## 环境搭建（Android）

**1. 安装termux**

直接运行安装程序termux-arm64-v8a.apk，按照系统提示直接安装即可，安装中可能由于本安装包不是官网应用市场中的，可能会有安全提示，直接允许即可。

termux安装包去官网下载或[网盘下载，提取码：enhj](https://pan.baidu.com/s/1pdcgpmOvTB3nd5I11PIIiA)

**2. 打开APP**

termux安装好后，直接打开APP，会出现命令行工具，接下来就可以跟linux一样输入命令操作了。


**3. 安装API工具**

在termux命令行工具中输入命令为：

```bash
pkg install termux-api
```

注：有时候由于网络问题，安装失败，可以多次尝试，如果还不行可以上网查下把pkg的源设为国内镜像

**4. 获取本地存储访问权限**

方便导入和操作文件，在termux命令行工具中输入命令为：

```bash
termux-setup-storage
```

执行命令后，屏幕下方会弹出如下对话框，选择始终允许
![Termux界面](images/termux.png)

**5. 拷贝环境包**

首先将环境包放在手机目录的Download或者其他能访问到的目录，然后执行如下命令，将环境包拷贝到Termux中。环境包下载地址是：[网盘下载，提取码：qhca](https://pan.baidu.com/s/1aTx82w3qtiwjc-nJ_F4aRQ)

```bash
cp storage/Download/termux-backup.tar.gz ~/
```

**6. 直接解压安装**

```bash
tar -xzvf termux-backup.tar.gz -C /data/data/com.termux/files --recursive-unlink --preserve-permissions
```

至此，大模型运行依赖的环境就安装好了

## 模型部署

**1. 获取源代码**

获取本工程源代码，并下载模型文件，放在models中，下载地址是：[网盘下载，提取码：d6rc](https://pan.baidu.com/s/1Tf2d_lZFOoU7wO4x4iWdJQ)

**2. 运行**

将代码放在Termux能访问到的任意一个文件夹即可，进入到代码目录，执行：

```bash
python run.py
```

执行命令后，稍等一会，出现如下界面，表示服务启动成功
![Termux运行](images/run.png)

## API使用说明

马上到来

## APP部署和使用

直接下载APP点击安装即可，下载地址：[网盘下载，提取码：m2a2](https://pan.baidu.com/s/16Fpg4dAIbMiZk0SlndDrHA)

界面如下所示：

![Termux运行](images/app.png)

界面主要功能介绍：

**①对话展示区**

**②语音输入功能按钮，点击后区域③变成语音操控，按住语音操控即可开始实时语音录入**

**③文字输入区，在此处输入你想要问的问题**

**④清空按钮，点击会清空当前聊天记录，新建一个对话**

**⑤点击会出现⑦⑧功能展示区**

**⑥深度思考或标准模式切换功能**

**⑦拍照问答，待开发上线**

## 开源端侧大模型跟踪和评测对比

马上到来
