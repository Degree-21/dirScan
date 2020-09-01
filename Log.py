import logging


def set_log(msg, file_name='log.txt'):
    logging.basicConfig(
                        filename=file_name,
                        level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %X'
                       )
    logging.info(msg)
