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
Creates a seller.\
**Input**\
```python
{
    "cpf": "77711100077",
    "name": "Bruce Wayne",
    "age": 30,
    "phone": "47997001177",
    "email": "bruce_wayne@wayneenterprises.com",
    "plan": 3
}
```
**Output**\
```python
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

#### GET /sellgood/seller/\
Lists all sellers sorted by name.\
**Output**\
```python
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

#### GET /sellgood/seller/1/\
**Output**\
Lists seller details.\
```python
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

**PUT /sellgood/seller/1/**\
Updates all seller data. \
**Input**\
```python
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
**Output**\
```python
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
Updates seller data partially. \
**Input**\
```python
{
    "id": 1,    
    "name": "Bruce Wayne - The Batman"
}
```
**Output**\
```python
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
