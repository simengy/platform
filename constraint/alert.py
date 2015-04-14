import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class alert(object):

    def __init__(self, from_addr, to_addr,  message):
       
        self.from_addr = from_addr
        self.to_addr = to_addr
        
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

        usr = raw_input('Username [%s]: ' % getpass.getuser())
        pwd = getpass.getpass()

        mail.login(usr, pwd)
        mail.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        mail.quit()


if __name__ == '__main__':
    
    message = '''
To whom it may concern,<br>

We are testing the alerting system.<br>

You can refer to:

<a href='http://10.20.102.190/machinelearning.html'>link</a>
    '''


    trigger = alert('simengy@uci.edu', 'simeng.yan@saama.com', message)
    
    try:
        trigger.alerting()
    except Exception, err:
        # Probably Password or User name error
        print err

