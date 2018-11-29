# Authentication Services

This are the authentication endpoints

---
## Log in
User authentication endpoint  
**POST**  
**url** `/auth/signin/`  
**receives** application/json  
**Authentication:**  Not Required
#### Request Body Parameters  
|Field  |Type  | Description| Extra info|
|-------|------|------------|------|
|email  |string|user email  |required|
|password|string|user password|required|

**json example**  
```
POST /api/auth/signin/
{
  "username": "user@test.com",
  "password": "reallySecurePassword"
}
```

### Responses

#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description|
|-------|------|------------|
|id  |integer|user id  |
|user|string|user name|
|token|string|user session token|

**json response**
```
HTTP/1.1 200 OK
{
  "id": 1,
  "user": "UserOO1",
  "token": "really_cool_session_token"
}
```

#### 400 Bad Request - Invalid email format or empty credentials
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|email  |error message|
|password|error message|

**json response**  
```
HTTP/1.1 400 Bad Request
{
  "email": [
    "Please include email",
    "Please use a valid email"
  ],
  "password": [
    "Please submit a valid password"
  ]
}
```

#### 401 Unauthorized - Wrong credentials
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
HTTP/1.1 401 Unauthorized
{
  "detail": "Login failed: Wrong credentials"
}
```
---
## Log out
User log out endpoint  
**POST**  
**url** `/auth/signout/`  
**receives** application/json  
**Authentication:**  Required
#### Request Body Parameters  
**No Request Body required**  

**json example**  
```
POST /api/auth/signout/
```

### Responses

#### 200 Success
**returns:** application/json  
**No response body returned**  

**json response**
```
HTTP/1.1 200 OK
```
---
## Sign up
User account creation endpoint  
**POST**  
**url** `/auth/signup/`  
**receives** application/json  
**Authentication:**  Not Required
#### Request Body Parameters  
|Field       |Type  | Description| Extra info|
|-------     |------|------------|------|
|first_name  |string|user name  |required|
|last_name   |string|user last name||
|email       |string|user email|required|
|password    |string|user password|required|
|confirm_password|string|password confirmation|required|

**json example**  
```
  POST /api/auth/signup/
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john_doe@test.com",
    "password": "reallySecurePassword",
    "confirm_password": "reallySecurePassword"
  }
```

### Responses
#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description|
|-------|------|------------|
|first_name|integer|new user name  |
|last_name|string|new user last name|
|email|string|new user email|

**json response**
```
HTTP/1.1 200 OK
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john_doe@test.com"
}
```

#### 400 Bad Request - Invalid data
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|first_name|error message|
|email|error message|
|password|error message|

**json response**
```
HTTP/1.1 400 Bad Request
{
  "first_name": [
    "This field may not be blank."
  ],
  "email": [
    "This field may not be blank.",
    "The mail is already in use.",
    "Enter a valid email address."
  ],
  "password": [
    "This field may not be blank.",
    "Passwords do not match"
  ]
}
```
