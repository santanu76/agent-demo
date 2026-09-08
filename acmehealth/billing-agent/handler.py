"""Stand-in for Acme Health's OWN, pre-existing billing agent — the "onboard
an external agent from the customer's git" test fixture. This file is
deliberately NOT built on AiGenie: it's a plain Lambda Function URL
speaking the OpenAI-compatible chat shape (same contract
local/demo_acmehealth_agent.py's CareLine uses locally), deployed with its
own minimal execution role that has zero access to any AiGenie
control-plane resource — same trust boundary a real customer's own
infrastructure would have. AiGenie's Hub calls this over HTTPS exactly the
way it would call anything a real customer deployed from their own repo;
onboarding it is purely a Hub Agent Registry entry (openai_chat mapping),
zero changes to this file.

Deployed by local/deploy_acmehealth_demo_agent.py, not infra/deploy.py —
this is a test fixture simulating a customer's own system, not a component
of AiGenie's own platform, so it deliberately isn't tracked in AiGenie's
managed infra/Terraform state.
"""
import json
import os
import urllib.request

SYSTEM = (
    "You are Acme Health's billing support agent. Answer questions about "
    "invoices, payment plans and insurance claims status — concise, "
    "practical, reassuring. You cannot access a specific patient's real "
    "billing record; if asked for one, direct them to call billing at "
    "1-800-555-ACME. Never invent a specific dollar amount or claim status."
)


def _answer(messages: list[dict]) -> str:
    key = os.environ.get("LLM_API_KEY", "")
    base = os.environ.get("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b")
    if not key:
        return ("Billing support is offline right now — please call "
                "1-800-555-ACME or try again shortly.")
    req = urllib.request.Request(
        f"{base.rstrip('/')}/chat/completions",
        data=json.dumps({
            "model": model, "temperature": 0.3, "max_tokens": 400,
            "messages": [{"role": "system", "content": SYSTEM}] + messages,
        }).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key}",
                 "User-Agent": "acmehealth-billing-agent/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"].strip()


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        if event.get("isBase64Encoded"):
            import base64
            body = json.loads(base64.b64decode(event["body"]).decode())
        messages = [m for m in body.get("messages", [])
                   if m.get("role") in ("system", "user", "assistant")]
        text = _answer(messages)
    except Exception as exc:  # their agent, their honesty
        text = f"Sorry — I couldn't reach my billing system ({exc})."
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"choices": [{"message": {"content": text}}]}),
    }
