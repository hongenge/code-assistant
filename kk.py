import sys
import os
from contextlib import contextmanager
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from ui import Ui_Form
import sqlite3
import win32con
import win32clipboard as w
from pynput import keyboard as pynput_keyboard
from pynput.keyboard import Controller, Key
from add_ui import Ui_AddForm
import html
from PyQt5.QtNetwork import QLocalServer, QLocalSocket


DB_NAME = "data.db"

# =========================
# 数据库连接统一方法
# =========================
@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    tmp_list = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 添加 Ctrl+K 快捷键
        self.focus_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+K'), self)
        self.focus_shortcut.activated.connect(self.focus_search_bar)


        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWindowFlags(Qt.FramelessWindowHint)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)

        self.setStyleSheet('#Form{background-color:#3c3c3c;}')
        self.lineEdit.setStyleSheet("border:0px;background-color:#666;color:#e0e0e0;font-size:22px;font-family:'Microsoft YaHei UI';")
        self.listWidget.setStyleSheet('#listWidget{border:0px;background-color:#3c3c3c;}')
        self.listWidget.setGeometry(QtCore.QRect(8, 8+51, 734, 272))
        self.resize(750, 16+51)
        self.lineEdit.setFocus()

        # 居中
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        newLeft = int((screen.width() - size.width()) / 2)
        newTop = 360
        self.move(newLeft, newTop)

        self.lineEdit.textChanged.connect(self.on_edit_textChanged)
        self.lineEdit.returnPressed.connect(self.lineEdit_function)
        self.listWidget.itemActivated.connect(self.itemok)

        self.add_win = AddWindow()
        self.edit_win = EditWindow()
        self.edit_win._signal.connect(self.receivedmsg)

        # 右键菜单
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QtWidgets.QMenu(self)
        self.medit = self.contextMenu.addAction('编辑')
        self.mdel = self.contextMenu.addAction('删除')
        self.medit.triggered.connect(self.EditEvent)
        self.mdel.triggered.connect(self.DelEvent)

        self.search_timer = QtCore.QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.mylistLoad)

        self.lineEdit.installEventFilter(self)
        self.listWidget.installEventFilter(self)

        # 启动快捷键监听
        self._listener = None
        self.start_hotkey_listener()
        QtWidgets.QApplication.instance().aboutToQuit.connect(self.cleanup)


    def cleanup(self):
        if self._listener:
            try:
                self._listener.stop()
                self._listener = None
                print("热键监听已停止")
            except Exception as e:
                print("停止热键监听失败:", e)


    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # 情况 A: 输入框按 ⬇️
            if watched == self.lineEdit and event.key() == Qt.Key_Down:
                if self.listWidget.count() > 0:
                    self.listWidget.setFocus()
                    self.listWidget.setCurrentRow(0)
                    return True
            
            # 情况 B: 列表按 ⬆️ 且当前已是第一项
            elif watched == self.listWidget and event.key() == Qt.Key_Up:
                if self.listWidget.currentRow() == 0:
                    self.lineEdit.setFocus()
                    # self.lineEdit.selectAll() # 如果需要可以加上全选
                    return True
                    
        return super(MainWindow, self).eventFilter(watched, event)



    def focus_search_bar(self):
        """全选并聚焦输入框"""
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()  # 可选：聚焦时顺便全选，方便直接输入新内容


    # =========================
    # 快捷键监听
    # =========================
    def start_hotkey_listener(self):
        if self._listener:
            return
        def on_activate():
            self.on_hotkey_triggered()

        self._listener = pynput_keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+k': on_activate
        })
        self._listener.start()


    def on_hotkey_triggered(self):
        QtCore.QMetaObject.invokeMethod(
            self,
            "show_window",
            QtCore.Qt.QueuedConnection
        )

    @QtCore.pyqtSlot()
    def show_window(self):
        print("显示窗口")
        self.show()
        self.lineEdit.setFocus()

    def showMenu(self):
        self.contextMenu.exec_(QCursor.pos())

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

    def receivedmsg(self, msg):
        print("收到消息内容：", msg)
        self.mylistLoad()

    def highlight_keyword(self, keyword, search_text):
        if not search_text:
            return html.escape(keyword)

        keyword_escaped = html.escape(keyword)
        search_escaped = html.escape(search_text)

        # 忽略大小写替换
        import re
        pattern = re.compile(re.escape(search_escaped), re.IGNORECASE)

        return pattern.sub(
            lambda m: f"<span style='background-color:#5A5A5A;color:#E0E0E0;font-weight:bold;'>{m.group(0)}</span>",
            keyword_escaped
        )


    # =========================
    # 列表加载
    # =========================
    def mylistLoad(self):
        self.tmp_list = []
        self.listWidget.clear()
        str1 = self.lineEdit.text()

        if str1:
            self.tmp_list = self.search(str1)
            total_height = 0
            max_height = 612

            for a in self.tmp_list:
                highlighted_keyword = self.highlight_keyword(a[1], str1)
                title = f"{html.escape(a[2])}  <span style='color:#9E9E9E;'> {highlighted_keyword}</span>"

                example = a[3]
                is_secret = a[5]
                describe = "******" if is_secret else a[4]
                widget = self.get_item_wight(title, example, describe)

                item = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, widget)

                item_height = widget.sizeHint().height()
                item.setSizeHint(widget.sizeHint())
                total_height += item_height

            win_height = min(total_height, max_height)
            self.resize(750, 16 + 51 + win_height)
            self.listWidget.setGeometry(QtCore.QRect(8, 8 + 51, 734, win_height))
        else:
            self.listWidget.setGeometry(QtCore.QRect(8, 8 + 51, 734, 272))
            self.resize(750, 16 + 51)

    def itemok(self):
        index = self.listWidget.currentIndex().row()
        content = self.tmp_list[index][4]
        self.inputtxt(content)

        modifiers = QtWidgets.QApplication.keyboardModifiers()
        print(f"检测到回车! 当前修饰键代码: {int(modifiers)}")
        self.hide_ok()
        if modifiers == QtCore.Qt.ControlModifier:
            QtCore.QTimer.singleShot(300, self.simulate_paste)


    def lineEdit_function(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        print(f"检测到回车! 当前修饰键代码: {int(modifiers)}")
        if self.tmp_list:
            content = self.tmp_list[0][4]
            self.inputtxt(content)
            self.hide_ok()
            if modifiers == QtCore.Qt.ControlModifier:
                print(">>> 判定成功：你按下了 Ctrl + Enter")
                QtCore.QTimer.singleShot(150, lambda: self.simulate_paste())
        else:
            tmp_str = self.lineEdit.text()
            if tmp_str == ":add":
                self.add_win.show()
                self.lineEdit.setText("")
            else:
                self.hide_ok()


    def simulate_paste(self):
        try:
            kb = Controller()
            with kb.pressed(Key.ctrl):
                kb.press('v')
                kb.release('v')
            print("粘贴成功")
        except Exception as e:
            print(f"粘贴失败: {e}")


    def on_edit_textChanged(self):
        # self.mylistLoad()
        self.search_timer.start(150)

    # =========================
    # 剪贴板
    # =========================
    def inputtxt(self, string):
        try:
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, string)
        finally:
            w.CloseClipboard()

    def hide_ok(self):
        self.lineEdit.setText("")
        self.resize(750, 16+51)
        print("隐藏窗口")
        self.hide()

    # =========================
    # 拖动窗口
    # =========================
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

    def get_item_wight(self, title, example=None, describe=""):
        wight = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()

        label_title = QtWidgets.QLabel(title)
        label_title.setStyleSheet("color:#e0e0e0;font-size:16px;font-family:'Microsoft YaHei UI';")
        layout.addRow(label_title)

        if example:
            label_example = QtWidgets.QLabel(example)
            label_example.setStyleSheet("color:#e0e0e0;font-size:14px;font-family:'Microsoft YaHei UI';")
            layout.addRow(label_example)

        label_describe = QtWidgets.QLabel(describe)
        label_describe.setStyleSheet("color:#e0e0e0;font-size:14px;font-family:'Microsoft YaHei UI';")

        # 限制最大高度（两行文本）
        font_metrics = QtGui.QFontMetrics(label_describe.font())
        max_height = font_metrics.lineSpacing() * 4
        label_describe.setMaximumHeight(max_height)

        label_describe.setToolTip(describe)
        label_describe.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-family: 'Microsoft YaHei UI';
            }
        """)
        layout.addRow(label_describe)
        wight.setLayout(layout)
        return wight

    # =========================
    # 查询（防 SQL 注入）
    # =========================
    def search(self, msg):
        with get_conn() as conn:
            c = conn.cursor()
            sql = "select * from t1 where keyword like ? ORDER BY sort desc"
            cursor = c.execute(sql, ('%' + msg + '%',))
            return cursor.fetchall()


# =========================
# 数据库操作
# =========================
def create_ok():
    if os.path.exists(DB_NAME):
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS t1(
            id INTEGER PRIMARY KEY,
            keyword TEXT,
            title TEXT,
            example TEXT,
            note TEXT,
            is_secret INTEGER DEFAULT 0,
            sort INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("数据库创建成功！")


def delete(id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM t1 WHERE id=?", (id,))
        conn.commit()
    print("删除成功！")


def select(str1):
    with get_conn() as conn:
        c = conn.cursor()
        sql = "select * from t1 where keyword like ?"
        cursor = c.execute(sql, ('%' + str1 + '%',))
        for row in cursor:
            print(row[0], row[1], row[2])


# =========================
# 添加窗口（未改）
# =========================
class AddWindow(QtWidgets.QMainWindow, Ui_AddForm):
    def __init__(self, parent=None):
        super(AddWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ok_btn)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)

    def ok_btn(self):
        keyword_text = self.lineEdit_keyword.text()
        title_text = self.lineEdit_title.text()
        example_text = self.lineEdit_example.text()
        note_text = self.textEdit_Note.toPlainText()
        is_secret = 1 if self.checkBox.isChecked() else 0

        self.insert_ok(keyword_text, title_text, example_text, note_text, is_secret)
        self.lineEdit_keyword.setText("")
        self.lineEdit_title.setText("")
        self.lineEdit_example.setText("")
        self.textEdit_Note.setText("")
        self.checkBox.setChecked(False)


    def insert_ok(self, keyword, title, example, note, is_secret):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO t1 (keyword,title,example,note,is_secret) VALUES (?,?,?,?,?)",
                (keyword, title, example, note, is_secret)
            )
            conn.commit()
        print("数据写入成功！")


# =========================
# 编辑窗口（仅修 SQL）
# =========================
class EditWindow(QtWidgets.QMainWindow, Ui_AddForm):
    id = ''
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(EditWindow, self).__init__(parent)
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AddForm", "修改"))
        self.pushButton.setText(_translate("AddForm", "修改"))
        self.pushButton.clicked.connect(self.ok_btn)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)

    def setID(self, id):
        self.id = id
        self.select_one(id)

    def ok_btn(self):
        keyword_text = self.lineEdit_keyword.text()
        title_text = self.lineEdit_title.text()
        example_text = self.lineEdit_example.text()
        note_text = self.textEdit_Note.toPlainText()
        is_secret = 1 if self.checkBox.isChecked() else 0

        self.update(keyword_text, title_text, example_text, note_text, is_secret)
        self.lineEdit_keyword.setText("")
        self.lineEdit_title.setText("")
        self.lineEdit_example.setText("")
        self.textEdit_Note.setText("")
        self.checkBox.setChecked(False)
        self._signal.emit("向主窗口发送消息")
        self.close()

    def update(self, keyword, title, example, note, is_secret):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE t1 SET keyword=?,title=?,example=?,note=?,is_secret=? WHERE id=?",
                (keyword, title, example, note, is_secret, self.id)
            )
            conn.commit()
        print("修改成功！")

    def select_one(self, id):
        with get_conn() as conn:
            c = conn.cursor()
            try:
                c.execute("select * from t1 where id=?", (id,))
                res = c.fetchone()
                if res:
                    self.lineEdit_keyword.setText(res[1])
                    self.lineEdit_title.setText(res[2])
                    self.lineEdit_example.setText(res[3])
                    self.textEdit_Note.setText(res[4])
                    self.checkBox.setChecked(bool(res[5]))
            except Exception as e:
                print("修改失败:", e)


# 启动
if __name__ == '__main__':
    create_ok()
    app = QtWidgets.QApplication(sys.argv)
    
    # --- 单实例检查开始 ---
    serverName = "MyUniqueAppServerName" # 这里的名字要唯一
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    
    # 如果能连接上，说明已有实例在运行
    if socket.waitForConnected(500):
        print("程序已在运行，激活已有窗口")
        sys.exit(0)
    
    # 如果连接不上，说明是第一个实例，创建一个本地服务器监听
    localServer = QLocalServer()
    localServer.listen(serverName)
    # --- 单实例检查结束 ---

    main = MainWindow()
    
    # 当有新连接（新实例尝试启动）时，激活主窗口
    localServer.newConnection.connect(lambda: (
        main.setWindowState(main.windowState() & ~Qt.WindowMinimized | Qt.WindowActive),
        main.show(),
        main.raise_(),
        main.activateWindow(),
        main.lineEdit.setFocus()
    ))

    main.show()
    sys.exit(app.exec_())