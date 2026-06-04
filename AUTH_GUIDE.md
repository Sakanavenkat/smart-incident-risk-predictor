# Authentication Guide

## Overview

The Smart Incident Risk Predictor uses JWT (JSON Web Token) based authentication with role-based access control (RBAC).

### Roles

1. **Admin (role_id: 1)** - Full system access, can manage users
2. **Manager (role_id: 2)** - Can upload tickets, view reports
3. **User (role_id: 3)** - Can view dashboards, read-only access

---

## Default Test Accounts

After running `install.bat` and starting the server, the following accounts are automatically created:

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | Admin@123456 | Admin |
| manager@example.com | Manager@123456 | Manager |
| user@example.com | User@123456 | User |

⚠️ **IMPORTANT**: Change these passwords in production!

---

## API Endpoints

### Authentication Endpoints

#### 1. Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": 4,
  "email": "newuser@example.com",
  "full_name": "John Doe",
  "role": {
    "id": 3,
    "name": "user"
  }
}
```

**Errors:**
- 400: Password too short (min 8 chars) or passwords don't match
- 409: User already exists

---

#### 2. Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "Admin@123456"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "full_name": "Administrator",
    "role": {
      "id": 1,
      "name": "admin"
    }
  }
}
```

**Errors:**
- 401: Invalid email or password

---

#### 3. Logout
```http
POST /api/auth/logout
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

### User Management Endpoints (Admin Only)

#### 1. List All Users
```http
GET /api/users?skip=0&limit=100
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "full_name": "Administrator",
    "role": {
      "id": 1,
      "name": "admin"
    }
  },
  ...
]
```

---

#### 2. Get User by ID
```http
GET /api/users/1
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "full_name": "Administrator",
  "role": {
    "id": 1,
    "name": "admin"
  }
}
```

---

#### 3. Update User Role
```http
PUT /api/users/3/role?role_id=2
Authorization: Bearer <access_token>
```

**Role IDs:**
- 1: Admin
- 2: Manager
- 3: User

**Response (200):**
```json
{
  "id": 3,
  "email": "user@example.com",
  "full_name": "Sample User",
  "role": {
    "id": 2,
    "name": "manager"
  }
}
```

---

#### 4. Delete User
```http
DELETE /api/users/3
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "User deleted successfully"
}
```

---

## Using the Token in Requests

### Include Token in Authorization Header

All protected endpoints require the JWT token in the Authorization header:

```http
GET /api/tickets
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- Access tokens expire after **60 minutes**
- When expired, user must login again to get a new token

---

## Testing with curl

### 1. Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPass123",
    "password_confirm": "TestPass123",
    "full_name": "Test User"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "Admin@123456"
  }'
```

### 3. List Users (Admin Only)
```bash
curl -X GET "http://localhost:8000/api/users" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## Testing with Postman

1. Open Postman
2. Create a new request
3. Set method to `POST` and URL to `http://localhost:8000/api/auth/login`
4. In **Body** tab, select **raw** and **JSON**:
   ```json
   {
     "email": "admin@example.com",
     "password": "Admin@123456"
   }
   ```
5. Send request and copy the `access_token` from response
6. For subsequent requests:
   - Go to **Auth** tab
   - Select **Bearer Token**
   - Paste the token

---

## Testing with FastAPI Docs

1. Start the backend: `run.bat` (Windows) or `bash run.sh` (Unix)
2. Navigate to `http://localhost:8000/docs`
3. Click **Authorize** button (top right)
4. In the popup, enter only the token (without "Bearer "):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
5. Click **Authorize**
6. Now all protected endpoints are unlocked in the UI

---

## Security Best Practices

1. **Always use HTTPS in production** (not HTTP)
2. **Change default passwords** before deploying
3. **Keep tokens secure** - never share in logs or version control
4. **Set strong passwords** - minimum 8 characters, mix of upper/lower case, numbers
5. **Rotate tokens** - implement token refresh mechanism for long-lived sessions
6. **Use environment variables** for SECRET_KEY (not hardcoded)
7. **Implement rate limiting** on login to prevent brute force attacks
8. **Log all authentication events** for audit trail

---

## Troubleshooting

### "Invalid token" Error

**Problem:** Token has expired or is malformed.
**Solution:** Login again to get a new token.

### "Admin access required" Error

**Problem:** User role is not Admin.
**Solution:** Ask an admin to promote your account or use admin account.

### "Not authenticated" Error

**Problem:** Authorization header is missing or invalid.
**Solution:** Include `Authorization: Bearer <token>` header in request.

---

## Next Steps

Once authentication is working:
1. Use authenticated tokens for Ticket Upload API
2. Implement role-based checks on file upload endpoints
3. Add audit logging for user actions
