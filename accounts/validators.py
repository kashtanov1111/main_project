from django.core.validators import URLValidator

class CustomURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(CustomURLValidator, self).__call__(value)