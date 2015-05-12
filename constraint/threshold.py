import alert
import getpass


def threshold(metric_name, image, message):
    
    receiver = raw_input('Reciever\' Username [%s]' % getpass.getuser())
    sender = raw_input('\nSender\' Username [%s]' % getpass.getuser())
    print ('Enter password for Username %s' % sender)
    pwd = getpass.getpass()

    header = '''
    Alerts of METRIC = {}:

        '''.format(metric_name)
    
    message = header + message
                
    trigger = alert.alert(sender, receiver, pwd, message, image)
            
    try:
        trigger.mailing()
    except Exception, err:
        print err
            
