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

### Plan endpoints

**POST /sellgood/plan/**: Creates a plan.\
**GET /sellgood/plan/**: Lists all plans sorted by name.\
**GET /sellgood/plan/{id}/**: Lists plan details.\
**PUT /sellgood/plan/{id}/**: Updates plan data.\
**PATCH /sellgood/plan/{id}/**: Partially updates plan data.\
**DELETE /sellgood/plan/{id}/**: Deletes a plan.\

### Seller endpoints

**POST /sellgood/seller/**: Creates a seller.\
**GET /sellgood/seller/**: Lists all sellers sorted by name.\
**GET /sellgood/seller/{id}/**: Lists seller details.\
**GET sellgood/seller/{id}/address/**: Lists seller address.\
**GET sellgood/seller/{id}/sale/**: Lists seller sales.\
**PUT /sellgood/seller/{id}/**: Updates seller data.\
**PATCH /sellgood/seller/{id}/**: Partially updates seller data.\
**DELETE /sellgood/seller/{id}/**: Deletes a seller.\

### Address endpoints

**POST /sellgood/address/**: Creates a address.\
**GET /sellgood/address/**: Lists all addresses sorted by seller's name.\
**GET /sellgood/address/{id}/**: Lists address details.\
**PUT /sellgood/address/{id}/**: Updates address data.\
**PATCH /sellgood/address/{id}/**: Partially updates address data.\
**DELETE /sellgood/address/{id}/**: Deletes a address.\

### Sale endpoints

**POST /sellgood/sale/**: Creates a sale.\
**GET /sellgood/sale/**: Lists all sales sorted by date.\
**GET /sellgood/sale/{id}/**: Lists sale details.\
**PUT /sellgood/sale/{id}/**: Updates sale data.\
**PATCH /sellgood/sale/{id}/**: Partially updates sale data.\
**DELETE /sellgood/sale/{id}/**: Deletes a sale.\

### Commission endpoints

**GET /sellgood/commission/**: Lists all commissions ranked by highest value.\
**GET /sellgood/commission/?date__year={year}**: Lists all commissions in a specific year ranked by highest value.\
**GET /sellgood/commission/?date__month={month}**: Lists all commissions in a specific month ranked by highest value.\
**GET /sellgood/commission/?date__year={year}&date__month={month}**: Lists all commissions in a specific year and month ranked by highest value.\
**GET /sellgood/commission/{id}/**: Lists commissions details.\

## Observations

In date input, the endpoint updates the day to the last day of the respective month. For instance, if the input date is "2019-07-15", the output date will be "2019-07-31". This endpoint accepts only one sale per month per seller.

This endpoint  automaticlly calculates the commision and identifies if the seller should reiceve an e-mail notification based on the respective commision value.


