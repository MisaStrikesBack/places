# Favorites places service

This service saves a selected place in the users favorites section  

---

## List
Favorites list endpoint  

**GET**  
**url** `/favorites/`  
**receives:** application/json  
**Authentication:**  Required  
**Pagination size:** 10 objects  

#### Query Parameters  
|Param    | Description    | Extra info|valid values|
|---------|----------------|-----------|------------|
|lat      |search latitude |required   |integer     |
|long     |search longitude|required   |integer     |
|order   |search order value  |           |'newer'<br>'older'<br>'better'<br>'worst'<br>'near'<br>'far'|

**request examples**  
```
GET /api/search/?lat=19.8719294&long=-99.1367931

GET /api/search/?lat=19.8719294&long=-99.1367931&order=newer

GET /api/search/?lat=19.8719294&long=-99.1367931&order=older

GET /api/search/?lat=19.8719294&long=-99.1367931&order=better

GET /api/search/?lat=19.8719294&long=-99.1367931&order=worst

GET /api/search/?lat=19.8719294&long=-99.1367931&order=near

GET /api/search/?lat=19.8719294&long=-99.1367931&order=far
```

### Responses

#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description|
|-------|------|------------|
|count  |integer|total favorites number  |
|next|string|next page pagination link |
|previous|string|previous page pagination link|
|results|objects list|list of favorites|

**Favorites fields**

|Field  |Type  | Description|
|-------|------|------------|
|api_id  |string| favorite map id  |
|name|string|favorite name|
|place_id|string|favorite id|
|rating|decimal|favorite rating|
|vicinity|string|favorite address string|
|lat|decimal| favorite latitude|
|long|decimal|favorite longitude|
|creation_date|datetime|favorite creation date|
|distance|decimal|distance in meters between the favorite and the request lat and long|

**json response**  
```
{
  "count": 4,
  "next": "http://localhost:8000/api/favorites/?lat=19.4719294&limit=2&long=-99.1967931&offset=2",
  "previous": null,
  "results": [
    {
      "pk": 8,
      "api_id": "77cbfa939e1865ff49880765f853b8df69b0b59f",
      "name": "Centennial ballrooms",
      "place_id": "ChIJ-UlR64H40YURYL3t4Rca1gw",
      "rating": "2.4",
      "vicinity": "Centenario 367, Nextengo, Ciudad de México",
      "lat": "19.4716780",
      "long": "-99.1940690",
      "creation_date": "2018-11-28T11:13:04.153706Z",
      "distance": 287.35864780538105
    },
    {
      "pk": 7,
      "api_id": "8f6a9f9be6cf7c5c8d347de045ce6e577f7dc7ff",
      "name": "Walmart Azcapotzalco",
      "place_id": "ChIJO0lU038C0oUR260PKftz2r8",
      "rating": "3.2",
      "vicinity": "Calle Camino a Nextengo 78, Santa Cruz Acayucan, Ciudad de México",
      "lat": "19.4983580",
      "long": "-99.2921490",
      "creation_date": "2018-11-28T11:11:08.327673Z",
      "distance": 10429.495177022078
    }
  ]
}
```

#### 401 Unauthorized
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
HTTP/1.1 401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}
```

#### 400 Bad Request
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|lat  |error message|
|long  |error message|

**json response**  
```
HTTP/1.1 404 Bad Request
{
  "lat": [
    "This query param is required",
    "A valid number is required."
  ],
  "long": [
    "This query param is required",
    "A valid number is required."
  ]
}
```
---

## Detail
Favorite detail service endpoint  

**GET**  
**url** `/favorites/{id}/`
**receives** application/json  
**Authentication:**  Required  

#### Query Parameters

|Param    | Description    | Extra info|valid values|
|---------|----------------|-----------|------------|
|lat      |search latitude |required   |integer     |
|long     |search longitude|required   |integer     |

**request examples**  
```
GET
/api/favorites/{id}/?lat=19.4719294&long=-99.1967931
```
### Responses

#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description|
|-------|------|------------|
|api_id  |string| favorite map id  |
|name|string|favorite name|
|place_id|string|favorite id|
|rating|decimal|favorite rating|
|vicinity|string|favorite address string|
|lat|decimal| favorite latitude|
|long|decimal|favorite longitude|
|creation_date|datetime|favorite creation date|
|distance|decimal|distance in meters between the favorite and the request lat and long|

#### 401 Unauthorized
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
HTTP/1.1 401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}
```

