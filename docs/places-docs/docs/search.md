# Search places service

This is the api's main service

This service allows to find places according to a pir of coordinates

---
## Search
Search service endpoint  
**GET**  
**url** `/search/`  
**receives** application/json  
**Authentication:**  Required
#### Query Parameters  
|Param    | Description    | Extra info|valid values|
|---------|----------------|-----------|------------|
|lat      |search latitude |required   |integer     |
|long     |search longitude|required   |integer     |
|keyword  |search keyword  |           |string      |
|order   |search order value  |           |'distance'  |
|next_page_token   |pagination token  |is a really long string|string |

**request examples**  
```
GET /api/search/?lat=19.8719294&long=-99.1367931

GET /api/search/?lat=19.8719294&long=-99.1367931&keyword=comida

GET /api/search/?lat=19.8719294&long=-99.1367931&order=distance

GET /api/search/?lat=19.8719294&long=-99.1367931&order=distance&keyword=tacos

```

### Responses

#### 200 Success
**returns:** application/json  
**Response fields**

|Field  |Type  | Description| Extra Info |
|-------|------|------------|--|
|next_page_token  |string|pagination token  | optional |
|places|objects list|list of places| |

**Places fields**

|Field  |Type  | Description|
|-------|------|------------|
|api_id  |string| place map id  |
|name|string|place name|
|place_id|string|place id|
|rating|decimal|place rating|
|vicinity|string|place address string|
|lat|decimal| place latitude|
|long|decimal|place longitude|
|distance|decimal|distance in meters between the place and the request lat and long|

**json response**
```
HTTP/1.1 200 OK
{
  "next_page_token": "CrQCKgEAA...BEZo6cWvu75Zc",
  "places": [
    {
      "api_id": "77cbfa939e1865ff49880765f853b8df69b0b59f",
      "name": "Centennial ballrooms",
      "place_id": "ChIJ-UlR64H40YURYL3t4Rca1gw",
      "rating": "4.1",
      "vicinity": "Centenario 367, Nextengo, Ciudad de México",
      "lat": "19.4730008",
      "long": "-99.1885226",
      "distance": 876.39256601346
    },
    {
      "api_id": "5921d83485fbce6c2d04445d65a048b399dc6806",
      "name": "Bicentennial Park Skatepark",
      "place_id": "ChIJR2Yx83kC0oURs3kgnNCL91s",
      "rating": "4.6",
      "vicinity": "Av. 5 de Mayo 290, San Lorenzo Tlaltenango, Miguel Hidalgo",
      "lat": "19.4670980",
      "long": "-99.1949826",
      "distance": 567.6020735119857
    },
    {
      "api_id": "5308550773d180024315638162a2009619ff069d",
      "name": "Seca",
      "place_id": "ChIJFyytPlv40YUR-OsLx-bsnLs",
      "rating": "4.9",
      "vicinity": "Centeotl 223-A, San Antonio, Azcapotzalco",
      "lat": "19.4775198",
      "long": "-99.1963905",
      "distance": 620.2868702074812
    },
    ...
    {
      "api_id": "8f6a9f9be6cf7c5c8d347de045ce6e577f7dc7ff",
      "name": "Walmart Azcapotzalco",
      "place_id": "ChIJO0lU038C0oUR260PKftz2r8",
      "rating": "4.0",
      "vicinity": "Calle Camino a Nextengo 78, Santa Cruz Acayucan, Ciudad de México",
      "lat": "19.4728407",
      "long": "-99.1925539",
      "distance": 456.36835393052377
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
HTTP/1.1 400 Bad Request
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
