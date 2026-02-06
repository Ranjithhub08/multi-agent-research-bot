# 📡 API Reference

The backend provides a RESTful interface for agentic orchestration.

## Base URL
`http://localhost:8080/api`

## Endpoints

### 1. Initiate Research
`POST /research`

Triggers the full multi-agent swarm sequence for a specific topic.

**Request Body:**
```json
{
  "topic": "Future of Quantum Computing"
}
```

**Response Body (200 OK):**
```json
{
  "finalReport": "# Research Report: Future of Quantum Computing\n...",
  "agentLogs": [
    { "agent": "Researcher", "message": "Identified 12 sources..." },
    { "agent": "Critic", "message": "Validated 9 sources..." }
  ]
}
```

### 2. Health Check
`GET /health`

Returns the status of the backend and AI services.

---

## 🛡️ Error Handling

The API uses standard HTTP status codes:
- `200`: Success.
- `400`: Bad Request (invalid topic).
- `500`: Internal Server Error (usually AI provider downtime).

*Note: The Frontend gracefully handles 500 or connection errors by switching to Autonomous Simulation Mode.*