#### 400 Bad Request
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|lat  |error message|
|long  |error message|

**json response**  
```
HTTP/1.1 404 Bad Request
{
  "lat": [
    "This query param is required",
    "A valid number is required."
  ],
  "long": [
    "This query param is required",
    "A valid number is required."
  ]
}
```

#### 404 Not Found
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
{
  "detail": "Not found."
}
```

---

## Create
Favorite creation service endpoint  

**POST**  
**url** `/favorites/`  
**receives:** application/json  
**Authentication:**  Required  

#### Query Parameters

|Param    | Description    | Extra info|valid values|
|---------|----------------|-----------|------------|
|lat      |search latitude |required   |integer     |
|long     |search longitude|required   |integer     |

#### Request Body Parameters

|Field  |Type  | Description| Extra info|
|-------|------|------------|--|
|api_id  |string| favorite map id  |required|
|name|string|favorite name|required|
|place_id|string|favorite id|required|
|rating|decimal|favorite rating||
|vicinity|string|favorite address string|required|
|lat|decimal| favorite latitude|required|
|long|decimal|favorite longitude|required|
|user_id|integer|creator user id|required|

**json example**  
```
POST /api/favorites/?lat=19.4719294&long=-99.1967931
{
  "api_id": "8f6a9f9be6cf7c5c8d347de045ce6e577f7dc7ff",
  "name": "Walmart Azcapotzalco",
  "place_id": "ChIJO0lU038C0oUR260PKftz2r8",
  "rating": "3.2",
  "vicinity": "Calle Camino a Nextengo 78, CDMX",
  "lat": "19.4983580",
  "long": "-99.2921490",
  "user_id": 2,
}
```

### Responses

#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description|
|-------|------|------------|
|pk|integer|created object pk|
|api_id  |string| favorite map id  |
|name|string|favorite name|
|place_id|string|favorite id|
|rating|decimal|favorite rating|
|vicinity|string|favorite address string|
|lat|decimal| favorite latitude|
|long|decimal|favorite longitude|
|creation_date|datetime|favorite creation date|
|distance|decimal|distance in meters between the favorite and the request lat and long|

**json response**
```
HTTP/1.1 201 Created
{
  "pk": 16,
  "api_id": "wertrey",
  "name": "asdf",
  "place_id": "qw3rerth",
  "rating": "2.5",
  "vicinity": "dsfg sdfg sdfg",
  "lat": "19.4983580",
  "long": "-99.2921490",
  "creation_date": "2018-12-01T09:01:06.782651Z",
  "distance": 10429.495177022078
}
```

#### 401 Unauthorized
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
HTTP/1.1 401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}
```

#### 400 Bad Request
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|lat  |error message|
|long  |error message|
|non_field_errors  |error message|

**json response**  
```
HTTP/1.1 400 Bad Request
{
  "lat": [
    "This query param is required",
    "A valid number is required."
  ],
  "long": [
    "This query param is required",
    "A valid number is required."
  ],
  "non_field_errors": [
    "The fields api_id, user must make a unique set."
  ]
}
```
---
## Delete
Favorite deletion service endpoint  

**DELETE**  
**url** `/favorites/{id}/`  
**receives:** application/json  
**Authentication:**  Required  

#### Query Parameters

 - No query parameters required

#### Request Body Parameters

 - No request body required

**json example**  

```
DELETE /api/favorites/{id}/
```

### Responses

#### 204 No Content
**returns:** application/json  
**Response fields**  
No body returned

#### 401 Unauthorized
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  

```
HTTP/1.1 401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found
**returns:** application/json  
**Response fields**

|Field  |Type  |
|-------|------|
|detail  |error message|

**json response**  
```
{
  "detail": "Not found."
}
```
