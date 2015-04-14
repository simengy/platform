import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class alert(object):

    def __init__(self, from_addr, to_addr, pwd, message):
       
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.pwd = pwd

        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = 'Link'
        self.msg['From'] = from_addr
        self.msg['To'] = to_addr

        # translate text to html
        message = message.replace('\n', '<br>')
        
        html = '''
        <html>
            <head></head>
            <body>
                <p>
                {}
                
                <br><br>
                sent from,<br>
                <br>
                Constraint Alerting System<br>
                <br>
                <a href='http://10.20.102.190/machinelearning.html'>Data Science Team</a>
                </p>
            </body>
        </html>
        '''.format(message)
        
        part = MIMEText(html, 'html')

        self.msg.attach(part)


    def alerting(self):
        
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()
        mail.starttls()
        
        mail.login(self.from_addr, self.pwd)
        mail.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        mail.quit()


if __name__ == '__main__':
    
    message = '''
To whom it may concern,

We are testing the alerting system. This is supposed to be the alerting email received in production.
    '''
   
    receiver = raw_input('Receiver\' Username [%s]: ' % getpass.getuser())
    sender = raw_input('\nSender\'s Username [%s]: ' % getpass.getuser())
    print ('Enter password for Username %s' % sender)
    pwd = getpass.getpass()

    trigger = alert(sender, receiver, pwd, message)
    
    try:
        trigger.alerting()
    except Exception, err:
        # Probably Password or User name error
        print err

