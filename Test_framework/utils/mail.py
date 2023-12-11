"""
郵件類。用來給指定用戶發送郵件。可指定多個收件人，可帶附件。
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from .log import logger
from .config import REPORT_PATH

class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """初始化Email
        :param title: 郵件標題，必填。
        :param message: 郵件正文，非必填。
        :param path: 附件路徑，可傳入list（多附件）或str（單個附件），非必填。
        :param server: smtp服務器，必填。
        :param sender: 發件人，必填。
        :param password: 發件人密碼，必填。
        :param receiver: 收件人，多收件人用“；”隔開，必填。
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def _attach_file(self, att_file):
        """將單個文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 郵件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多個附件（傳入list），或者單個附件（傳入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 連接服務器並發送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 連接sever
        except (gaierror and error) as e:
            logger.exception('發送郵件失敗,無法連接到SMTP服務器，檢查網絡以及SMTP服務器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登錄
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用戶名密碼驗證失敗！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 發送郵件
            finally:
                smtp_server.quit()  # 斷開連接
                logger.info('發送郵件"{0}"成功! 收件人：{1}。如果沒有收到郵件，請檢查垃圾箱，'
                            '同時檢查收件人地址是否正確'.format(self.title, self.receiver))


if __name__ == '__main__':

    report = REPORT_PATH + '\\report.html'
    e = Email(title='百度搜素測試報告',
              message='這是今天的測試報告，請查收！',
              receiver='396214358@qq.com',
              server='',
              sender='',
              password='',
              path=report
              )
    e.send()