# Telesales commission management

This project is a REST API for calculating the monthly commission of each seller according to the commission rule selected at the registration time.

## Prerequisites

Python 3.7.3.
```bash
sudo apt-get install python3.7
```

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

### Plan endpoints

Creates a plan.
```
POST /sellgood/plan/
```
Lists all plans sorted by name.
```
GET /sellgood/plan/
```
Lists plan details.
```
GET /sellgood/plan/{id}/
```
Updates plan data.
```
PUT /sellgood/plan/{id}/
```
Partially updates plan data.
```
PATCH /sellgood/plan/{id}/
```
Deletes a plan
```
DELETE /sellgood/plan/{id}/
```

### Seller endpoints

Creates a seller.
```
POST /sellgood/seller/
```
Lists all sellers sorted by name.
```
GET /sellgood/seller/
```
Lists seller details.
```
GET /sellgood/seller/{id}/
```
Lists seller address.
```
GET sellgood/seller/{id}/address/
```
Lists seller sales.
```
GET sellgood/seller/{id}/sale/
```
Updates seller data.
```
PUT /sellgood/seller/{id}/
```
Partially updates seller data.
```
PATCH /sellgood/seller/{id}/
```
Deletes a seller
```
DELETE /sellgood/seller/{id}/
```

### Address endpoints

Creates a address.
```
POST /sellgood/address/
```
Lists all addresses sorted by name.
```
GET /sellgood/address/
```
Lists address details.
```
GET /sellgood/address/{id}/
```
Updates address data.
```
PUT /sellgood/address/{id}/
```
Partially updates address data.
```
PATCH /sellgood/address/{id}/
```
Deletes a address
```
DELETE /sellgood/address/{id}/
```

### Sale endpoints

Creates a sale.
```
POST /sellgood/sale/
```
Lists all sales sorted by name.
```
GET /sellgood/sale/
```
Lists sale details.
```
GET /sellgood/sale/{id}/
```
Updates sale data.
```
PUT /sellgood/sale/{id}/
```
Partially updates sale data.
```
PATCH /sellgood/sale/{id}/
```
Deletes a sale
```
DELETE /sellgood/sale/{id}/
```

### Commission endpoints

Lists all commissions sorted by name.
```
GET /sellgood/commission/
```
Lists commissions details.
```
GET /sellgood/commissions/{id}/
```
Lists all commissions in a specific year ranked by highest value.
```
GET /sellgood/commission/?date__year={year}
```
Lists all commissions in a specific month ranked by highest value.
```
GET /sellgood/commission/?date__month={month}
```
Lists all commissions in a specific year and month ranked by highest value.
```
GET /sellgood/commission/?date__year={year}&date__month={month}
```

## Observations

In date input, the endpoint updates the day to the last day of the respective month. For instance, if the input date is "2019-07-15", the output date will be "2019-07-31". This endpoint accepts only one sale per month per seller.

This endpoint  automaticlly calculates the commision and identifies if the seller should reiceve an e-mail notification based on the respective commision value.

For Sale PATCH method is required to include the date field.

Global variables starting with EMAIL_ in the setting.py file located in the telesales package must be updated with the sender information to perform email notification.
