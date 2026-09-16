# Telco Voice Central — System Architecture Specification

**Document Version:** 1.0.0  
**Target Platform:** Google Customer Engagement Suite (CES / CXAS)  
**Agent Model:** `gemini-3.5-flash`  
**Modality:** Native Audio / Voice First  
**Application ID:** `projects/fde-bootcamp/locations/us/apps/a2630043-2939-46be-93b2-daef4c7fd3e8`  

---

## 1. Architecture Pillars

As outlined in the core system architecture guidelines, Telco Voice Central is engineered around three foundational pillars:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    THREE ARCHITECTURE PILLARS                                    │
├───────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│   Detailed Visual Diagrams    │        Defined Subagents         │    Step-by-Step Data Flow     │
│ Designing the structural      │ Modularizing complex flows into  │ Mapping the complete query    │
│ layout, modeling boundaries,  │ isolated subagents, strictly     │ lifecycle from client prompt  │
│ external tool integrations,   │ separating Billing from Tech     │ to orchestrator, runner, tool │
│ and session relationships.    │ Support, Sales, and Identity.    │ execution, and back.          │
└───────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

---

## 2. High-Level Execution Trace (`[diagram_execution_trace]`)

The diagram below maps how an incoming user interaction moves through the client interface, orchestrator, execution runner, and state storage:

```mermaid
flowchart LR
    subgraph CLIENT_INTERFACE ["CLIENT_INTERFACE"]
        direction TB
        US["<b>User Session</b><br/>Dispatches original query;<br/>renders agent audio answers.<br/><br/><i>state: idle_listening</i>"]
    end

    subgraph ORCHESTRATOR ["ORCHESTRATOR"]
        direction TB
        FC["<b>Flow Controller</b><br/>Decides intent routing and<br/>state transition tree.<br/><br/><i>module: root_agent (router_main)</i>"]
    end

    subgraph EXECUTION_RUNNER ["EXECUTION_RUNNER"]
        direction TB
        SR["<b>Subagent Runner</b><br/>Executes target flow domain:<br/>• auth_agent<br/>• billing_agent<br/>• tech_support_agent<br/>• sales_agent<br/>• appointment_agent<br/>• account_agent<br/>• secondary_language_agent"]
    end

    subgraph TOOL_LAYER ["BACKEND INTEGRATION"]
        direction TB
        TL["<b>23 Backend Tools</b><br/>Deterministic execution;<br/>CRM, Billing, Ticketing APIs;<br/><i>mock_mode & zero-latency</i>"]
    end

    %% Lifecycle Steps
    US -->|"1. prompt (audio/text)"| FC
    FC -->|"2. delegate"| SR
    SR -->|"tool call / args"| TL
    TL -->|"tool result"| SR
    SR -->|"3. state_upd (params)"| FC
    FC -->|"4. response (audio/speech)"| US

    classDef clientBox fill:#f8f9fa,stroke:#495057,stroke-width:2px;
    classDef orchBox fill:#1a73e8,stroke:#1557b0,stroke-width:2px,color:#ffffff;
    classDef runnerBox fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;
    classDef toolBox fill:#e6f4ea,stroke:#137333,stroke-width:2px;

    class US clientBox;
    class FC orchBox;
    class SR runnerBox;
    class TL toolBox;
```

---

## 3. End-to-End Sequence Diagram (Turn-by-Turn Trace)

This sequence diagram illustrates the complete call lifecycle, from initial SIP/Audio ingress to intent triage, delegated execution, tool invocation, and spoken response generation:

```mermaid
sequenceDiagram
    autonumber
    actor User as Telephony Caller
    participant Client as Client Interface (Audio Stream)
    participant Orchestrator as Flow Controller (root_agent)
    participant Runner as Subagent Runner (e.g. billing_agent)
    participant Tools as Tool Execution Engine (Python Tools)
    participant State as Session State Store (app.json)

    User->>Client: Dial inbound number / Speak prompt
    Client->>Orchestrator: 1. Ingest audio stream + Caller ID (CLID)
    Note over Orchestrator: Evaluate entrypoint rules:<br/>- Verbatim recording notice<br/>- Restricted caller check<br/>- Regional outage probe
    Orchestrator->>State: Initialize session (set clid, language, auth_level=Tier0)
    Orchestrator->>Client: 4. Emit standard greeting + consent notice
    Client->>User: Audio playback (TTS)

    User->>Client: "I have a question about a charge on my bill"
    Client->>Orchestrator: 1. Stream prompt
    Note over Orchestrator: Intent classification:<br/>Query matches Billing & Payments domain
    Orchestrator->>Runner: 2. Delegate turn to billing_agent
    
    Runner->>Tools: Invoke fetch_recent_bills(billing_account)
    Tools-->>Runner: Return {status: "success", current_balance: 142.50, due_date: "2026-10-01"}
    Runner->>State: 3. Update session variables (last_bill_amount, due_date)
    Runner-->>Orchestrator: Agent response payload + spoken script
    Orchestrator->>Client: 4. Synthesize spoken response: "Your current balance is $142.50 due October 1st."
    Client->>User: Audio playback to caller
```

