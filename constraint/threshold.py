import alert
import getpass


def threshold(ci_low, ci_high, test, metric_name, image, ci_level='95%'):
    
    if len(ci_low) == len(ci_high) == len(test):
        N = len(test)
    else:
        print 'PREDICTION and TEST are size-different!'
        return 
    
    receiver = raw_input('Reciever\' Username [%s]' % getpass.getuser())
    sender = raw_input('\nSender\' Username [%s]' % getpass.getuser())
    print ('Enter password for Username %s' % sender)
    pwd = getpass.getpass()

    message = '''
    Alerts of METRIC = {}:

        '''.format(metric_name)

    for p in xrange(N):
        print p, test[p], ci_low[p], ci_high[p]
        if test[p] < ci_low[p] or test[p] > ci_high[p]:
            
            message += '''
            
            ####################################################
            Day {}:
            
            observation value = {} 
            is out of {} confidence interval:
            [{}, {}].

            Please investigate the data!
            ####################################################
            
            '''.format(p, test[p], ci_level, ci_low[p], ci_high[p])

    trigger = alert.alert(sender, receiver, pwd, message, image)
            
    try:
        trigger.mailing()
    except Exception, err:
        print err
            
