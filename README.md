#  IP Info Lookup System with Django, Celery, Redis, WebSockets & JWT

This project provides an asynchronous system to submit IP addresses, process them using Celery workers, and stream real-time results back to authenticated users via WebSocket (Channels) with JWT authentication.

---

##  Features

- ✅ Submit multiple IPs via REST API
- ✅ Background processing using Celery + Redis
- ✅ Store IP geolocation info in PostgreSQL
- ✅ Real-time updates via Django Channels WebSocket (per-user)
- ✅ JWT Authentication using SimpleJWT
- ✅ WebSocket message isolation: each user only sees their own IP results
- ✅ Unit & WebSocket testing with `pytest`

---

Postman: ipinfo
[https://documenter.getpostman.com/view/30167640/2sB2xFg8Rv]

