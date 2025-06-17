**# Candidate Management API Documentation**

This document provides an overview of the available endpoints for managing candidate data, including their paths, descriptions, and example usages in JavaScript.

---

## 1. `GET /api/`

* **Path:** `/api/`
* **Description:** Root endpoint that returns a greeting message.
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/')
  .then(response => response.json())
  .then(data => console.log(data));
// Output: { message: "Hello World" }
```

---

## 2. `GET /api/health`

* **Path:** `/api/health`
* **Description:** Health check endpoint that returns the status of the application.
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/health')
  .then(response => response.json())
  .then(data => console.log(data));
// Output: { status: "ok" }
```

---

## 3. `GET /api/mongo`

* **Path:** `/api/mongo`
* **Description:** Verifies MongoDB connectivity by pinging the database.
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/mongo')
  .then(response => response.json())
  .then(data => console.log(data));
// Output when Mongo is running:
// { status: "ok", data: { message: "MongoDB is running" } }
```

---

## 4. `POST /api/mongo/get_candidate`

* **Path:** `/api/mongo/get_candidate`
* **Description:** Retrieves one or multiple candidates filtered by specialization. If no specialization is provided, returns all candidates.
* **Request Body:**

  ```json
  { "specialization": "<specialization>" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/mongo/get_candidate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ specialization: 'Data Science' })
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: [ { _id: "60f...", name: "Alice", ... } ] }
```

---

## 5. `POST /api/create_candidate`

* **Path:** `/api/create_candidate`
* **Description:** Creates a new candidate entry in the database. Validates the provided candidate data.
* **Request Body:**

  ```json
  {
    "candidate": {
      "name": "Alice",
      "email": "alice@example.com",
      "nationality": "USA",
      "phone": "123-456-7890",
      "education": "MSc Computer Science",
      "years_of_experience": 5,
      "specialization": "Backend Development",
      "DOB": "1990-05-12"
    }
  }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/create_candidate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ candidate: {
    name: 'Alice',
    email: 'alice@example.com',
    nationality: 'USA',
    phone: '123-456-7890',
    education: 'MSc Computer Science',
    years_of_experience: 5,
    specialization: 'Backend Development',
    DOB: '1990-05-12'
    skills: ["Python", "Django", "SQL"]
    CVPath: "..."
  } })
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { name: "Alice", ... } }
```

---

## 6. `POST /api/search_candidate`

* **Path:** `/api/search_candidate`
* **Description:** Searches for candidates matching a query string against multiple fields (name, email, phone, etc.). If no query is provided, falls back to `/api/mongo/get_candidate` behavior.
* **Request Body:**

  ```json
  { "query": "Alice" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/search_candidate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Alice' })
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: [ { _id: "60f...", name: "Alice", ... } ] }
```

---

## 7. `POST /api/generate_visitor_account`

* **Path:** `/api/generate_visitor_account`
* **Description:** Generates a visitor account with a random username and password.
* **Request Body:**

  ```json
  { "username": "<username>", "days": <days> }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/generate_visitor_account', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'visitor123', days: 7 })
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { user: { username: "visitor123", password: "..." } } }
```

---

## 8. `POST /api/login`

* **Path:** `/api/login`
* **Description:** Logs in a user by verifying their username and password.
* **Request Body:**

  ```json
  { "username": "<username>", "password": "<password>" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'visitor123', password: '...'})
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { token: "..." } }
```

---

## 9. `POST /api/is_logged_in`

* **Path:** `/api/is_logged_in`
* **Description:** Checks if a user is logged in by verifying their access token.
* **Request Body:**

  ```json
  { "token": "<token>" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/is_logged_in', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token: '...'})
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { is_logged_in: true } }
```

---

## 10. `POST /api/logout`

* **Path:** `/api/logout`
* **Description:** Logs out a user by revoking their access token.
* **Request Body:**

  ```json
  { "token": "<token>" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/logout', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token: '...'})
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { token: null } }
```

---

## 11. `POST /api/mongo/download_cv`

* **Path:** `/api/mongo/download_cv`
* **Description:** Downloads a candidate's CV file.
* **Request Body:**

  ```json
  { "id": "<candidate_id>" }
  ```
* **Example (JavaScript):**

```javascript
fetch('https://localhost/api/mongo/download_cv', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: '...'})
})
  .then(res => res.json())
  .then(data => console.log(data));
// Output:
// { status: "ok", data: { CVPath: "..." } }
```

---

*End of documentation.*
