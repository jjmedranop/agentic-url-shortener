# Architecture Overview: Agentic SDLC Orchestrator

## 1. Design & Control Flow Rationale
To provide reliable, stateful automation of our URL Shortener application lifecycle, we selected **LangGraph** as our core runtime framework over a standard linear pipeline approach. 

### Why LangGraph?
* **Cyclic Path Support:** Software engineering is inherently non-linear. If code fails integration testing, it must rollback or loop back to repair cycles. LangGraph manages cyclic directed graphs easily.
* **Traceable Lineage & Shared State:** The `SDLCState` acts as a unified source of truth passing payload modifications, error logs, and metrics across isolated agent execution environments.

## 2. System Topology Visual Model
Below is the structural operational model mapping control data behavior between stages:

[Requirement Input]
│
▼
┌──────────────────┐
│   Requirements   │ ──(If Ambiguous)──► [Early Termination Stop]
│       Node       │
└──────────────────┘
│
▼
┌──────────────────┐
│    Coder Node    │ ◄─────────────────┐
└──────────────────┘                   │
│                            │
▼                    (If Test Fails & < 3 Retries)
┌──────────────────┐                   │
│   Tester Node    │ ──────────────────┘
└──────────────────┘
│
(If Test Passes)
│
▼
┌──────────────────┐
│  Human Approval  │ ──(Rejected)──► [Aborted Operations]
│    Check Gate    │
└──────────────────┘
│
(Approved)
│
▼
[Production Release]

## 3. Policy Guardrails & Risk Management Controls
* **Bounded Loop Recovery Thresholds:** The `route_after_testing` condition strictly enforces a max threshold boundary of **3 execution loops**. If an AI agent cannot fix its code compilation errors within 3 attempts, it throws an exception and halts execution to protect computing resource overhead.
* **Human-in-the-Loop Gateways:** High-impact runtime actions (file compilation rewrites and production container staging steps) cannot execute implicitly. The system halts on a text stream hook requiring an explicit terminal input verification flag.
* **Failure Resiliency:** Database state or system crashes mid-execution preserve contextual sta