---

## 4. Multi-Agent Topology (Defined Subagents)

To enforce clean modular boundaries, conversation flows are partitioned into **8 independent agents**. The root orchestrator routes between specialist agents while subagents maintain zero circular parentage:

```mermaid
graph TD
    Root["<b>root_agent</b><br/><i>(Flow Controller / Entrypoint)</i><br/>• Verbatim Recording Notice<br/>• Restricted Number Check<br/>• Outage Interception<br/>• Intent Classification & Dispatch<br/>• Human Escalation Hub"]

    Root -->|"Auth required"| Auth["<b>auth_agent</b><br/><i>(Identity & Verification)</i><br/>• SMS OTP Delivery<br/>• 6-digit OTP Validation<br/>• 4-digit Account PIN<br/>• Lockout Protection (3 tries)"]
    
    Root -->|"Billing inquiry"| Billing["<b>billing_agent</b><br/><i>(Billing & Payments)</i><br/>• Balance & Due Date Inquiry<br/>• CC / Bank Bill Pay<br/>• Autopay Enrollment<br/>• $50 Instant Dispute Policy"]

    Root -->|"Service issue"| Tech["<b>tech_support_agent</b><br/><i>(Assurance & Diagnostics)</i><br/>• Live Outage Notification<br/>• Remote Modem Reboot (ONT)<br/>• Guided Troubleshooting Cadence<br/>• Trouble Ticket Status"]

    Root -->|"Buy / upgrade / port"| Sales["<b>sales_agent</b><br/><i>(Products & Equipment)</i><br/>• Catalog Recommendations<br/>• Equipment Ordering<br/>• Hardware Warranty Claims<br/>• PAC Port-Out Transfers"]

    Root -->|"Field dispatch"| Appt["<b>appointment_agent</b><br/><i>(Field Operations)</i><br/>• 2-Hour Window Discovery<br/>• Technician Dispatch Booking<br/>• Appointment Rescheduling<br/>• Cancellation Management"]

    Root -->|"Security / line mgmt"| Acct["<b>account_agent</b><br/><i>(Account Security & Plan)</i><br/>• Password Reset SMS Link<br/>• MFA Activation / Deactivation<br/>• Lost/Stolen Line Suspension<br/>• Service Cancellation Disclosure"]

    Root -->|"Spanish requested"| SecLang["<b>secondary_language_agent</b><br/><i>(Spanish Language Support)</i><br/>• Native Spanish Dialogue<br/>• Regional Outage Reporting<br/>• Virtual Repair in Spanish<br/>• Bilingual Agent Escalation"]

    classDef rootStyle fill:#1a73e8,stroke:#1557b0,stroke-width:2px,color:#ffffff;
    classDef subStyle fill:#ffffff,stroke:#1a73e8,stroke-width:2px,color:#202124;
    
    class Root rootStyle;
    class Auth,Billing,Tech,Sales,Appt,Acct,SecLang subStyle;
```

---

## 5. Component Breakdown & Layer Specifications

### Layer 1: Client Interface (`CLIENT_INTERFACE`)
- **Telephony & Audio Ingress:** Ingests native audio streams via Google CES audio channel.
- **Voice Parameters:** Configured for low-latency conversational speech with `gemini-3.5-flash`.
- **Speech Formatting:** All prompt instructions forbid raw dollar signs (`$25`) and enforce spelled-out currency (`twenty-five dollars`) to ensure flawless text-to-speech output.
- **Interruption / Barge-in:** Allows callers to interrupt prompts naturally during long diagnostic explanations.
- **DTMF Support:** Dual-Tone Multi-Frequency inputs are captured for digit entry (PINs, OTPs, `0` for human agent).

### Layer 2: Orchestrator / Flow Controller (`ORCHESTRATOR`)
- **First-Touch Compliance:** Guaranteed recitation of mandatory recording consent (`BR-TV-001`):
  > *"This call may be recorded for quality and training purposes."*
- **Restricted Caller Screening (`BR-TV-002`):** Calls from blocked or restricted numbers receive an immediate termination notice and clean disconnection.
- **Outage Alert Pre-emption (`BR-TV-003`):** Proactively intercepts callers in confirmed outage areas, informing them of restoration ETAs before they waste time troubleshooting.
- **Intent Router:** Matches conversational queries to domain specialists using child agent descriptions and transfer rules.
- **Pivot Hub (`BR-TV-019`):** Manages topic switches seamlessly. When a customer finishes paying a bill and says *"also my wifi is down"*, the orchestrator switches context from `billing_agent` to `tech_support_agent` without dropping session memory.

