### Ticket selling application
Django REST API with the endpoints to list Events, Tickets and TicketTypes and POST requests to buy a ticket for the specific Event.
Tickets can be either reserved (for 15 minutes) or bought.

## Deployment
1. With Docker.

```
$ docker-compose build
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate
$ docker-compose up -d
```
The app is running at http://0.0.0.0:8000


## API endpoints

1. /api/event/
- **Method:** GET
- **Call:**  `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/event/"`

2. /api/event/pk	
- **Method:** GET
- **Call**: `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/event/1"`

3. /api/tickets/
- **Method:** GET
- **Call:** `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/tickets/"`

4. /api/tickets/pk
- **Method:** GET
- **Call:** `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/tickets/1"`

4. /api/ticket-type/
- **Method:** GET
- **Call:** `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/ticket-type/"`

5. /api/ticket-type/pk
- **Method:** GET
- **Call:** `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "http://0.0.0.0:8000/api/ticket-type/pk"`

6. /api/ticket/purchase
- **Method**: POST
- **Call**: `curl -H "Accept: Application/json" -H "Content-Type: application/json" -d '{"ticket":34, "quantity":2, "email":"test-email@wp.pl"}' -X POST http://0.0.0.0:8000/api/ticket/purchase/`

7. /api/ticket/purchase/pk
- **Method**: GET
- **Call**: `curl -H "Accept: Application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:8000/api/ticket/purchase/54`

8. /api/ticket/purchase/pk
- **Method**: PUT
- **Call**: `curl -H "Accept: Application/json" -H "Content-Type: application/json" -d '{"quantity":4}' -X PUT http://0.0.0.0:8000/api/ticket/purchase/54`

9. /api/ticket/purchase/pk
- **Method**: POST
- **Call**: `curl -H "Accept: Application/json" -H "Content-Type: application/json" -d '{"amount": 100.00, "token": "valid_card"}' -X POST http://0.0.0.0:8000/api/ticket/purchase/54`
- **Description:** Endpoint to validate the payment and change purchase status to paid.

## Tests
Test module can be found in `tickets_selling/tickets/tests/` folder. To run the test use:
```
$ docker-compose run web python manage.py test
```
