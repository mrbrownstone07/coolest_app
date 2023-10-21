import json
import logging


INFO_LEVEL='info'
ERROR_LEVEL='error'

def log(msg:str, log_level:str=None, extra:dict=None):
    """ msg: you can pass the main log message using this field,
        log_level: the level of the log(info/error), by default log_level is error.
        extra: obj/dict, you can pass all the extra fields you need to log, using a dict.
    """

    logger = None    

    if log_level.lower() == 'info':
        logger = logging.getLogger('restapi.log.success.file')
    else:
        logger = logging.getLogger('restapi.log.error.file')

    if 'request' in extra:
        extra['request'] = json.loads(extra['request'])

    if 'response' in extra:
        extra['response'] = json.loads(extra['response'])
    
    params = extra
    extra = {'params': json.dumps(params, indent=4, sort_keys=True)}

    if log_level.lower() == 'info':
        logger.info(msg=msg, extra=extra)
    else:
        logger.error(msg=msg, extra=extra)
       

        

