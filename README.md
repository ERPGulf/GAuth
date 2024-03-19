## Gauth

Authenticaltion APP for Frappe ERPNext by ERPGulf

#### License

mit# GAuth




## Generate token and refresh_key (GET)

The generate token secure API is designed to facilitate secure authentication and token generation for accessing resources within the system.It generate token and refresh key.Here the request parameters are api key, api secret and app key. user-related parameters are included in the request headers as cookies.

### Request

```
curl --location '/api/method/gauth.gauth.gauth.generate_token_secure' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image=; full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'api_key="xxxxxx"' \
--form 'api_secret="xxxxx"' \
--form 'app_key="xxxxxmE5Nxxx=="' \
--form 'client_secret="xxxx"'
```
### Response
```
{
    "data": {
        "access_token": "3xxxxxB",
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": "all openid",
        "refresh_token": "xxxxxxxXxx"
    }
}

```

## Generate token for Users (GET)
This API is designed to securely generate authentication tokens for users based on their provided credentials and application key. It generate  each users token and refresh key. we pass the token that get from  generate token and refresh key  api to authenication bearer token field . Here the  parameters are api key, api secret and app key,user_name,password. user-related parameters are included in the request headers as cookies.
### Request

```
curl --location '/api/method/gauth.gauth.gauth.generate_token_secure_for_users' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image=; full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=; full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--header 'Authorization: Bearer your bearer token' \
--form 'api_key="your api key"' \
--form 'api_secret=""' \
--form 'app_key="xxxxx"' \
--form 'client_secret="xxxxx"' \
--form 'username="xxxx"' \
--form 'password="xxx"'
```
### Response
```
{
    "data": {
        "token": {
            "access_token": "xxx",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "all openid",
            "refresh_token": "xxxx5"
        },
        "user": {
            "id": "xx",
            "full_name": "xxxxxx",
            "email": "rxxxxx",
            "phone": "your mobile number"
        }
    }
}

```

## User available or not (GET)
This api checks the availability of a user based on either their email or mobile phone number.parameters are user email and phone number, Here authentication  is required,user-related parameters are included in the request headers as cookies.
### Request

```
curl --location --request GET 'api/method/gauth.gauth.gauth.is_user_available' \
--header 'Authorization: Bearer xxxxxx' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'mobile_phone=""' \
--form 'user_email="xxx"'
```
### Response
```
{
    "message": "Mobile exists",
    "user_count": 1
}
```

## create user (POST)
  This api  creating a new user and related records in a system,parameters are full_name,password,mobile_no,email,id,role, Here authentication  is required.user-related parameters are included in the request headers as cookies.
### Request

```
curl --location 'api/method/gauth.gauth.gauth.g_create_user' \
--header 'Authorization: Bearer YourBearerToken' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'full_name="Your Name"' \
--form 'password="YourPassword"' \
--form 'mobile_no="xxxxxxx"' \
--form 'email="youremail@erpgulf.com"' \
--form 'role="Auction"' \
--form 'id=""'

```
### Response
```
{
    "message": "User already exists",
    "user_count": 1
}
```

## who am i (GET)
Api is used to get the username of token which used in bearer token for authentication,The primary purpose of this api is to return the current user's information,Here authentication is required.user-related parameters are included in the request headers as cookies.
### Request

```
curl --location 'api/method/gauth.gauth.gauth.whoami' \
--header 'Authorization: Bearerxxxxx' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image='

```
### Response
```
{
    "data": {
        "user": "xxx"
    }
}
```

## delete user (DELETE)
 Api is designed for deleting user records. It takes three parameters username, email, and mobile_no  to identify the user to be deleted. This api verifies the existence of the user based on these parameters, and if found, deletes the user record from the database.Authentication is required.user-related parameters are included in the request headers as cookies.
### Request

