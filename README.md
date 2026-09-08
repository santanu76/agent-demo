# agent-demo

Demo repo used to show two ways a customer's agent code relates to AiGenie:

- **`acmehealth/billing-agent/`** — Acme Health's own, pre-existing billing
  agent. Not built on AiGenie; it speaks a plain OpenAI-compatible chat API.
  This is the "Scenario A" fixture: onboarding an agent whose code already
  lives in the customer's own git, by registering its deployed endpoint in
  AiGenie Hub's Agent Registry as an external/BYO agent. Nothing in this
  file changes when it's onboarded.

- **Everything AiGenie generates for you** lands here as a pull request —
  never a direct push, including the very first one. That's "Scenario B":
  create a new agent in AiGenie Hub, and its generated workspace arrives
  here as a PR for you to review and merge yourself.
