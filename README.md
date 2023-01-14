# KK-CODE

[![python版本](https://img.shields.io/badge/python-3.7+-brightgreen.svg?style=flat)]()
[![版本号](https://img.shields.io/badge/release-v1.0.0-brightgreen.svg?style=flat)]()
[![license](https://img.shields.io/badge/license-MulanPSL2.0-brightgreen.svg?style=flat)]()
[![license](https://img.shields.io/badge/os-win-brightgreen.svg?style=flat)]()
[![作者](https://img.shields.io/badge/Author-陌北v1-orange.svg?style=flat)]()
[![star](https://gitee.com/zzwhe/kk_code/badge/star.svg?theme=dark)]()
[![fork](https://gitee.com/zzwhe/kk_code/badge/fork.svg?theme=dark)]()

程序员命令太多记不住怎么办，快来试试`kk-code`命令快捷输入工具吧。命令、代码片段都能帮你记住。

用python开发的代码片段快捷输入工具。
开发环境:python3.7


#### 运行：
下载发行版，解压后运行`kk.exe`

![image-20230113094605172](image-20230113094605172.png)



#### 使用：

按两次`Ctrl+Alt`键，会弹出快捷输入框，输入自定义的`快捷短语`。`回车`或者选择需要复制的快捷短语就会自动复制到剪贴板上面。

`ESC`退出，`回车`隐藏。

**使用前别忘记先添加命令**




![image-20230113100333302](image-20230113100333302.png)

#### 添加编辑：
输入`:edit`会弹出编辑窗口：

![image-20230113095313083](image-20230113095313083.png)

编辑窗口：

![image-20230113095425867](image-20230113095425867.png)

添加：

![image-20230113095806716](image-20230113095806716.png)





#### 创建新的空数据库：

`data.db`为数据库文件。如果需要重新生成数据库文件可以用`kk.exe --create_ok`命令创建新的空数据库`data_new.db`然后重命名为`data.db`就可以用了。