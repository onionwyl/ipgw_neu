import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QGridLayout, QLabel, QLineEdit, QCheckBox,
                             qApp, QMessageBox, QDesktopWidget)
from PyQt5.Qt import QSystemTrayIcon, QMenu, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ipgw_crawler import IPGW_Crawler

class IPGW_UI(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.ipgw = IPGW_Crawler()
        self.initUI()
        self.login = loginWidget(self.loginCallback)
        self.login.show()
    def initUI(self):
        # 右键菜单
        trayIconMenu = QMenu()
        bindAction = trayIconMenu.addAction('绑定帐号')
        subMenu1 = trayIconMenu.addMenu('登录')
        self.loginComAction = subMenu1.addAction('电脑版登录')
        loginMobAction = subMenu1.addAction('手机版登录')
        subMenu2 = trayIconMenu.addMenu('退出登录')
        logoutComAction = subMenu2.addAction('退出电脑登录')
        logoutMobAction = subMenu2.addAction('退出手机登录')
        logoutAllAction = subMenu2.addAction('退出全部登录')
        infoSearchAction = trayIconMenu.addAction('帐户信息查询')
        helpAction = trayIconMenu.addAction('帮助')
        aboutAction = trayIconMenu.addAction('关于')
        quitAction = trayIconMenu.addAction('退出')
        # 绑定Action
        bindAction.triggered.connect(self.bindUser)
        self.loginComAction.triggered.connect(lambda :self.login(1))
        loginMobAction.triggered.connect(lambda :self.login(2))
        logoutComAction.triggered.connect(lambda :self.logout(1))
        logoutMobAction.triggered.connect(lambda :self.logout(2))
        logoutAllAction.triggered.connect(lambda :self.logout(3))
        helpAction.triggered.connect(self.help)
        aboutAction.triggered.connect(self.about)
        quitAction.triggered.connect(qApp.quit)

        icon = QIcon('icon.png')
        self.setIcon(icon)
        self.setContextMenu(trayIconMenu)
        self.setToolTip('IPGW助手')
        self.show()

    def bindUser(self):
        self.login.show()

    def loginCallback(self, username, password, auto, remember):
        req = self.ipgw.login(username, password)
        if req == 1:
            QMessageBox.warning(self.login, 'Warning', '用户名不存在!')
        elif req == 2:
            QMessageBox.warning(self.login, 'Warning', '用户密码错误!')
        else:
            print(self.ipgw.query())
            used_flux, used_time, user_balance, ip_addr = self.ipgw.query()
            message = '登录成功！\n'
            message = message + "已用流量：%.2fM\n" % used_flux
            (hour, minute, second) = used_time
            message = message + "已用时长：%d:%02d:%02d\n" % (hour, minute, second)
            message = message + "帐户余额：￥" + user_balance + "\n"
            message = message + "IP地址：" + ip_addr + "\n"
            QMessageBox.about(self.login, 'Success', message)
            self.login.close()

    def login(self, mode):
        self.trayIcon.showMessage('登录','登录成功')
        self.loginComAction.setIcon(QIcon('confirm.png'))

    def logout(self, mode):
        pass

    def help(self):
        pass

    def about(self):
        pass

class loginWidget(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.initUI()

    def initUI(self):
        imageLabel = QLabel()
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.rememberCheck = QCheckBox()
        self.autoLoginCheck = QCheckBox()
        self.loginButton = QPushButton()

        self.loginButton.setFixedHeight(30)
        self.usernameEdit.setFixedWidth(160)
        self.usernameEdit.setFixedHeight(25)
        self.passwordEdit.setFixedHeight(25)
        pixmap = QPixmap('icon.png')
        icon = QIcon('icon.png')
        imageLabel.setFixedSize(90, 90)
        imageLabel.setPixmap(pixmap)
        imageLabel.setScaledContents(True)
        self.usernameEdit.setPlaceholderText("用户名")
        self.passwordEdit.setPlaceholderText("密码")
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.rememberCheck.setText("记住密码")
        self.autoLoginCheck.setText("自动登录")
        self.loginButton.setText("登录")


        grid = QGridLayout()
        grid.addWidget(imageLabel, 0, 0, 3, 1)
        grid.addWidget(self.usernameEdit, 0, 1, 1, 2)
        grid.addWidget(self.passwordEdit, 1, 1, 1, 2)
        grid.addWidget(self.rememberCheck, 2, 1, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addWidget(self.autoLoginCheck, 2, 2, 1, 1, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self.loginButton, 3, 1, 1, 2)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)
        self.setLayout(grid)
        self.setWindowIcon(icon)
        self.setWindowTitle('登录')
        self.resize(160, 120)
        self.center()

        self.loginButton.clicked.connect(self.handleLogin)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handleLogin(self):
        if not self.usernameEdit.isModified() or not self.passwordEdit.isModified():
            QMessageBox.warning(self, 'Warning', "请填写用户名与密码")
            return
        self.callback(self.usernameEdit.text(), self.passwordEdit.text(), self.autoLoginCheck.isChecked(), self.rememberCheck.isChecked())

    def closeEvent(self, event):
        print("close")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = IPGW_UI()
    sys.exit(app.exec_())

