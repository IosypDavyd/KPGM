# KPGM API Documentation

## Overview

KPGM (KEYPOWERGRAILMYSTERY) Music Video Generator API provides endpoints for generating music and videos using AI.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All protected endpoints require JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register

```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}

Response (201):
{
  "message": "User registered successfully",
  "user_id": "uuid",
  "email": "user@example.com"
}
```

#### Login

```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}

Response (200):
{
  "message": "Login successful",
  "access_token": "jwt_token",
  "user_id": "uuid",
  "email": "user@example.com"
}
```

### Music & Video Generation

#### Generate Music and Video

```
POST /generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "upbeat electronic music with synths",
  "style": "electronic",
  "duration": 60,
  "video": true,
  "video_style": "cinematic",
  "project_name": "My Project"
}

Response (202):
{
  "project_id": "uuid",
  "status": "processing",
  "message": "Music and video generation started",
  "progress": 0
}
```

#### Get Generation Status

```
GET /generate/<project_id>/status
Authorization: Bearer <token>

Response (200):
{
  "project_id": "uuid",
  "status": "processing",
  "progress": 50,
  "music_url": "https://...",
  "video_url": null,
  "created_at": "2026-07-18T...",
  "updated_at": "2026-07-18T..."
}
```

### Projects

#### List Projects

```
GET /projects
Authorization: Bearer <token>

Response (200):
{
  "projects": [
    {
      "id": "uuid",
      "name": "My Project",
      "status": "completed",
      "music_url": "https://...",
      "video_url": "https://...",
      "created_at": "2026-07-18T..."
    }
  ]
}
```

#### Get Project Details

```
GET /projects/<project_id>
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "name": "My Project",
  "status": "completed",
  "progress": 100,
  "music_prompt": "upbeat electronic music",
  "music_style": "electronic",
  "duration": 60,
  "music_url": "https://...",
  "video_url": "https://...",
  "created_at": "2026-07-18T...",
  "updated_at": "2026-07-18T..."
}
```

#### Delete Project

```
DELETE /projects/<project_id>
Authorization: Bearer <token>

Response (200):
{
  "message": "Project deleted successfully"
}
```

### Styles

#### Get Music Styles

```
GET /music/styles

Response (200):
{
  "styles": [
    "ambient",
    "electronic",
    "pop",
    "rock",
    ...
  ]
}
```

#### Get Video Styles

```
GET /video/styles

Response (200):
{
  "styles": [
    "cinematic",
    "abstract",
    "nature",
    ...
  ]
}
```

## Error Responses

```
400 Bad Request
{
  "error": "Bad Request",
  "message": "Description of the error"
}

401 Unauthorized
{
  "error": "Unauthorized",
  "message": "Authentication required"
}

404 Not Found
{
  "error": "Not Found",
  "message": "The requested resource does not exist"
}

500 Internal Server Error
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting

- Default rate limit: 100 requests per hour per user
- Music generation: 10 per day
- Video generation: 5 per day

## WebSockets

For real-time status updates, connect to:

```
ws://localhost:5000/ws/project/<project_id>
```
