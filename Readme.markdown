# Conversation API

## Overview
This FastAPI application provides endpoints to retrieve chat conversations stored in a Supabase database table named `conversationmemories`. The table contains columns: `id`, `created_at`, `user_message`, `assistant_message`, `sender` (phone number), `recipient`, and `name`. Conversations are grouped by `sender` for easy access, and unique sender phone numbers are listed.

## Setup
1. **Dependencies**:
   - Install required packages:
     ```bash
     pip install fastapi uvicorn supabase python-dotenv
     ```
2. **Environment Variables**:
   - Create a `.env` file in the project directory with:
     ```env
     SUPABASE_URL=your-supabase-url
     SUPABASE_KEY=your-supabase-key
     ```
3. **Run the Server**:
   - Save the code in `main.py` and run:
     ```bash
     uvicorn main:app --reload
     ```
   - The API will be available at `http://127.0.0.1:8000`.

## Database Schema
The `conversationmemories` table in Supabase has the following columns:
- `id`: Integer, unique identifier for each conversation.
- `created_at`: String, timestamp of the conversation.
- `user_message`: String, message sent by the user.
- `assistant_message`: String, response from the bot.
- `sender`: String, user’s phone number (e.g., `923400957795`).
- `recipient`: String, bot’s phone number.
- `name`: String, user’s name.

## Endpoints

### 1. GET `/conversations`
Fetches all conversations, grouped by `sender` (phone number), and lists unique sender phone numbers.

- **Response**:
  ```json
  {
    "unique_senders": ["923400957795", "9876543210"],
    "conversations": [
      {
        "sender": "923400957795",
        "name": "John Doe",
        "conversations": [
          {
            "id": 1,
            "created_at": "2025-08-06T05:48:00Z",
            "user_message": "Hello, bot!",
            "assistant_message": "Hi! How can I help?",
            "sender": "923400957795",
            "recipient": "bot_number",
            "name": "John Doe"
          },
          ...
        ]
      },
      ...
    ],
    "last_updated": "2025-08-06 11:03:00"
  }
  ```
- **Errors**:
  - `404`: `"No conversations found"` if the table is empty.
  - `500`: `"Error fetching conversations: <error>"` for server issues.

### 2. GET `/conversations/phone/{phone}`
Fetches conversations for a specific phone number.

- **Parameters**:
  - `phone` (path): Phone number (e.g., `923400957795`).
- **Response**:
  ```json
  {
    "conversations": [
      {
        "sender": "923400957795",
        "name": "John Doe",
        "conversations": [
          {
            "id": 1,
            "created_at": "2025-08-06T05:48:00Z",
            "user_message": "Hello, bot!",
            "assistant_message": "Hi! How can I help?",
            "sender": "923400957795",
            "recipient": "bot_number",
            "name": "John Doe"
          },
          ...
        ]
      }
    ],
    "last_updated": "2025-08-06 11:03:00"
  }
  ```
- **Errors**:
  - `404`: `"No conversations found for <phone>"` if no conversations exist.
  - `500`: `"Error fetching conversations: <error>"` for server issues.

## Usage
- **Test Endpoints**:
  ```bash
  curl http://127.0.0.1:8000/conversations
  curl http://127.0.0.1:8000/conversations/phone/923400957795
  ```
- **Time Zone**: The `last_updated` field reflects the server’s time (e.g., 11:03 AM PKT, August 06, 2025). Set `TZ=Asia/Karachi` for PKT:
  ```bash
  export TZ=Asia/Karachi
  ```

## Notes
- **Phone Number Format**: The `sender` column must match the input phone number exactly (e.g., `923400957795`).
- **Security**: Enable Row-Level Security (RLS) in Supabase:
  ```sql
  ALTER TABLE conversationmemories ENABLE ROW LEVEL SECURITY;
  CREATE POLICY user_access ON conversationmemories USING (sender = auth.uid());
  ```
- **Context**: Designed for a WhatsApp chatbot for `petalnex.com`. For xAI API integration, see https://x.ai/api.
- **Troubleshooting**:
  - Check `sender` values: `SELECT DISTINCT sender FROM conversationmemories;`.
  - Verify Supabase credentials and table name.
  - Check server logs for errors.