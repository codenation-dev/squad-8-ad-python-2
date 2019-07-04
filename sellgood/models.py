from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=50)
    minimum_value = models.DecimalField(max_digits=6, decimal_places=2)
    lower_percentage = models.DecimalField(max_digits=1, decimal_places=4)
    higher_percentage = models.DecimalField(max_digits=1, decimal_places=4)
    
    def __str__(self):
        return f'{self.name}, {self.minimum_value}'


class Seller(models.Model):
    cpf = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

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
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.seller.name}, {self.city}'


class Sale(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=6, decimal_places=2)  
    commission = models.DecimalField(max_digits=5, 
                                     decimal_places=2, 
                                     editable=False)   
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}, {self.value}, {self.seller.name}'
