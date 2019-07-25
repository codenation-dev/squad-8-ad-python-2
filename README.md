# Telesales commission management

This project is a REST API for calculating the monthly commission of each seller according to the commission rule selected at the registration time.

## Installation

Clone the project.
```bash
git clone https://github.com/codenation-dev/squad-8-ad-python-2.git
cd squad-8-ad-python-2/
```

Create a virtual environment and enable it.
```bash
python3.7 -m venv venv
source venv/bin/activate
```

Install the necessary packages through pip.
```bash
pip install -r requirements.txt
```

## Usage

Starting development server at http://127.0.0.1:8000/.
```bash
python manage.py runserver
```

Necessary header for all requests.
```
Content-Type: application/json
```

### Seller endpoints

**POST /sellgood/seller/**\
Creates a seller.
```python
# input
{
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 30,
    "phone": "47997001177",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
}
```
```python
# output
{
    "id": 1,
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 30,
    "phone": "47997001177",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
 }
```

**GET /sellgood/seller/**\
Lists all sellers sorted by name.

```python
# output
[
    {
        "id": 1,
        "cpf": "77711100077",
        "name": "Bruce Wayne",
        "age": 30,
        "phone": "47997001177",
        "email": "bruce_wayne@wayneenterprises.com",
        "plan": 3
    }
    {
        "id": 3,
        "cpf": "00022245655",
        "name": "Peter Parker",
        "age": 18,
        "phone": "51999112222",
        "email": "peter.parker@starkindustries.com",
        "plan": 1
    }
]
```

**GET /sellgood/seller/1/**\
Lists seller details.
```python
# output
{
    "id": 1,
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 30,
    "phone": "47997001177",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
}
```

**GET sellgood/seller/1/address/**\
List seller address.
```python
# output
{
    "seller": 1,
    "street": "6th Ave",
    "neighborhood": "Downtown",
    "city": "Gotham",
    "state": "Unknown",
    "number": "13",
    "complement": "The biggest building",
    "zipcode": "1300000"
}
```

**PUT /sellgood/seller/1/**\
Updates all seller data.

```python
# input
{
    "id": 1,
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 33,
    "phone": "47997001100",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
}
```

```python
# output
{
    "id": 1,
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 33,
    "phone": "47997001100",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
 }
```

**PATCH /sellgood/seller/1/**\
Updates seller data partially.
```python
# input
{
    "id": 1,    
    "name": "Bruce Wayne - The Batman"
}
```

```python
# output
{
    "id": 1,
    "cpf": "77711100077",
    "name": "Bruce Wayne - The Batman",
    "age": 33,
    "phone": "47997001100",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
 }
```

**DELETE /sellgood/seller/1/**\
Delete a seller.\


### Sale endpoints

**POST /sellgood/sale/**

```
# input
{
	"date": "2019-07-31",
	"amount": 12300.00,
	"seller": 1
}
```

Ps.: In date input, the endpoint updates the day to the last day of the respective month. For instance, if the input date is "2019-07-15", the output date will be "2019-07-31". This endpoint accepts only one sale per month per seller.

```
# output
{
    "id": 50,
    "date": "2019-07-31",
    "amount": "12300.00",
    "commission": "246.00",
    "seller": 1,
    "should_notify": false
}
```

This endpoint  automaticlly calculates the commision and identifies if the seller should reiceve an e-mail notification based on the respective commision value.

**GET /sellgood/sale/**

Returns a list ordered by

```
# output
[
    {
        "id": 51,
        "date": "2019-07-31",
        "amount": "12300.00",
        "commission": "246.00",
        "seller": 1
    },
    {
        "id": 52,
        "date": "2019-07-31",
        "amount": "15000.00",
        "commission": "300.00",
        "seller": 2
    }
]
```

**GET /sellgood/sale/52/**

List sale details

```
# output
{
    "id": 52,
    "date": "2019-07-31",
    "amount": "15000.00",
    "commission": "300.00",
    "seller": 2
}
```

**PUT /sellgood/sale/52/**

Updates all sale data.

```
# input 
{
    "date": "2019-08-30",
    "amount": "9800.00",
    "seller": 2
}
```
```
# output 
{
    "id": 52,
    "date": "2019-08-30",
    "amount": "9800.00",
    "commission": "196.00",
    "seller": 2
}

```

**PATCH /sellgood/sale/52/**

Updates sale data partially

```
# input
{
    "date": "2019-12-31",
}
```

```
# output 
{
    "id": 52,
    "date": "2019-12-31",
    "amount": "9800.00",
    "commission": "196.00",
    "seller": 2
}
```

**DELETE /sellgood/sale/52/**

Delete a sale.\

### Address endpoints

**POST /sellgood/address/**

```
# input
{
    "seller": 1,
    "street": "Batcave Street",
    "neighborhood": "Manhattan",
    "city": "Arkham City",
    "state": "Nova York",
    "number": "666",
    "complement": "Apartament 204",
    "zipcode": "10001"
}
```

```
# output
{
    "seller": 1,
    "street": "Batcave Street",
    "neighborhood": "Manhattan",
    "city": "Arkham City",
    "state": "Nova York",
    "number": "666",
    "complement": "Apartament 204",
    "zipcode": "10001"
}
```

**GET /sellgood/address/**

```
# output
[
    {
        "seller": 1,
        "street": "Batcave Street",
        "neighborhood": "Manhattan",
        "city": "Arkham City",
        "state": "Nova York",
        "number": "666",
        "complement": "Apartament 204",
        "zipcode": "10001"
    },
    {
        "seller": 2,
        "street": "1th Ave",
        "neighborhood": "Manhattan",
        "city": "New York",
        "state": "New York",
        "number": "1",
        "complement": "The coolest building",
        "zipcode": "1111111"
    }
]
```

**GET /sellgood/address/1**

List address details. For address endpoints, the "address id" is the "seller id".

```
# output
{
    "seller": 1,
    "street": "Batcave Street",
    "neighborhood": "Manhattan",
    "city": "Arkham City",
    "state": "Nova York",
    "number": "666",
    "complement": "Apartament 204",
    "zipcode": "10001"
}
```

**PUT /sellgood/address/1**

Updates all address data.

```
# input 
{
    "seller": 1,
    "street": "Batcave Street",
    "neighborhood": "Manhattan",
    "city": "Gotham City",
    "state": "Nova York",
    "number": "1235",
    "complement": "Confidential",
    "zipcode": "2050"
}
```

```
# output 
{
    "seller": 1,
    "street": "Batcave Street",
    "neighborhood": "Manhattan",
    "city": "Gotham City",
    "state": "Nova York",
    "number": "1235",
    "complement": "Confidential",
    "zipcode": "2050"
}

```

**PATCH /sellgood/address/1/**

Updates address data partially.

```
# input
{
    "street": "Main Street",
    "zipcode": "4561"
}
```

```
# output 
{
    "seller": 1,
    "street": "Main Street",
    "neighborhood": "Manhattan",
    "city": "Gotham City",
    "state": "Nova York",
    "number": "1235",
    "complement": "Confidential",
    "zipcode": "4561"
}
```

**DELETE /sellgood/address/1/**

Delete an address.\
