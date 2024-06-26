import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import QCursor
from ui import Ui_Form
import sqlite3
import win32con
import win32clipboard as w
import keyboard
import time
import argparse
from add_ui import Ui_AddForm

class MainWindow(QtWidgets.QMainWindow,Ui_Form):
    conn = sqlite3.connect("data.db")
    tmp_list = []
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(Qt.FramelessWindowHint) #隐藏窗口标题
        # self.setAttribute(Qt.WA_TranslucentBackground) #背景透明
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)
        
        self.setStyleSheet('#Form{background-color:#3c3c3c;}')
        self.lineEdit.setStyleSheet("border:0px;background-color:#666;color:#e0e0e0;font-size:22px;font-family:'Microsoft YaHei UI';")
        self.lineEdit.setFocus()
        self.listWidget.setStyleSheet('#listWidget{border:0px;background-color:#3c3c3c;}')
        self.listWidget.setGeometry(QtCore.QRect(8, 8+51, 734, 272))
        self.resize(750, 16+51)

        # 获得屏幕坐标系
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        # 获得窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width())/2
        newTop = 360
        self.move(newLeft, newTop)
        
        self.lineEdit.textChanged.connect(self.on_edit_textChanged)#文本框输入事件
        self.lineEdit.returnPressed.connect(self.lineEdit_function)#文本框回车事件
        self.listWidget.itemActivated.connect(self.itemok)

        self.add_win = AddWindow()
        self.edit_win = EditWindow()
        self.edit_win._signal.connect(self.receivedmsg)

        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.listWidget.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QtWidgets.QMenu(self)
        self.medit = self.contextMenu.addAction('编辑')
        self.mdel = self.contextMenu.addAction('删除')
        #事件绑定
        self.medit.triggered.connect(self.EditEvent)
        self.mdel.triggered.connect(self.DelEvent)
    def showMenu(self):
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
    def EditEvent(self):
        index = self.listWidget.currentIndex().row()
        id = self.tmp_list[index][0]
        self.edit_win.setID(id)
        self.edit_win.show()
    def DelEvent(self):
        index = self.listWidget.currentIndex().row()
        id = self.tmp_list[index][0]
        delete(id)
        self.mylistLoad()

    def receivedmsg(self,msg):
        print("收到消息内容：",msg)
        self.mylistLoad()

    #输入内容后渲染列表
    def mylistLoad(self):
        self.tmp_list = []
        self.listWidget.clear()
        str1 = self.lineEdit.text()
        if str1:
            self.tmp_list = self.search(str1)
            len_list = len(self.tmp_list)
            win_height = len_list * 67
            if win_height >= 612:
                win_height = 612
            self.resize(750, 16+51+win_height)
            self.listWidget.setGeometry(QtCore.QRect(8, 8+51, 734, win_height))
            for a in self.tmp_list:
                if a[3]:
                    tmp_b = a[3]
                else:
                    tmp_b = a[4]
                widget = self.get_item_wight(a[2] + " | " +a[1],tmp_b)
                item = QtWidgets.QListWidgetItem()
                item.setSizeHint(QtCore.QSize(1, 65))
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item,widget)
        else:
            self.listWidget.setGeometry(QtCore.QRect(8, 8+51, 734, 272))
            self.resize(750, 16+51)



    #item点击事件
    def itemok(self):
        index = self.listWidget.currentIndex().row()
        self.inputtxt(self.tmp_list[index][4])
        self.hide_ok()     


    #回车默认选择第一个
    def lineEdit_function(self):
        if self.tmp_list:
            self.inputtxt(self.tmp_list[0][4])
            self.hide_ok()
        else:
            tmp_str = self.lineEdit.text()
            if tmp_str==":add":
                # self.list_win.show()
                self.add_win.show()
                self.lineEdit.setText("")
            else:
                self.hide_ok()


    #文件框输入事件
    def on_edit_textChanged(self):
        self.mylistLoad()

    #写入剪贴板
    def inputtxt(self,string):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT,string)
        w.CloseClipboard()


    #隐藏窗口
    def hide_ok(self):
        self.lineEdit.setText("")
        self.resize(750, 16+51)
        print("隐藏窗口")
        self.hide()
        self.abc()#监听键盘

    #开始监听键盘
    def abc(self):
        if keyboard.wait(hotkey='ctrl+alt') == None:
            a = time.time()
            if keyboard.wait(hotkey='ctrl+alt') == None:
                b = time.time()
                if b-a < 0.5:
                    print("显示窗口")
                    self.show()
                    self.lineEdit.setFocus()#获取焦点
                else:
                    print("继续监听")
                    self.abc()

    # def resizeEvent(self, event):
    #     h = event.size().height()
    #     print("窗口高度：",h)
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ismoving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.ismoving:
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        self.ismoving = False


    def get_item_wight(self,title,describe):
        wight = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        label_title = QtWidgets.QLabel(title)
        label_title.setStyleSheet("color:#e0e0e0;font-size:16px;font-family:'Microsoft YaHei UI';")
        layout.addRow(label_title)
        label_describe = QtWidgets.QLabel(describe)
        label_describe.setStyleSheet("color:#e0e0e0;font-size:14px;font-family:'Microsoft YaHei UI';")
        layout.addRow(label_describe)
        wight.setLayout(layout)
        return wight

    #查询
    def search(self,msg):
        c = self.conn.cursor()
        sql = "select * from t1 where keyword like'%{}%' ORDER BY sort desc".format(msg)
        # print(sql)
        cursor = c.execute(sql)
        mlist = []
        for row in cursor:
            mlist.append(row)
        return mlist


