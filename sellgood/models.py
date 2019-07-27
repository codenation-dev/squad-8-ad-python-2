from decimal import Decimal

from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.core.mail import send_mail
from django.conf import settings

class Plan(models.Model):
    name = models.CharField(max_length=50)
    minimum_amount = models.DecimalField(
        max_digits=7, decimal_places=2,                                        validators=[MinValueValidator(Decimal(0.0))])
    lower_percentage = models.DecimalField(
        max_digits=3, decimal_places=2, 
        validators=[MinValueValidator(Decimal(0.0))])
    higher_percentage = models.DecimalField(
        max_digits=3, decimal_places=2, 
        validators=[MinValueValidator(Decimal(0.0))])

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Seller(models.Model):
    cpf = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Address(models.Model):    
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    number = models.CharField(max_length=7)
    complement = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=8)
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  primary_key=True)

    class Meta:
        ordering = ['seller']

    def __str__(self):
        return f'{self.seller.name}, {self.city}'


class Sale(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=7, 
                                 decimal_places=2, 
                                 validators=[MinValueValidator(Decimal(0.0))])
    commission = models.DecimalField(max_digits=7, 
                                     decimal_places=2, 
                                     editable=False)   
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        unique_together = ['seller', 'date']

    def __str__(self):
        return f'{self.date}, {self.amount}, {self.seller.name}'

    def save(self, *args, **kwargs):
        plan = self.seller.plan
        if Decimal(self.amount) > plan.minimum_amount:
            self.commission = Decimal(self.amount)*plan.higher_percentage
        else:
            self.commission = Decimal(self.amount)*plan.lower_percentage

        super().save(*args, **kwargs)

    def notify(self, *args, **kwargs):
        seller = Seller.objects.get(pk=self.seller.id)
        sales = seller.sale_set.all()[:5]

        if len(sales) > 1:
            commissions = [sale.commission for sale in sales]
                        
            weighted_average = self.commission_weighted_average(commissions)
            minimum = weighted_average-(weighted_average*Decimal(0.1))
            
            if self.commission <= minimum:                
                subject = 'Commission performance tracking'
                message = (f'Hello {self.seller.name}.\r\n\r\n'
                           'You need to work harder, you are below the'   'average!')
                send_mail(subject, message, 
                          settings.EMAIL_HOST_USER, 
                          [self.seller.email])
                return True            
            return False
        return False

    def commission_weighted_average(self, commissions):    
        sum_weighted_terms = 0
        sum_terms = 0
        for weight, amount in enumerate(sorted(commissions), 1):
                sum_weighted_terms += Decimal(weight)*amount
                sum_terms += Decimal(weight)
        return sum_weighted_terms/sum_terms  
 