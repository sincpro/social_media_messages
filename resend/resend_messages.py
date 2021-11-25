import logging

from ..dispatcher.dispatcher import dispatch
from ..dispatcher.actions import FB_SEND_MESSAGE

_logger = logging.getLogger(__name__)


def resend_message(registers_not_sent, token):
    for register in registers_not_sent:
        if register.attempts < 3:
            response = dispatch(
                FB_SEND_MESSAGE,
                data={"message": register.customer_message},
                id_facebook=register.customer_id,
                token=token,
            )
            register.attempts = register.attempts + 1
            if response:
                register.status_message = "SENT"
        else:
            _logger.info("Verificar mensaje no enviado: " + register)
