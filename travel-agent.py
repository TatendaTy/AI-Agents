import json
import requests

def ollama_chat(messages, model="granite3.3:latest", base_url="http://localhost:11434"):
    """
    Sends a chat completion request to a local Ollama server using /api/generate.
    """
    url = f"{base_url}/api/generate"
    # Concatenate messages for context as a single prompt string
    prompt = ""
    for m in messages:
        if m["role"] == "system":
            prompt += f"System: {m['content']}\n"
        elif m["role"] == "user":
            prompt += f"User: {m['content']}\n"
        elif m["role"] == "assistant":
            prompt += f"Assistant: {m['content']}\n"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["response"]

def book_flight(passenger_name: str,
                from_city: str,
                to_city: str,
                travel_date: str) -> str:
    return f"A {travel_date} flight has been booked from {from_city} to {to_city} for {passenger_name}"

def travel_agent(user_message: str, messages: list) -> str:
    messages.append({"role": "user", "content": user_message})
    response = ollama_chat(messages)
    # Simple function call detection (customize as needed)
    if "book a flight" in response.lower():
        # Try to extract details from the conversation history
        # (In production, use a more robust extraction method)
        passenger_name = "John Doe"  # Placeholder: extract from messages
        from_city = "Los Angeles"    # Placeholder: extract from messages
        to_city = "New York"         # Placeholder: extract from messages
        travel_date = "2024-06-01"   # Placeholder: extract from messages
        confirmation = book_flight(passenger_name, from_city, to_city, travel_date)
        messages.append({"role": "assistant", "content": confirmation})
        return confirmation
    else:
        messages.append({"role": "assistant", "content": response})
        return response

# Example usage:
messages = [
    {"role": "system", "content": "You are a helpful travel agent assistant. If the user wants to book a flight, ask for all details and then say 'book a flight' with the details."}
]
user_input = "I want to book a flight from Los Angeles to New York on June 1st for John Doe."
result = travel_agent(user_input, messages)
print(result)