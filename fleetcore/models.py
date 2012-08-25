from django.contrib.auth.models import User
from django.db import models


INTERNAL = 0.0717
IVA = 0.27
MINUTE_CENTS = 22
PESOS = 100.0


class MoneyField(models.DecimalField):
    pass


class Plan(models.Model):
    name = models.CharField(max_length=100)
    is_clearing = models.BooleanField()
    cost_cents = MoneyField()

    def __unicode__(self):
        return u'%s - $%s' % (self.name, self.cost)

    @property
    def cost(self):
        return self.cost_cents / PESOS


class Phone(models.Model):
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    notes = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.number, self.user)


class Consumption(models.Model):
    phone = models.ForeignKey(Phone)
    billing = models.DateField(auto_now=True) # billing date
    period = models.DateField(auto_now_add=True) # period to pay

    monthly_amount_cents = MoneyField('Abono')
    refund_cents = MoneyField('Cargos y reintegros')
    included_minutes = models.PositiveIntegerField('Aire incluido')
    excess_minutes = models.PositiveIntegerField('Aire excedente')
    total_cents = MoneyField('Total')
    equipment_cents = MoneyField('Equipo')
    sms = models.PositiveIntegerField()

    payed_cents = MoneyField(null=True) # cents

    def __unicode__(self):
        return self.period

    @property
    def total_without_fees(self):
        if phone.plan.is_clearing:
            res = self.total_cents - self.monthly_amount_cents
            res += self.included_minutes * MINUTE_CENTS
        else:
            res = self.monthly_amount_cents
        return res

    @property
    def total_in_pesos(self):
        res = self.total_without_fees
        fees = res * INTERNAL + res * IVA # fees
        res = res + fees + self.equipment_cents
        return res / PESOS # round?

    class Meta:
        ordering = ('period',)
        get_latest_by = 'period'


class Bill(models.Model):
    invoice = models.FileField(upload_to='invoices')

    def save(self, *args, **kwargs):
        # parse invoice
        fname = self.invoice.path
        import pdf2cell
        data = pdf2cell.main(fname)
        super(Bill, self).save(*args, **kwargs)
