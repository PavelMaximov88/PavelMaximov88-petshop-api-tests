PET_SCHEMA = {
  "type": "object",
  "properties": {
        "id": {
        "type": "integer"
    },
        "name": {
        "type": "string"
    },
    "category": {
        "type": ["object", 'null'],
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": False
    },
    "photoUrls": {
      "type": ["array", 'null'],
      "items": {
        "type": "string"
      }
    },
    "tags": {
      "type": ["array", 'null'],
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          }
        },
        "required": ["id", "name"],
        "additionalProperties": False
      }
    },
    "status": {
      "type": "string",
      "enum": ["available", "pending", "sold"]
    }
  },
  "required": ["id", "name", "photoUrls", "status"],
  "additionalProperties": False
}