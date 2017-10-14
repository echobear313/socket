from PyQt5.QtWidgets import *
import sys
import socket
import threading
import global_var
import time
import datetime

class MainDlg(QDialog):
    def __init__(self, parent=None):
        super(MainDlg, self).__init__(parent)
        # self.plainText = QLabel("Test")
        self.inputText = QLineEdit()
        self.sendButton = QPushButton("发送")
        self.disconnectButton = QPushButton("断开链接")
        # self.plainText.setFixedSize(200, 200)
        # self.plainText.setAlignment(Top)
        self.plainText = QTextEdit()
        # self.plainText.setEnabled(False)
        self.plainText.setReadOnly(True)
        self.plainText.setText("给我可爱的宝贝")
        self.content = ""

        '''
        断开发送按钮已经设置了槽
        只需要设置一下文本框的内容成接受的内容+发送的内容
        '''

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.plainText, 0, 0, 8, 9)
        gridLayout.addWidget(self.inputText, 10, 0, 1, 7)
        gridLayout.addWidget(self.sendButton, 10, 7, 1, 1)
        gridLayout.addWidget(self.disconnectButton, 10, 8, 1, 1)
        self.setLayout(gridLayout)
        self.setWindowTitle("主菜单")
        self.resize(500, 800)
        self.sendButton.clicked.connect(self.setPlainTextContent)

        self.disconnectButton.clicked.connect(self.disconnect)

    '''
    在这里发送消息
    并且设置文本的信息
    '''
    def setPlainTextContent(self):
        text = "{\"info\": \"%s\", \"type\": \"msg\"}" % self.inputText.text()
        print(text)
        self.content = self.content + "\n" + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " " + text
        self.plainText.setText(self.content)
        # global_var.client_socket.sendto(text.encode(), ("localhost", 23000))
        global_var.client_socket.sendall(text.encode())
        time.sleep(1)
        self.content = self.content + "\n" + "服务器响应：" + global_var.messages[-1]
        print("message:"+global_var.messages[-1])
        self.plainText.setText(self.content)

        self.inputText.setText("")

    def disconnect(self):
        global_var.client_socket.close()
        self.close()
        sys.exit(0)

class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        usr = QLabel("用户：")
        pwd = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)
        self.messages = ""

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3)
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3)

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)
        self.setWindowTitle("登录")
        self.resize(300, 200)



    def accept(self):
        account = self.usrLineEdit.text().strip()
        password = self.pwdLineEdit.text()
        s = "{\"account\": \"%s\", \"password\": \"%s\", \"type\": \"login\"}" % (account, password)
        # global_var.client_socket.sendto(s.encode(), ('localhost', 23000))
        global_var.client_socket.sendall(s.encode())
        time.sleep(1)
        isLoginSuccess = bool(global_var.messages[0])
        print("isLogin: "+str(isLoginSuccess))

        '''
        这里验证登录
        还是创建一个socket链接来验证密码
        在函数里是用不了全局变量的，所以需要建立两次链接，完成之后关闭就行
        发送给服务器，然后服务返回一个是否正确的
        '''
        if isLoginSuccess:
            # super(LoginDlg, self).accept()
            # self.global_var.client_socket.close()
            self.close()
            # w = QDialog()
            w = MainDlg()
            w.show()
            w.exec_()
        else:
            QMessageBox.warning(self,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.usrLineEdit.setFocus()

def receiveFromServer():
    print("hello world")
    while True:
        data = global_var.client_socket.recv(1024)
        print(data.decode())
        if not data:
            exit()
        # global_var.messages = data
        # print("global_var")
        # print(global_var.messages)
        global_var.messages.append(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " " + data.decode())



if __name__ == "__main__":
    # global_var.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # global_var.client_socket.bind(("localhost", 23001))
    # 接受服务器
    recvThread = threading.Thread(target=receiveFromServer)
    recvThread.setDaemon(True)
    recvThread.start()
    app = QApplication(sys.argv)
    dlg = LoginDlg()
    dlg.show()
    dlg.exec_()
    app.exit()
