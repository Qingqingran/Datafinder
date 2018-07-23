import re
from functools import partial


def not_surrounded_by_digit(func):
    def wrapper(text: str, pos):
        cond = not (text[max(0, pos[0] - 1)].isdigit() or text[min(len(text), pos[1] + 1)].isdigit())
        return cond and func(text, pos)
    return wrapper


def not_surrounded_by_alpha(func):
    def wrapper(text: str, pos):
        cond = not (text[max(0, pos[0] - 1)].isalpha() or text[min(len(text), pos[1] + 1)].isalpha())
        return cond and func(text, pos)
    return wrapper


# Define some filters
@not_surrounded_by_digit
def phone_number_filter(text: str, pos):
    # Use other techniques to judge if this is really a phone number
    return True


class Finder:
    __all_regex = {
        'email': r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',
        'IPv4': r'''(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$''',
        'hostname': r'''\b(([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])\.)+([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])\b''',
        'cardnum': r'([1-9]{1})(\d{14}|\d{18})',
        # creditcardnumregex = [visa, mastercard, American_express, diner_club, discover, jcb]
        'creditcardnum_visa': r'''([^\\d\\.-]|^)4[0-9]{3}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'creditcardnum_mastercard': r'''([^\\d\\.-]|^)5[1-5][0-9]{2}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'creditcardnum_American_express': r'''([^\\d\\.-]|^)(34|37)[0-9]{2}(\\ |\\-|)[0-9]{6}(\\ |\\-|)[0-9]{5}(\\D|$)''',
        'creditcardnum_diner_club1': r'''([^\\d\\.-]|^)30[0-5][0-9](\\ |\\-|)[0-9]{6}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'creditcardnum_diner_club2': r'''([^\\d\\.-]|^)(36|38)[0-9]{2}(\\ |\\-|)[0-9]{6}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'creditcardnum_discover': r'''([^\\d\\.-]|^)6011(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'creditcardnum_jcb1': r'''([^\\d\\.-]|^)3[0-9]{3}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\ |\\-|)[0-9]{4}(\\D|$)''',
        'phonenum': r'''(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?''',
        'creditcardnum_jcb2': r'''([^\\d\\.-]|^)(2131|1800)[0-9]{11}(\\D|$)''',
        'date': '(\\d{4})[-/\.](0[1-9]|1[012])[-/\.](0[1-9]|[12]\\d|3[01])',
        'idcard': r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx])',
        # postcoderegex = r'''(^[1-9][0-9]{5}$)'''
        # priceregex =
        # passwordregex =
        # activecoderegex =
        # issnregex =
        # urlregex =
        # imsiregex =
    }

    def __init__(self, text=''):
        self.__text = None
        self.__result = None
        self.set_text(text)

    def set_text(self, text):
        self.__text = text

        def __find_all():
            ret = dict()
            for tag, regex in self.__all_regex.items():
                ret.update({tag: [it.span() for it in re.finditer(regex, text)]})

            ret['phonenum'] = list(filter(partial(phone_number_filter, text), ret['phonenum']))
            return ret
        self.__result = __find_all()

    def find_all(self):
        """Return all the sensitive data.

        Format: a dictionary, strings like 'email', 'id_card' as key, list of positions as value.
        """
        return self.__result

    def find_email(self):
        """Return the list of positions of all the email addresses."""
        return self.__result['email']

    def find_phonenum(self):
        return self.__result['phonenum']
