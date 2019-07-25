from decimal import Decimal

from django.db import models
from django.core.validators import EmailValidator, MinValueValidator


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
        ordering = ['date']
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
