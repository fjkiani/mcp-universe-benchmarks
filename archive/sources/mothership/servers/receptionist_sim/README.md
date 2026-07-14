# Receptionist Simulator MCP Server

This MCP server provides an interface to a virtual receptionist that can handle appointment bookings for haircut services. The receptionist uses AI-powered intent classification to understand natural language conversations.

## Overview

The Receptionist Simulator simulates a front desk receptionist at a hair salon. It can handle various customer interactions including:

- Greeting customers
- Providing service information and pricing
- Showing available appointment slots
- Processing bookings with customer details
- Handling deposits for weekend appointments
- Managing rescheduling and cancellations

## Features

- **Natural Language Understanding**: Uses GPT-4o-mini for intent classification
- **State Management**: Maintains booking state throughout the conversation
- **Multi-Session Support**: Can handle multiple concurrent booking sessions
- **Deposit Handling**: Requires deposits for weekend appointments
- **Flexible Scheduling**: Offers predefined time slots across multiple days

## Tools

### 1. `start_session`

Start a new receptionist session.

- **Input**:
  - `session_id` (optional string): Session identifier. Defaults to 'default'
- **Returns**: Initial greeting and session state

### 2. `send_message`

Send a message to the receptionist and receive a response.

- **Input**:
  - `message` (string): The message to send
  - `session_id` (optional string): Session identifier. Defaults to 'default'
- **Returns**: Receptionist's response, current state, and booking status

### 3. `get_session_state`

Get the current state of a booking session.

- **Input**:
  - `session_id` (optional string): Session identifier. Defaults to 'default'
- **Returns**: Current booking state, available slots, and deposit requirements

### 4. `reset_session`

Reset a receptionist session to start fresh.

- **Input**:
  - `session_id` (optional string): Session identifier. Defaults to 'default'
- **Returns**: Confirmation and reset state

### 5. `list_sessions`

List all active receptionist sessions.

- **Returns**: List of sessions with their booking status and details

## Resources

### 1. `receptionist://demo`

Provides a sample conversation demonstrating the receptionist's capabilities.

### 2. `receptionist://capabilities`

Detailed information about the receptionist's features and supported intents.

## Supported Intents

The receptionist can understand and respond to:

- **greet**: Respond to greetings
- **ask_availability**: Show available time slots
- **pick_slot**: Select a specific time slot
- **provide_name**: Capture customer name
- **provide_phone**: Capture customer phone number
- **ask_price**: Provide pricing information
- **pay**: Process deposit payment
- **confirm**: Finalize the booking
- **reschedule**: Change appointment time
- **cancel**: Cancel appointment

## Service Details

- **Service**: Haircut
- **Price**: 70,000 Gs
- **Duration**: ~30 minutes
- **Deposit**: 20,000 Gs (required for weekend bookings)

## Available Time Slots

- Thursday 15:00
- Thursday 16:00
- Friday 14:00
- Saturday 11:00 (deposit required)

## Usage Example

```python
# Start a new session
response = start_session()
# Returns: {"session_id": "default", "message": "Hi! This is the front desk...", "state": {...}}

# Send a message
response = send_message("I'd like to book a haircut")
# Returns: {"message": "We have openings: [1] Thu 15:00...", "state": {...}}

# Pick a slot
response = send_message("I'll take Saturday at 11")
# Returns: {"message": "I can hold Sat 11:00. A 20,000 Gs deposit is required...", ...}

# Continue the conversation...
```

## Requirements

- Python 3.7+
- OpenAI API key (for intent classification)
- Dependencies: `openai`, `mcp`, `click`

## Notes

- The intent classifier requires an OpenAI API key to function
- Sessions are stored in memory and will be lost on server restart
- The receptionist follows a structured conversation flow for bookings
- Weekend appointments automatically require deposits
