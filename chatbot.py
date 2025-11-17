# chatbot.py
from typing import Dict, Any
from pyDatalog import pyDatalog
from logic_layer import response, escalate, fallback  # predicates
from nlu import match_intent, extract_entities

def format_escalation(intent: str, reason: str, entities: Dict[str, Any]) -> str:
    e_str = ', '.join(f'{k}={v}' for k, v in entities.items()) or 'none'
    return (
        f"I’m escalating this to a human support specialist "
        f"(intent={intent}, reason={reason}, entities={e_str}). "
        f"You’ll be contacted shortly. Meanwhile, please share any relevant IDs or screenshots."
    )

def handle_query(text: str) -> str:
    intent, conf = match_intent(text)
    entities = extract_entities(text)

    # If we can't infer an intent at all, escalate on low confidence
    if not intent:
        return format_escalation('unknown', 'low_confidence', entities)

    # Check rule-based escalation conditions
    esc_result = pyDatalog.ask(f'escalate("{intent}", {conf}, Reason)')
    esc_rows = esc_result.answers if esc_result else []
    if esc_rows:
        reason = esc_rows[0][0]  # Reason bound by the rule
        return format_escalation(intent, reason, entities)

    # If no escalation, try to retrieve a response
    # Prefer entity-specific responses if you choose to add them later
    resp_result = pyDatalog.ask(f'response("{intent}", Text)')
    rows = resp_result.answers if resp_result else []
    if rows:
        base = rows[0][0]
        # Lightweight personalization based on entities
        if intent == 'order_status' and 'order_id' in entities:
            return f"{base} I can see your order ID: {entities['order_id']}. I’ll check and update you."
        return base

    # If intent exists but no response rule, use fallback + escalate
    fb_result = pyDatalog.ask(f'fallback("{intent}")')
    fb = fb_result.answers if fb_result else []
    if fb:
        return format_escalation(intent, 'no_defined_response', entities)

    # Safety net
    return format_escalation('unknown', 'unhandled_case', entities)

if __name__ == '__main__':
    print("Support bot ready. Type your question (Ctrl+C to exit).")
    try:
        while True:
            user = input("> ").strip()
            if not user:
                continue
            print(handle_query(user))
    except KeyboardInterrupt:
        print("\nGoodbye.")