### Layer 3: Subagent Runner (`EXECUTION_RUNNER`)
- **Single-Parent Topology:** Every specialist agent operates as a focused expert with `childAgents: []`. All cross-domain routing routes back through the orchestrator.
- **Progressive Authentication Guardrails:** Specialist sub-agents enforce security levels before performing sensitive actions:
  - **Tier 0 (Unauthenticated):** General plan inquiries, store hours, general outage status.
  - **Tier 1 (OTP Verified):** Account balance, due dates, billing dispute logging, ticket status.
  - **Tier 2 (PIN Verified):** Bill payments, credit card entry, password reset, line suspension, contract cancellation.
- **Verbatim Disclosures:** Enforces mandatory regulatory disclosures (e.g. early cancellation fee notice under `BR-TV-018`).

### Layer 4: Tool Execution & Mock Integration Layer (`TOOL_LAYER`)
- **Contract Standardization:** Every tool implements a defensive `try/except` returning standard JSON contracts:
  ```json
  {
    "status": "success",
    "result_data": "..."
  }
  ```
  or on error:
  ```json
  {
    "status": "error",
    "error": "Detailed error string",
    "agent_action": "Spoken recovery instruction for the LLM"
  }
  ```
- **Zero-Latency Evaluation:** Backend tools include fast, deterministic mock paths (`mock_mode: true`) to ensure simulation test suites run in under 2 minutes with zero external API dependencies.
- **Auditing & Safety:** Sensitive values (passwords, PINs, full payment details) are never echoed back in tool logs.

---

## 6. Progressive Authentication State Machine

Security verification follows a strict ladder architecture to prevent unauthorized access while minimizing customer friction:

```mermaid
stateDiagram-v2
    [*] --> Tier0_Identified: Caller ID (CLID) matched to CIRN
    
    Tier0_Identified --> Tier1_OTP_Pending: Customer requests account-specific data
    Tier1_OTP_Pending --> Tier1_OTP_Verified: 6-Digit SMS OTP validated
    Tier1_OTP_Pending --> Auth_Retry: Invalid code (Attempts < 3)
    Auth_Retry --> Tier1_OTP_Pending: Re-enter code
    Auth_Retry --> Lockout_Escalate: 3 Consecutive Failures

    Tier1_OTP_Verified --> Tier2_PIN_Pending: Customer requests sensitive action (Pay, Cancel, Suspend)
    Tier2_PIN_Pending --> Tier2_PIN_Verified: 4-Digit Account PIN validated
    Tier2_PIN_Pending --> Lockout_Escalate: 3 Consecutive PIN Failures

    Tier2_PIN_Verified --> Full_Access: Execute high-security transaction
    Lockout_Escalate --> Human_Transfer: Warm transfer to Fraud / Live Agent
```

---

## 7. Escalation & Queue Handover Architecture

When an escalation trigger occurs, the subagent issues an `execute_live_agent_handover` tool call. The tool routes the call to the appropriate ACD queue with a comprehensive JSON metadata payload:

```mermaid
flowchart TD
    Trigger["Escalation Trigger Occurs<br/>(User pressed 0 / 3 Auth Failures / Severe Frustration / Billing > $50)"] --> Eval["Evaluate Reason Code & Domain"]

    Eval -->|"Billing dispute > $50 or payment failure"| Q1["<b>Queue: Billing_Specialist</b><br/>Pass: CIRN, dispute amount, bill ID"]
    Eval -->|"Virtual repair unresolved / Hardware defect"| Q2["<b>Queue: Technical_Support</b><br/>Pass: CIRN, ONT status, symptom"]
    Eval -->|"Service cancellation / High churn risk"| Q3["<b>Queue: Retention_Team</b><br/>Pass: CIRN, cancellation reason, fee disclosure status"]
    Eval -->|"General representative request / Auth lockout"| Q4["<b>Queue: Customer_Care_Tier1</b><br/>Pass: CIRN, auth status, session transcript"]

    classDef trigStyle fill:#fce8e6,stroke:#c5221f,stroke-width:2px;
    classDef qStyle fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;
    class Trigger trigStyle;
    class Q1,Q2,Q3,Q4 qStyle;
```

### Context Metadata Transferred:
```json
{
  "cirn": "CRN-8849",
  "auth_level": "Tier1_OTP_Verified",
  "primary_intent": "service_cancellation",
  "sentiment_score": -0.6,
  "queue": "Retention_Team",
  "summary": "Customer moving outside coverage zone. Verbatim fee disclosure recited. Customer confirmed intention to cancel."
}
```

---

## 8. Summary of Architectural Guarantees

1. **Compliance by Design:** Verbatim disclosures cannot be skipped, hallucinated, or truncated.
2. **Zero Orphaned Calls:** Infinite loops are eliminated through deterministic counter limits (max 3 retries) and automatic warm transfers.
3. **Resilient State Persistence:** State parameters are globally available across subagents, preventing customers from having to repeat account details after transfers.
4. **Sub-second Tool Responses:** All 23 tools return in $<50\text{ms}$ with standardized error recovery guidance.