```
curl --location 'api/method/gauth.gauth.gauth.g_delete_user' \
--header 'Authorization: Bearer xxxxxxxB' \
--header 'Cookie: full_name=xxxx; sid=xxxxx; system_user=yes; user_id=mumtaz32%40erpgulf.com; user_image=' \
--form 'email="xxxxx"' \
--form 'mobile_no=""' \
--form 'username="sfdwsw"'
```
### Response
```
{
    "message": "User not found",
    "user_count": 0
}
```



## get user name (GET)
Api is used to retrieve user details from a Frappe-based system based on either the user's email address or mobile phone number. The api allows flexibility by accepting one of these parameters as input. It fetches information such as the user's name and whether the user is enabled or not. Authentication is required,user-related parameters are included in the request headers as cookies.

### Request

```
curl --location --request GET 'api/method/gauth.gauth.gauth.get_user_name' \
--header 'Authorization: Bearer xxxxxx' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'user_email="xxxx"' \
--form 'mobile_phone="7xxxx"'
```
### Response
```
{
    "data": [
        {
            "name": "xxxx",
            "enabled": 1
        }
    ],
    "user_count": 0
}
```

##  update password (POST)
 This api is used to update the password for a user in a system.it takes a username and a new password as parameters and ensures the password update is performed securely.Here authentication  is required.user-related parameters are included in the request headers as cookies. needed.
### Request

```
curl --location 'api/method/gauth.gauth.gauth.g_update_password' \
--header 'Authorization: Bearer YourToken' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'username="xxx"' \
--form 'password="YourPassword"'
```
### Response
```
{
    "message": "Password successfully updated",
    "user_count": 1
}
```

## create_user (POST)
This api is  designed to create new user accounts in a system. It takes several parameters such as full_name, password, mobile_no, email, id, and an optional role.Here authentication  is required.user-related parameters are included in the request headers as cookies. needed.

### Request

```
curl --location --request GET 'api/method/gauth.gauth.gauth.is_user_available' \
--header 'Authorization: Bearer xxxxx' \
--form 'mobile_phone="xx"' \
--form 'user_email="xxx"'
```
### Response
```
{
    "reset_key": "xx7",
    "generated_time": "2024-02-12 07:35:21.903321",
    "URL":" 8012/update-password?key=261907"
}
```

<!-- ##  test passwordstrength

### Request

```
curl --location --request GET '/api/method/frappe.core.doctype.user.user.test_password_strength' \
--header 'Authorization: Bearer EaIt6IRFwJNcu3LSebgtT0wfs4Cz8i' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'new_password="&^&*JKJ&^WD878BHerw"'
```
### Response
```
{
    "message": {}
}

``` -->

## Enable  or disable user (POST)
This api is designed to enable or disable a user in a system based on the provided parameters.Here authentication  is required.user-related parameters are included in the request headers as cookies  needed.

### Request

```
curl --location '/api/method/gauth.gauth.gauth.g_user_enable' \
--header 'Authorization: Bearer rxxxxx' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'username="xxx"' \
--form 'email="7xxxx"' \
--form 'mobile_no="7xxx"' \
--form 'enable_user="True"'
```
### Response
```
{
    "message": "User successfully enabled ",
    "user_count": 1
}
```

## Current time (GET)
This api shows the current time.
### Request

```
curl --location '/api/method/gauth.gauth.gauth.time' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image='
```
### Response
```
{
    "message": {
        "data": {
            "serverTime": "2024-02-12 08:09:00.081533",
            "unix_time": 1707714540.081707
        }
    }
}

``` 

## get account balance (GET)
This api is designed to find the balance of a user, here authentication is required, which user token is passed here that user account balance we get.

### Request
```
curl --location --request GET 'api/method/gauth.gauth.gauth.get_account_balance' \
--header 'Authorization: Bearer xxxxx' \
--header 'Cookie: full_name=Guest; sid=Guest; system_user=yes; user_id=Guest; user_image=' \
--form 'customer="xx"' \
--form 'mobile_phone="xxx"'
```
### Response

```
{
    "data": {
        "balance": 0.0
    }
}
```