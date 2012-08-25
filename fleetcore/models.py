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

import logging
import os.path
from pdflib.pdf2txt import TextConverter, TextExtractionNotAllowed, PDFResourceManager, \
                           FigureItem, TextItem, enc, convert
LOG_DIR = 'logs'
FIELD_TOKEN = '|'
PHONE_TOKEN = '-'
X = 0
Y = 1


class Bill(models.Model):
    invoice = models.FileField(upload_to='invoices')

    def save(self, *args, **kwargs):
        # parse invoice
        fname = self.invoice.path
        LOG_FILENAME = os.path.join(LOG_DIR, fname + '.log')
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)
        rsrc = PDFResourceManager()
        device = CellularConverter(rsrc, file(fname + '.csv', 'wb'))
        convert(rsrc, device, fname)
        super(Bill, self).save(*args, **kwargs)


class CellularConverter(TextConverter):
    """ Cellular Converter. """
    start_x, start_y = 0, 0 # 222.5, 22.85

    def __init__(self, rsrc, outfp, codec='utf-8'):
        TextConverter.__init__(self, rsrc, outfp, codec=codec)

    def process_item(self, item):
        if not isinstance(item, TextItem): return
        if item.origin[X] < self.start_x: return

        t = enc(item.text, self.codec)
        if item.origin[X] > self.last_x: # is a new row?
            self.last_x, self.last_y = item.origin

            row = FIELD_TOKEN.join(map(str.strip, self.last_content))
            if self.is_table_row:
                self.outfp.write(row + '\n') # previous content
            else:
                logging.debug("not is table row:" + row)

            self.is_table_row = PHONE_TOKEN in t and t.strip().replace(PHONE_TOKEN, '').isdigit()
            self.last_content = [t] # new content
        elif item.origin[Y] == self.last_y: # is the same table cell?
            self.last_content[-1] += t
        else: # new table cell for current row
            #assert self.last_x == item.origin[X]
            self.last_y = item.origin[Y]
            self.last_content.append(t)

    def end_page(self, page):
        TextConverter.end_page(self, page)

        self.last_x, self.last_y = self.start_x, self.start_y
        self.last_content = []
        self.is_table_row = False

        page = self.cur_item
        #import pdb; pdb.set_trace()
        #self.outfp.write('Page %s\n' % page.id)
        for child in page.objs:
            try:
                self.process_item(child)
            except AttributeError:
                pass
