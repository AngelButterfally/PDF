### V0.1.1:

确认实现 pdf 文字提取，转为 txt，关键字检索和信息提取，可整合为 excel

### V0.1.2:

对功能进行了分割整合

### V0.1.3:

将文件进行了分类归档，修改了引入地址
添加了 G120C 变频器故障手册的 scan 和 search 功能 py 文件

### V1.3

- 添加了搜索框索引条目功能，根据不同设备型号显示不同的故障码条目索引。
- 完善历史记录功能模块内容
  - 增加鼠标右键菜单，能够对某一条目进行删除
  - 对于没有搜索结果的故障码，不将其显示在历史记录中

### V1.4
- 添加软件重启功能。
- 添加启动系统虚拟键盘功能
- 完善故障码输入框
  - 现在可以在故障码输入框中输入小写字母，程序可以自动将其转为大写字母
- 完善历史记录功能模块内容
  - 鼠标右键菜单添加选项，一键删除全部历史记录
- 添加软件启动配置文件自检功能
  - 软件启动，若配置文件夹TXT中未发现相关故障.txt文件，则进行提示，并将软件中对应的功能模块变为不可选择状态
  - 软件启动时将自动选择存在的故障.txt文件
  - 若三种故障.txt文件均不存在，则软件报错

### V1.5
- 菜单栏添加‘关于QT’
- 完善搜索框功能
  - 当输入故障码小于6个字符并点击回车时，自动匹配提示框中第一个最相关的故障码。
- 完善任务栏图标的显示功能
- 将所有相对路径替换为自动生成的绝对路径，使软件在不同安装路径下能够运行
- 新增多线程模块，将扫描PDF功能转入子线程中进行，主界面仍可进行操作。
  - 子线程继承自Qobject类而不是QThread类
  - 实现了主线程与子线程之间的双向通信
###### TODO 


## 环境配置
pip install PyQt5 -i https://pypi.douban.com/simple
pip install PyQt5-tools -i https://pypi.douban.com/simple
pip3 install PyInstaller -i https://pyp.douban.com/simple
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

## 软件打包
pyinstaller --onefile app.py
pyinstaller --windowed --icon=hand.ico app.py
pyinstaller --windowed --icon=hand.ico --add-data="hand.ico;." app.py
InstallForge

