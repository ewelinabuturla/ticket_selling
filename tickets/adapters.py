from collections import namedtuple


class CardError(Exception):
    pass


class PaymentError(Exception):
    pass


class CurrencyError(Exception):
    pass


PaymentResult = namedtuple('PaymentResult', ('amount', 'currency'))
supported_currencies = ('EUR')


def charge(amount, token, currency='EUR'):
    """
    Charges the total amount of purchased tickets.

    :param amount: <class 'float'>
    :param token: <class 'str'>
    :param currency: <class 'str'>
    """
    if token == 'card_error':
        raise CardError('Your card has been declined')
    elif token == 'payment_error' or token == '':
        raise PaymentError('Something went wrong with your transaction')
    elif currency not in supported_currencies:
        raise CurrencyError(f'Currency {currency} not supported')
    else:
        return PaymentResult(amount, currency)
