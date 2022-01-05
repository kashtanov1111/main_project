from django.db import models

from products_billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='USA')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return '%s\n%s\n%s\n%s, %s\n%s' % (
            self.address_line_1,
            self.address_line_2 or '',
            self.city,
            self.state,
            self.postal_code,
            self.country
        )