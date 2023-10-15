# Crowd_Fund_API_-Project

### Endpoints

POST (Register) /register

<!-- To get registered as an admin, make sure that the is_admin variable is set to "True" else you'll be registered as a mere user -->


REQUEST
```json
{
    "first_name": "sam",
    "last_name": "jones",
    "email": "sam@gmail.com",
    "password": "pass",
}
```

RESPONSE
```json

{
    "message": "Please enter your OTP",
    "otp": 4148,
    "status": 200
}
```


POST (verify otp) /token/<email>

REQUEST
```json
{
    "otp": "7854"
}
```

RESPONSE
```json
{
    "message": "You have been verified",
    "status": 200
}
```


POST (Login) /login

REQUEST
```json
{
    "emial" : "sam@gmail.com",
    "password" : "pass"
}
```


RESPONSE
```json
  {
    "access_token": "iIsInR5cCI6IkpXVCJ9..............................",
    "message": "Login successful",
    "status": 200
}
```


To login with your access_token in the Authorization holder in the bearer token section,

```sh
<access_token>
```




<!-- To make a fundraising request -->

POST /category (users)
@jwt_required

REQUEST 
```json
{
    "category_name" : "Animals",
    "fundraising_for" : "Myself",
    "amount" : 123456789,
    "expiryDate" : "2023-10-30",
    "user_email" : "mj@gmail.com",
    "minimum_amount": 5000,
    "description" : "I need to get a pet"
}
```

RESPONSE
```json

{
    "message": "Category added successfully",
    "status": 200
}
```


GET (users) /view_requests
@jwt_required()

RESPONSE
```json
{
    "requests": [
        [
            "Education",
            "Others",
            "120000.00",
            "For the education of Others"
        ],
        [
            "Animals",
            "Others",
            "120000.00",
            "For the feeding of Animals"
        ],
        [
            "Others",
            "Others",
            "120000.00",
            "For the feeding of Humans"
        ],
        [
            "Others",
            "Others",
            "122525250.00",
            "For the feeding of Everyone"
        ],
        [
            "Animals",
            "Myself",
            "123456789.00",
            "I need to get a pet"
        ]
    ],
    "status": 200
}
```
POST /logout
@jwt_required

RESPONSE
```json
{
    "message": "You have been logged out",
    "status": 200
}
```


GET/ (admin) /see_requests
@jwt_required

RESPONSE
```json

{
    "message": "These are the users requests",
     "requests": [
        {
            "amount": "876543.00",
            "approved": 1,
            "category_name": "business",
            "description": "kjhgfd",
            "expiry_date": "Sat, 21 Oct 2023 00:00:00 GMT",
            "fundraising_for": "others",
            "id": 1,
            "user_email": "kingsleydike318@gmail.com"
        },
        {
            "amount": "20000.00",
            "approved": 1,
            "category_name": "business",
            "description": "vd vdc addve dfvfd",
            "expiry_date": "Sat, 21 Oct 2023 00:00:00 GMT",
            "fundraising_for": "yourself",
            "id": 2,
            "user_email": "hellotunmbi@protonmail.com"
        },
        {
            "amount": "120000.00",
            "approved": 0,
            "category_name": "Education",
            "description": "For the education of Others",
            "expiry_date": null,
            "fundraising_for": "Others",
            "id": 3,
            "user_email": "sj@gmail.com"
        }
     ],
     "status": 200
}
```