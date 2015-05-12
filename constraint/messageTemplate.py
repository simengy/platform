class template:

    def type_1(self, IDs, scores, threshold_lower, threshold_upper):

        assert len(scores) == len(threshold_lower) and len(scores) == len(IDs)
        
        N = len(scores)
        message = ''
        
        for p in xrange(N):
            print p, scores[p], threshold_lower[p], threshold_upper[p]
            if scores[p] < threshold_lower[p] or scores[p] > threshold_upper[p]:
            
                message +=  '''
            
                ####################################################
                
                ClaimID = {}:
                    
                fraud score = {} 
                is higher than the current threshold = {}.
    
                Please investigate the transaction!
                ####################################################
            
                '''.format(IDs[p], scores[p], threshold_upper[p])

        return message
    
    
    def type_2(self, obs, ci_lower, ci_upper, ci_level = '95%'):
    
        assert len(ci_lower) == len(ci_upper) and len(obs) == len(ci_lower)
        
        N = len(obs)
        message = ''
        
        for p in xrange(N):
            print p, obs[p], ci_lower[p], ci_upper[p]
            if obs[p] < ci_lower[p] or obs[p] > ci_lower[p]:

                message += '''
                
                ####################################################
                Day = {}:
                        
                Observation value = {} 
                is out of {} confidence interval:
                [{}, {}].
            
                Please investigate the transaction!
                ####################################################
            
                '''.format(p, obs[p], ci_level, ci_lower[p], ci_upper[p])

        return message

