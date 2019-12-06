
import os
import sys

import pika

sys.path.append(os.path.abspath('.\src'))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
os.environ['PYTHONPATH'] = os.path.abspath('..') + ";" + os.path.abspath('.')

# Configure the server
from config.iso8583_config import queue_name
from config.logging import LogConfig
from random import choices
from iso8583.ISO8583 import *
from iso8583.ISOErrors import *

population = ['00', '14', '30', '51', '76', '83', '92', '94', '96']
weights = [98.65, 0.10, 0.10, 1.00, 0.005, 0.001, 0.001, 0.007, 0.001]

log = LogConfig(__file__)
logger = log.create_logger()


def produce_bit39_random():
    choice = choices(population, weights)
    logger.debug("choice = " + choice[0])
    return choice[0]


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue_name)


def on_request(ch, method, props, body):
    isoStr = body.decode()
    logger.debug("\nInput ASCII |%s|" % isoStr)
    if isoStr is not None:
        try:
            pack = ISO8583()
            pack.setNetworkISO(isoStr)

            v1 = pack.getBitsAndValues()
            for v in v1:
                logger.debug('Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value']))

            if pack.getMTI() == '0200':
                logger.debug("\tThat's great !!! The client send a correct message !!!")
            else:
                logger.debug("The client doesn't send the correct message!")

        except InvalidIso8583 as ii:
            logger.debug(ii)
        except Exception:
            logger.debug('Something happened!!!!')

        # send answer
        pack.setMTI('0210')
        pack.setBit(39, produce_bit39_random())

        ans = pack.getNetworkISO()
        logger.debug('Sending answer %s' % ans)
        # logger.debug('routing key %s' % props.reply_to)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         # routing_key=queue_name,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=ans)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        isoStr = None


# if __name__ == '__main__':
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=queue_name)

logger.info("Waiting for message")
channel.start_consuming()