#创建数据库
def create_ok():
    conn = sqlite3.connect("data_new.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS t1(id INTEGER PRIMARY KEY,keyword TEXT,title TEXT,example TEXT,note TEXT,sort INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()
    print("数据库创建成功！")


#删除
def delete(id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    sql = "DELETE from t1 where id={}".format(id)
    c.execute(sql)
    conn.commit()
    conn.close()
    print("删除成功！")

#获取全部记录方法
def select_all():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    cursor = c.execute("select * from t1")
    li = []
    for row in cursor:
        li.append([row[0],row[1],row[2]])
        print(row[0],row[1],row[2])
    conn.close()

#查找
def select(str1):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    sql = "select * from t1 where keyword like'%{}%'".format(str1)
    cursor = c.execute(sql)
    for row in cursor:
        print(row[0],row[1],row[2])
    conn.close()


#添加界面
class AddWindow(QtWidgets.QMainWindow,Ui_AddForm):
    def __init__(self,parent=None):
        super(AddWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ok_btn)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)

    #添加数据按钮
    def ok_btn(self):
        keyword_text = self.lineEdit_keyword.text()
        title_text = self.lineEdit_title.text()
        example_text = self.lineEdit_example.text()
        note_text = self.textEdit_Note.toPlainText()

        self.insert_ok(keyword_text,title_text,example_text,note_text)
        self.lineEdit_keyword.setText("")
        self.lineEdit_title.setText("")
        self.lineEdit_example.setText("")
        self.textEdit_Note.setText("")
    

    #添加数据方法
    def insert_ok(self,keyword,title,example,note):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("INSERT INTO t1 (keyword,title,example,note) VALUES (?,?,?,?)",(keyword,title,example,note))
        conn.commit()
        conn.close()
        print("数据写入成功！")



#修改界面
class EditWindow(QtWidgets.QMainWindow,Ui_AddForm):
    id = ''
    _signal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(EditWindow, self).__init__(parent)
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AddForm", "修改"))
        self.pushButton.setText(_translate("AddForm", "修改"))
        self.pushButton.clicked.connect(self.ok_btn)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)
        
    def setID(self,id):
        self.id = id
        self.select_one(id)
    
    #添加数据按钮
    def ok_btn(self):
        keyword_text = self.lineEdit_keyword.text()
        title_text = self.lineEdit_title.text()
        example_text = self.lineEdit_example.text()
        note_text = self.textEdit_Note.toPlainText()
        self.update(keyword_text,title_text,example_text,note_text)
        self.lineEdit_keyword.setText("")
        self.lineEdit_title.setText("")
        self.lineEdit_example.setText("")
        self.textEdit_Note.setText("")
        self._signal.emit("向主窗口发送消息")
        self.close()
        

    #修改方法
    def update(self,keyword,title,example,note):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("UPDATE t1 SET keyword=?,title=?,example=?,note=? WHERE id=?",(keyword,title,example,note,self.id))
        conn.commit()
        conn.close()
        print("修改成功！")
    
    #获取第一条记录
    def select_one(self,id):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            sql = "select * from t1 where id={}".format(id)
            print(sql)
            c.execute(sql)
            res = c.fetchone()
            print(res)
            self.lineEdit_keyword.setText(res[1])
            self.lineEdit_title.setText(res[2])
            self.lineEdit_example.setText(res[3])
            self.textEdit_Note.setText(res[4])
        except:
            print("修改失败，请检查参数是否错误。")
            sys.exit(0)
        conn.commit()
        conn.close()


parser = argparse.ArgumentParser(description='参数说明')
parser.add_argument('--list',help='获取全部记录',action="store_true")
parser.add_argument('--create_ok', help="创建数据库",action="store_true")
args = parser.parse_args()
# print(args)

if __name__ == '__main__':
    #创建数据库
    if args.create_ok:
        create_ok()
    #查找
    elif args.list:
        select_all()
    else:
        app = QtWidgets.QApplication(sys.argv)
        main = MainWindow()
        main.show()
        sys.exit(app.exec_())