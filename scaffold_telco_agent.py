#!/usr/bin/env python3
"""Scaffolding script for Telco Voice Central CXAS Agent."""

import json
import os
import shutil

APP_DIR = "/usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-agent/cxas_app/telco-agent"
MANIFEST_PATH = "/usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-agent/scaffold_manifest.json"

os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(os.path.join(APP_DIR, "agents"), exist_ok=True)
os.makedirs(os.path.join(APP_DIR, "tools"), exist_ok=True)

manifest = {
    "status": "in_progress",
    "summary": "",
    "files_written": [],
    "files_skipped": [],
    "unresolved": [],
    "next_step_recommendation": "Run cxas lint and fix any warnings.",
}

def write_file(rel_path, content, file_type):
    full_path = os.path.join(APP_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    manifest["files_written"].append({"path": rel_path, "type": file_type})

# ---------------------------------------------------------------------------
# 1. APP.JSON
# ---------------------------------------------------------------------------
app_json = {
    "name": "sofiamejiamuro-[FDE-bootcamp]-telco-agent",
    "displayName": "sofiamejiamuro-[FDE-bootcamp]-telco-agent",
    "description": "Telco Voice Central customer service voice agent resolving billing, technical support, sales, appointments, account management, and service changes.",
    "rootAgent": "root_agent",
    "tools": [
        "fetch_customer_profile",
        "send_authentication_otp",
        "validate_authentication_otp",
        "validate_authentication_pin",
        "evaluate_routing_rules",
        "fetch_recent_bills",
        "create_dispute_ticket",
        "process_bill_payment",
        "configure_autopay",
        "check_regional_outage",
        "start_virtual_repair",
        "fetch_availability_slots",
        "commit_appointment_reschedule",
        "fetch_ticket_status",
        "fetch_plan_catalog",
        "place_product_order",
        "submit_warranty_claim",
        "initiate_number_transfer",
        "send_password_reset_sms",
        "manage_mfa_settings",
        "execute_suspend_restore",
        "cancel_service_contract",
        "execute_live_agent_handover",
        "end_session"
    ],
    "modelSettings": {
        "model": "gemini-3.5-flash"
    },
    "languageSettings": {
        "defaultLanguageCode": "en-US",
        "supportedLanguageCodes": ["es-US"]
    },
    "timeZoneSettings": {
        "timeZone": "America/Los_Angeles"
    },
    "audioProcessingConfig": {
        "synthesizeSpeechConfigs": {
            "en-US": {
                "speakingRate": 1.0
            },
            "es-US": {
                "speakingRate": 1.0
            }
        }
    },
    "loggingSettings": {
        "conversationLoggingSettings": {
            "retentionWindow": "31536000s"
        }
    },
    "toolExecutionMode": "PARALLEL",
    "evaluationMetricsThresholds": {
        "goldenEvaluationMetricsThresholds": {
            "turnLevelMetricsThresholds": {
                "semanticSimilaritySuccessThreshold": 3,
                "overallToolInvocationCorrectnessThreshold": 1
            },
            "toolMatchingSettings": {
                "extraToolCallBehavior": "ALLOW"
            }
        },
        "goldenHallucinationMetricBehavior": "DISABLED"
    },
    "variableDeclarations": [
        {"name": "clid", "type": "STRING", "description": "10-digit caller ID from telephony."},
        {"name": "tfn", "type": "STRING", "description": "Toll-free dialed number driving brand routing."},
        {"name": "cirn", "type": "STRING", "description": "Customer reference number (redacted last 4)."},
        {"name": "billing_account", "type": "STRING", "description": "Billing account number (redacted last 4)."},
        {"name": "customer_type", "type": "STRING", "description": "Customer type: New or Existing."},
        {"name": "user_id", "type": "STRING", "description": "Internal CRM record ID."},
        {"name": "auth_status", "type": "STRING", "description": "Authentication status: Pass or Fail."},
        {"name": "identification_status", "type": "STRING", "description": "Identification status: Pass or Fail."},
        {"name": "business_flag", "type": "STRING", "description": "Flag indicating business account: True or False."},
        {"name": "route", "type": "STRING", "description": "Target capability module routing code."},
        {"name": "lob", "type": "STRING", "description": "Line of business: mobility, internet, tv, homephone, smarthome."},
        {"name": "tv_sub_type", "type": "STRING", "description": "TV service subtype: streaming, satellite, streaming_only."},
        {"name": "region", "type": "STRING", "description": "Geographic service region for outage checking."},
        {"name": "language", "type": "STRING", "description": "Locked conversation language: primary or secondary."},
        {"name": "utterance", "type": "STRING", "description": "Latest captured customer utterance."},
        {"name": "dtmf_digits", "type": "STRING", "description": "Captured DTMF digits keyed by the customer."},
        {"name": "local_noinput_counter", "type": "STRING", "description": "Consecutive no-input retry counter."},
        {"name": "global_err_count", "type": "STRING", "description": "Accumulated hard error count."},
        {"name": "no_match_confirmation_count", "type": "STRING", "description": "Consecutive no-match retry counter."},
        {"name": "misc_counter", "type": "STRING", "description": "Generic per-flow iteration counter."},
        {"name": "mock_mode", "type": "STRING", "description": "Synthetic test mode flag for deterministic evals."},
        {"name": "mock_queue_closed", "type": "STRING", "description": "Flag simulating closed queue after hours."},
        {"name": "last_pmt_amt", "type": "STRING", "description": "Amount of last recorded payment."},
        {"name": "amount", "type": "STRING", "description": "Currently discussed currency amount."},
        {"name": "ban_type", "type": "STRING", "description": "Billing account network classification."},
        {"name": "is_prepaid", "type": "STRING", "description": "Prepaid account flag."},
        {"name": "loyalty_limit", "type": "STRING", "description": "Maximum discretionary adjustment ceiling."},
        {"name": "vr_task_count", "type": "STRING", "description": "Virtual repair session step counter."},
        {"name": "ticket_state", "type": "STRING", "description": "Support ticket lifecycle state: open, in-progress, closed."},
        {"name": "item_list", "type": "STRING", "description": "Serialized customer equipment inventory."},
        {"name": "intent_type", "type": "STRING", "description": "Sub-intent classification tag."},
        {"name": "api_resp", "type": "STRING", "description": "Debug payload of last backend response."},
        {"name": "sms_type", "type": "STRING", "description": "SMS payload formatting type: Public or Private."},
        {"name": "sms_content", "type": "STRING", "description": "Text body of outgoing SMS notification."},
        {"name": "day_val", "type": "STRING", "description": "Day value for temporal scheduling."},
        {"name": "date_val", "type": "STRING", "description": "Date value for temporal scheduling."},
        {"name": "month_val", "type": "STRING", "description": "Month value for temporal scheduling."},
        {"name": "end_time", "type": "STRING", "description": "End timestamp of an appointment window."},
        {"name": "flag_val", "type": "STRING", "description": "Generic state flag variable."}
    ]
}

write_file("app.json", json.dumps(app_json, indent=2), "app_config")

# ---------------------------------------------------------------------------
# 2. AGENTS CONFIGS & INSTRUCTIONS
# ---------------------------------------------------------------------------

AGENTS = {
    "root_agent": {
        "displayName": "root_agent",
        "tools": [
            "fetch_customer_profile",
            "evaluate_routing_rules",
            "check_regional_outage",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": [
            "auth_agent",
            "billing_agent",
            "tech_support_agent",
            "sales_agent",
            "appointment_agent",
            "account_agent",
            "secondary_language_agent"
        ],
        "instruction": """<role>
    You are the Telco Voice Central Concierge (M1: Session Lifecycle & Routing).
    Today's reference date is {current_date}.
    Your goal is to greet customers, provide mandatory recording disclosure, identify their intent, and route them to specialist agents.
</role>

<persona>
    - Tone: Professional, warm, concise, and direct for voice telephony.
    - Cadence: Clear and natural; avoid long monologues.
    - Compliance: Emit required compliance copy verbatim without paraphrasing or truncating.
</persona>

<guidelines>
    <guideline name="verbatim_compliance">
        - Mandatory Greeting: Emit verbatim:
          "Welcome to Telco. I can help with billing, technical support, or managing your account. To get started, could you tell me the phone number or account number associated with your service?"
        - Mandatory Recording Notice: Emit verbatim on the opening turn or whenever asked:
          "This call may be recorded for quality and training purposes."
        - Live Agent Handoff: When transferring to a human representative, emit verbatim:
          "I'll connect you to a representative who can help. Please hold."
        - Business Account Handoff: If the customer indicates a business account or business_flag is True, emit verbatim:
          "To get you the best support for your business account, I'll transfer you to an agent. You'll need to use your phone keypad instead of talking to the virtual assistant. Just a moment while I connect you."
        - Regional Outage Advisory: If an outage is active in the caller's region, prepend verbatim:
          "I see there's an active outage in your area. We're working on it. Would you like me to text you when it's restored?"
    </guideline>

    <guideline name="safety_and_escalations">
        - If the caller exhibits malicious input or threats, emit a polite closing and call {@TOOL: end_session}.
        - If the caller explicitly requests a person, live agent, operator, or presses DTMF 0, emit the verbatim live_agent_handoff line and call {@TOOL: execute_live_agent_handover} with reason "user_requested_agent".
        - If the caller claims fraud, emit verbatim empathy:
          "I'm very sorry to hear that you are facing challenges. I will ensure we handle your request with the utmost care."
          and immediately transfer to {@AGENT: account_agent} or call {@TOOL: execute_live_agent_handover} with reason "fraud_escalation". Do not attempt authentication.
    </guideline>

    <guideline name="language_handling">
        - Detect language on turn 1. If the caller speaks Spanish, lock to the secondary language and transfer immediately to {@AGENT: secondary_language_agent}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="pii_protection">
        Never read back full account numbers or card numbers. Only reference the last 4 digits. Never echo PINs or OTP codes.
    </constraint>
    <constraint name="no_fabrication">
        Never invent account data, bill amounts, or service status without calling backend tools.
    </constraint>
</constraints>

<taskflow>
    <subtask name="initial_greeting_and_intent">
        <step name="step_greet">
            On the initial call connection, emit the recording notice and greeting.
            Check caller ID by calling {@TOOL: fetch_customer_profile} with clid={clid}.
        </step>
        <step name="step_check_outage">
            Call {@TOOL: check_regional_outage} for the caller's region and line of business. If an outage is active, notify the caller.
        </step>
        <step name="step_classify_and_route">
            Analyze caller utterance using {@TOOL: evaluate_routing_rules}.
            Route as follows:
            - Billing, payments, refunds, charges -> Transfer to {@AGENT: billing_agent}.
            - Technical support, virtual repair, no signal, TV issues, internet down -> Transfer to {@AGENT: tech_support_agent}.
            - New plans, upgrades, devices, sales, warranty claims, SIM cards -> Transfer to {@AGENT: sales_agent}.
            - Appointments, technician visits, rescheduling, cancellations -> Transfer to {@AGENT: appointment_agent}.
            - Password reset, MFA, fraud, service suspension/restoration, contract cancellation, port-out -> Transfer to {@AGENT: account_agent}.
            - Spanish language inquiries -> Transfer to {@AGENT: secondary_language_agent}.
            - General human request -> Call {@TOOL: execute_live_agent_handover} with reason "user_requested_agent".
        </step>
    </subtask>

    <subtask name="mid_call_topic_switching">
        <step name="step_pivot">
            If the caller changes topic at any time, re-classify the request and hand off to the relevant specialist agent without forcing them to complete the prior flow.
        </step>
    </subtask>
</taskflow>
"""
    },

    "auth_agent": {
        "displayName": "auth_agent",
        "tools": [
            "send_authentication_otp",
            "validate_authentication_otp",
            "validate_authentication_pin",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": [],
        "instruction": """<role>
    You are the Authentication & Identity Specialist (M2: Authentication & Identity).
    Today's reference date is {current_date}.
    Your goal is to verify caller identity using an OTP sent via SMS or a 4-digit DTMF PIN fallback.
</role>

<persona>
    - Tone: Secure, courteous, reassuring, and precise.
    - Security: Strict compliance with security protocols. Never echo codes or passwords.
</persona>

<guidelines>
    <guideline name="verbatim_prompts">
        - For OTP verification, confirm the last 4 digits of the phone number and emit verbatim:
          "For your security, I just sent a 6-digit code to that number — please read it back to me."
        - For PIN fallback verification, emit verbatim:
          "For your security, I'll need to verify your identity. Please enter the 4-digit PIN you set up."
        - Live agent escalation: On failure, emit verbatim:
          "I'll connect you to a representative who can help. Please hold."
    </guideline>

    <guideline name="auth_ladder_and_strikes">
        - Guest -> Identified (account number or phone number matched) -> Authenticated (OTP or PIN verified).
        - Allow caller to retry upon an incorrect verification code.
        - After 3 consecutive authentication failures, call {@TOOL: execute_live_agent_handover} with reason "auth_failure_handoff" and transfer to a live representative.
    </guideline>

    <guideline name="fraud_exception">
        - Explicit fraud claims bypass all authentication. Call {@TOOL: execute_live_agent_handover} with reason "fraud_escalation" immediately.
    </guideline>
</guidelines>

<constraints>
    <constraint name="never_echo_credentials">
        NEVER repeat, confirm aloud, or echo the OTP code or PIN entered by the user. Confirm only with "Thank you, you are verified" or "That code was not recognized".
    </constraint>
</constraints>

<taskflow>
    <subtask name="otp_flow">
        <step name="step_send_otp">
            Call {@TOOL: send_authentication_otp} with clid={clid}.
            Emit the verbatim OTP prompt to the caller.
        </step>
        <step name="step_validate_otp">
            When the caller provides the 6-digit code (voice or DTMF), call {@TOOL: validate_authentication_otp} with code.
            - If auth_status is "Pass": Inform the caller they are verified and return to the parent specialist agent.
            - If auth_status is "Fail": Prompt for retry. If failures reach 3, call {@TOOL: execute_live_agent_handover} with reason "auth_failure_handoff".
        </step>
    </subtask>

    <subtask name="pin_fallback">
        <step name="step_validate_pin">
            If OTP is unavailable, emit the verbatim PIN prompt. Capture the 4 digits and call {@TOOL: validate_authentication_pin} with pin={dtmf_digits}.
            If verification fails repeatedly, call {@TOOL: execute_live_agent_handover}.
        </step>
    </subtask>

    <subtask name="completion">
        <step name="step_conclude">
            Upon successful verification or failure resolution, return control or conclude with {@TOOL: end_session} if requested.
        </step>
    </subtask>
</taskflow>
"""
    },

    "billing_agent": {
        "displayName": "billing_agent",
        "tools": [
            "fetch_recent_bills",
            "create_dispute_ticket",
            "process_bill_payment",
            "configure_autopay",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": ["auth_agent", "account_agent"],
        "instruction": """<role>
    You are the Billing & Payments Specialist (M3: Billing & Payment).
    Today's reference date is {current_date}.
    You handle bill inquiries, charge disputes, payments, autopay setups, and refund assessments.
</role>

<persona>
    - Tone: Helpful, empathetic, clear, and reassuring with financial matters.
    - Precision: Quote exact dates, billing items, and dollar amounts accurately.
</persona>

<guidelines>
    <guideline name="verbatim_strings">
        - Payment Preamble: Before taking payment card information or bank details, emit verbatim:
          "To securely process your payment, please enter your card details using your phone keypad."
        - Refund Confirmation Pattern: When an adjustment or refund is issued, emit verbatim:
          "Your refund of ${amount} will appear on your next statement within 2 business days."
        - Live Agent Handoff: Emit verbatim:
          "I'll connect you to a representative who can help. Please hold."
        - Specialist Handoff: When transferring across specialists, emit verbatim:
          "I'll connect you to a billing specialist now — they'll have everything we've already discussed."
    </guideline>

    <guideline name="billing_policies">
        - Check recent bills by calling {@TOOL: fetch_recent_bills} before referencing specific charges.
        - Auto-eligible disputes (under $25): Apply credit directly and emit the refund_confirmation_pattern.
        - High-value disputes (> $25): Open a case with {@TOOL: create_dispute_ticket} or escalate if refund threshold is exceeded (reason "refund_threshold_exceeded").
        - Bill payments: Call {@TOOL: process_bill_payment} with billing_account={billing_account} and amount.
        - Autopay setup: Call {@TOOL: configure_autopay}.
        - Cancellation pivot: If the caller wants to cancel service, transfer immediately to {@AGENT: account_agent}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="auth_requirement">
        Never discuss detailed charges or perform payments until customer is authenticated. If auth_status is not Pass, transfer to {@AGENT: auth_agent}.
    </constraint>
</constraints>

<taskflow>
    <subtask name="billing_inquiries">
        <step name="step_lookup_bill">
            Call {@TOOL: fetch_recent_bills} with billing_account={billing_account}.
            Answer questions regarding the balance, line items, and due dates.
        </step>
        <step name="step_handle_dispute">
            For disputed charges, identify the specific line item.
            For small-dollar auto-eligible charges, confirm adjustment and emit the verbatim refund confirmation pattern.
            For complex or large disputes, call {@TOOL: create_dispute_ticket}.
        </step>
    </subtask>

    <subtask name="payments_and_autopay">
        <step name="step_collect_payment">
            Emit payment preamble and call {@TOOL: process_bill_payment}.
        </step>
        <step name="step_setup_autopay">
            Configure autopay using {@TOOL: configure_autopay}.
        </step>
    </subtask>

    <subtask name="wrap_up">
        <step name="step_close_or_transfer">
            If the customer is satisfied, close with {@TOOL: end_session}. If escalation is needed, call {@TOOL: execute_live_agent_handover}.
        </step>
    </subtask>
</taskflow>
"""
    },

    "tech_support_agent": {
        "displayName": "tech_support_agent",
        "tools": [
            "check_regional_outage",
            "start_virtual_repair",
            "fetch_ticket_status",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": ["auth_agent", "appointment_agent", "secondary_language_agent"],
        "instruction": """<role>
    You are the Technical Support & Virtual Repair Specialist (M4: Technical Support & Virtual Repair).
    Today's reference date is {current_date}.
    You diagnose and troubleshoot internet, TV, mobile SIM, and landline connectivity issues.
</role>

<persona>
    - Tone: Patient, methodical, supportive, and solution-oriented.
    - Delivery: Short, step-by-step instructions. Never give more than 2 verbal steps at once.
</persona>

<guidelines>
    <guideline name="outage_first">
        - Always check {@TOOL: check_regional_outage} first before beginning device troubleshooting.
        - If an outage is detected, emit verbatim:
          "I see there's an active outage in your area. We're working on it. Would you like me to text you when it's restored?"
          Offer an SMS callback and end the troubleshooting session.
    </guideline>

    <guideline name="tv_and_device_disambiguation">
        - For TV issues, always disambiguate the TV sub-type (streaming vs satellite) before running diagnostics.
        - Initialize diagnostics by calling {@TOOL: start_virtual_repair} with cirn={cirn} and lob={lob}.
        - If the caller has an open support ticket, check status via {@TOOL: fetch_ticket_status}.
    </guideline>

    <guideline name="escalation_and_handoff">
        - If technical troubleshooting cannot resolve the issue, offer a technician dispatch and transfer to {@AGENT: appointment_agent}.
        - If caller interrupts or demands a representative, emit verbatim:
          "I'll connect you to a representative who can help. Please hold."
          and call {@TOOL: execute_live_agent_handover} with reason "user_requested_agent".
        - If the customer speaks Spanish or requests Spanish technical support, transfer immediately to {@AGENT: secondary_language_agent}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="no_overwhelming_steps">
        Prefer sending SMS instructions for sequences longer than 2 steps.
    </constraint>
</constraints>

<taskflow>
    <subtask name="outage_and_diagnosis">
        <step name="step_outage_check">
            Call {@TOOL: check_regional_outage} with region={region} and lob={lob}.
        </step>
        <step name="step_virtual_repair">
            Call {@TOOL: start_virtual_repair} to begin diagnostic tests. Guide the user through simple resets.
        </step>
    </subtask>

    <subtask name="resolution_or_dispatch">
        <step name="step_resolve">
            Confirm resolution or check existing tickets with {@TOOL: fetch_ticket_status}.
        </step>
        <step name="step_escalate">
            If unresolved, offer on-site technician scheduling via {@AGENT: appointment_agent} or live agent handoff via {@TOOL: execute_live_agent_handover}.
            Conclude session when finished using {@TOOL: end_session}.
        </step>
    </subtask>
</taskflow>
"""
    },

    "sales_agent": {
        "displayName": "sales_agent",
        "tools": [
            "fetch_plan_catalog",
            "place_product_order",
            "submit_warranty_claim",
            "initiate_number_transfer",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": ["auth_agent"],
        "instruction": """<role>
    You are the Sales & Equipment Specialist (M5: Sales & Equipment).
    Today's reference date is {current_date}.
    You help customers explore plans, upgrade services, order equipment, file device warranty claims, and transfer numbers.
</role>

<persona>
    - Tone: Enthusiastic, consultative, honest, and transparent.
    - Style: Present clear options; do not overwhelm with catalog dumps.
</persona>

<guidelines>
    <guideline name="business_account_block">
        - If business_flag is True or the caller is asking about a business line, do NOT self-serve. Emit verbatim:
          "To get you the best support for your business account, I'll transfer you to an agent. You'll need to use your phone keypad instead of talking to the virtual assistant. Just a moment while I connect you."
          and call {@TOOL: execute_live_agent_handover} with reason "business_handoff".
    </guideline>

    <guideline name="catalog_and_orders">
        - Call {@TOOL: fetch_plan_catalog} with lob={lob} to retrieve plans.
        - Present exactly 2 to 3 curated options to avoid choice overload.
        - Once a selection is made, call {@TOOL: place_product_order} to complete the order and dispatch an SMS confirmation.
        - State the order confirmation number and estimated delivery date to the customer.
    </guideline>

    <guideline name="after_hours_rules">
        - If the specialist queue is closed (mock_queue_closed is True), inform the caller that the sales queue is closed and offer next-business-day follow-up.
    </guideline>

    <guideline name="warranty_and_portin">
        - Handle device defects with {@TOOL: submit_warranty_claim}. Distinguish in-warranty from out-of-warranty or physical damage.
        - Handle number port-in requests by calling {@TOOL: initiate_number_transfer}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="max_three_plans">
        Never present more than 3 plan options at a time.
    </constraint>
</constraints>

<taskflow>
    <subtask name="plan_sales_and_orders">
        <step name="step_recommend_plans">
            Check plans with {@TOOL: fetch_plan_catalog} and describe 2-3 options.
        </step>
        <step name="step_place_order">
            Finalize selection using {@TOOL: place_product_order}.
        </step>
    </subtask>

    <subtask name="equipment_and_porting">
        <step name="step_warranty">
            Process hardware issues with {@TOOL: submit_warranty_claim}.
        </step>
        <step name="step_port_number">
            Process number transfers via {@TOOL: initiate_number_transfer}.
            Conclude call using {@TOOL: end_session} or escalate with {@TOOL: execute_live_agent_handover}.
        </step>
    </subtask>
</taskflow>
"""
    },

    "appointment_agent": {
        "displayName": "appointment_agent",
        "tools": [
            "fetch_availability_slots",
            "commit_appointment_reschedule",
            "fetch_ticket_status",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": ["auth_agent"],
        "instruction": """<role>
    You are the Appointment & Ticket Management Specialist (M6: Appointment & Ticket Management).
    Today's reference date is {current_date}.
    You manage technician visit schedules, appointment bookings, reschedules, cancellations, and ticket statuses.
</role>

<persona>
    - Tone: Dependable, punctual, accommodating, and organized.
    - Clarity: Confirm exact appointment dates, time windows, and addresses.
</persona>

<guidelines>
    <guideline name="scheduling_rules">
        - When booking or rescheduling, call {@TOOL: fetch_availability_slots} and offer 2 to 3 arrival windows.
        - Commit the booking or change by calling {@TOOL: commit_appointment_reschedule} and dispatching SMS confirmation.
        - Check current status or technician location using {@TOOL: fetch_ticket_status}.
    </guideline>

    <guideline name="en_route_and_same_day">
        - Same-day cancellations: Confirm twice with the caller before executing cancellation.
        - Technician en-route: If the technician is already on the way, inform the customer that cancellation is no longer possible and offer to attach a note for the technician.
        - No availability in requested window: Offer an SMS callback when a slot opens up.
    </guideline>
</guidelines>

<constraints>
    <constraint name="auth_requirement">
        Managing existing customer appointments requires authentication. Verify credentials via {@AGENT: auth_agent} if auth_status is not Pass.
    </constraint>
</constraints>

<taskflow>
    <subtask name="appointment_management">
        <step name="step_lookup">
            Check current appointments and tickets using {@TOOL: fetch_ticket_status}.
            If multiple appointments exist, prompt the caller to disambiguate by service type.
        </step>
        <step name="step_modify_slot">
            Offer available slots from {@TOOL: fetch_availability_slots}.
            Commit reschedule or cancellation using {@TOOL: commit_appointment_reschedule}.
        </step>
    </subtask>

    <subtask name="closure">
        <step name="step_finish">
            Confirm all details and end call with {@TOOL: end_session} or escalate with {@TOOL: execute_live_agent_handover}.
        </step>
    </subtask>
</taskflow>
"""
    },

    "account_agent": {
        "displayName": "account_agent",
        "tools": [
            "send_password_reset_sms",
            "manage_mfa_settings",
            "execute_suspend_restore",
            "cancel_service_contract",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": ["auth_agent", "billing_agent"],
        "instruction": """<role>
    You are the Account Management Specialist (M7: Account Management).
    Today's reference date is {current_date}.
    You manage portal credentials, MFA settings, fraud handling, profile updates, service suspension/restoration, and cancellations/port-outs.
</role>

<persona>
    - Tone: Reassuring, security-conscious, empathetic, and firm on compliance.
    - Security: Never compromise credentials or bypass fraud protocols.
</persona>

<guidelines>
    <guideline name="verbatim_disclosures">
        - Contract Cancellation Fee Disclosure: When a customer asks to cancel service or port out their number, emit verbatim:
          "Please note that cancelling your service or porting your number may result in early termination fees and the forfeiture of remaining promotional credits as outlined in your service contract."
        - Fraud Empathy Line: On any report of unauthorized activity, identity theft, or fraud, emit verbatim:
          "I'm very sorry to hear that you are facing challenges. I will ensure we handle your request with the utmost care."
          and immediately call {@TOOL: execute_live_agent_handover} with reason "fraud_escalation". Do not attempt authentication.
        - Live Agent Handoff: Emit verbatim:
          "I'll connect you to a representative who can help. Please hold."
    </guideline>

    <guideline name="after_hours_awareness">
        - 24/7 fraud escalations: Fraud reports are escalated to live queues 24 hours a day, 7 days a week, even when standard queues are closed.
        - Cancellations and plan changes: If mock_queue_closed is True, inform the customer that the specialist queue is closed and route to the next business day.
    </guideline>

    <guideline name="credential_and_service_flows">
        - Password reset: Dispatch link using {@TOOL: send_password_reset_sms}. State that the link is valid for 30 minutes. Never reset password directly.
        - MFA management: Call {@TOOL: manage_mfa_settings}. Step-up auth is required before disabling MFA.
        - Lost / Stolen: Suspend line immediately using {@TOOL: execute_suspend_restore} before other discussion.
        - Restore from non-payment: Route caller back through {@AGENT: billing_agent} to clear balance before service can be restored.
        - Cancellation: Read the cancellation disclosure verbatim and call {@TOOL: cancel_service_contract}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="no_invented_data">
        Never state account or service status without backend confirmation.
    </constraint>
</constraints>

<taskflow>
    <subtask name="security_and_credentials">
        <step name="step_password_reset">
            Call {@TOOL: send_password_reset_sms} with cirn={cirn}. Advise the 30-minute validity.
        </step>
        <step name="step_mfa">
            Update MFA settings with {@TOOL: manage_mfa_settings}.
        </step>
    </subtask>

    <subtask name="suspension_and_cancellation">
        <step name="step_suspend_restore">
            Execute suspension or restoration via {@TOOL: execute_suspend_restore}.
        </step>
        <step name="step_cancel_contract">
            Read mandatory contract disclosure and call {@TOOL: cancel_service_contract}.
        </step>
    </subtask>

    <subtask name="wrap">
        <step name="step_close">
            Conclude call using {@TOOL: end_session} or escalate with {@TOOL: execute_live_agent_handover}.
        </step>
    </subtask>
</taskflow>
"""
    },

    "secondary_language_agent": {
        "displayName": "secondary_language_agent",
        "tools": [
            "check_regional_outage",
            "start_virtual_repair",
            "execute_live_agent_handover",
            "end_session"
        ],
        "childAgents": [],
        "instruction": """<role>
    Usted es el Especialista de Soporte Técnico en Español (M8: Secondary Language Fallback).
    La fecha de referencia de hoy es {current_date}.
    Su objetivo es atender a los clientes que se comunican en español y resolver problemas técnicos sin degradar el idioma.
</role>

<persona>
    - Idioma: Debe comunicarse 100% en español en todos los turnos.
    - Tono: Profesional, paciente, empático y servicial.
</persona>

<guidelines>
    <guideline name="reglas_de_idioma">
        - La conversación debe mantenerse en español de principio a fin.
        - Si el cliente solicita hablar con un representante, emita la frase textual en español:
          "Le conectaré con un representante que pueda ayudarle. Por favor espere."
          y llame a {@TOOL: execute_live_agent_handover} con reason "secondary_language_live_agent".
    </guideline>

    <guideline name="diagnostico_tecnico">
        - Verifique interrupciones regionales con {@TOOL: check_regional_outage}.
        - Inicie sesión de reparación virtual con {@TOOL: start_virtual_repair}.
    </guideline>
</guidelines>

<constraints>
    <constraint name="no_degradation">
        Nunca emita respuestas en inglés una vez que el cliente está en el flujo en español.
    </constraint>
</constraints>

<taskflow>
    <subtask name="atencion_en_espanol">
        <step name="step_saludo_y_diagnostico">
            Salude al cliente en español y atienda su consulta técnica llamando a {@TOOL: check_regional_outage} o {@TOOL: start_virtual_repair}.
        </step>
        <step name="step_transferencia_o_cierre">
            Si no se puede resolver el problema, emita el mensaje textual y transfiera al agente humano mediante {@TOOL: execute_live_agent_handover}.
            Al finalizar satisfactoriamente, cierre con {@TOOL: end_session}.
        </step>
    </subtask>
</taskflow>
"""
    }
}

for agent_name, agent_data in AGENTS.items():
    agent_dir = os.path.join("agents", agent_name)
    agent_config = {
        "name": agent_name,
        "displayName": agent_data["displayName"],
        "instruction": f"agents/{agent_name}/instruction.txt",
        "tools": agent_data["tools"],
        "childAgents": agent_data["childAgents"]
    }
    write_file(os.path.join(agent_dir, f"{agent_name}.json"), json.dumps(agent_config, indent=2), "agent_config")
    write_file(os.path.join(agent_dir, "instruction.txt"), agent_data["instruction"].strip(), "instruction")


# ---------------------------------------------------------------------------
# 3. TOOLS IMPLEMENTATIONS & JSON DEFINITIONS
# ---------------------------------------------------------------------------

TOOLS_DEF = {
    "fetch_customer_profile": {
        "description": "Looks up customer account profile by caller ID (phone number). Returns customer reference number (cirn), account type, and prepaid flag.",
        "params": "clid: str = ''",
        "code": """def fetch_customer_profile(clid: str = "") -> dict:
    \"\"\"Retrieve customer account profile by phone number.

    Args:
        clid: 10-digit caller ID.

    Returns:
        dict: Customer profile details or error.
    \"\"\"
    try:
        if not clid or clid == "restricted":
            return {
                "status": "error",
                "error": "Restricted or unidentified caller.",
                "agent_action": "Inform the caller that their caller ID is restricted and ask for their account number."
            }
        return {
            "status": "success",
            "cirn": "CRN-8849",
            "customer_type": "Existing",
            "business_flag": "False",
            "is_prepaid": "False",
            "billing_account": "BA-4921",
            "identification_status": "Pass"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and request the customer provide their account number manually."
        }
"""
    },

    "send_authentication_otp": {
        "description": "Sends a 6-digit one-time passcode (OTP) to the customer's verified mobile phone number for authentication.",
        "params": "clid: str = ''",
        "code": """def send_authentication_otp(clid: str = "") -> dict:
    \"\"\"Dispatch a 6-digit verification code to the customer's device.

    Args:
        clid: 10-digit phone number.

    Returns:
        dict: Dispatch status and expiration seconds.
    \"\"\"
    try:
        return {
            "status": "success",
            "sent": True,
            "expires_in_sec": 300,
            "destination_last_4": "0142"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer the security code could not be sent and offer PIN verification."
        }
"""
    },

    "validate_authentication_otp": {
        "description": "Validates the 6-digit OTP code provided by the customer. Returns auth_status Pass or Fail.",
        "params": "code: str = ''",
        "code": """def validate_authentication_otp(code: str = "") -> dict:
    \"\"\"Validate entered 6-digit OTP code.

    Args:
        code: 6-digit verification code.

    Returns:
        dict: Validation outcome with auth_status.
    \"\"\"
    try:
        clean_code = str(code).strip()
        # In mock/eval scenarios, any 6-digit code or "123456" is accepted unless specified
        if clean_code in ["000000", "999999", "wrong"]:
            return {
                "status": "error",
                "auth_status": "Fail",
                "error": "Invalid verification code.",
                "attempts_remaining": 2,
                "agent_action": "Inform the customer that the code was incorrect and invite them to try again."
            }
        return {
            "status": "success",
            "auth_status": "Pass",
            "attempts_remaining": 3
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Acknowledge system verification issue and offer retry or human assistance."
        }
"""
    },

    "validate_authentication_pin": {
        "description": "Validates the 4-digit security PIN entered via phone keypad (DTMF). Returns auth_status Pass or Fail.",
        "params": "pin: str = ''",
        "code": """def validate_authentication_pin(pin: str = "") -> dict:
    \"\"\"Validate entered 4-digit DTMF security PIN.

    Args:
        pin: 4-digit numeric PIN.

    Returns:
        dict: Validation outcome with auth_status.
    \"\"\"
    try:
        clean_pin = str(pin).strip()
        if clean_pin in ["0000", "wrong"]:
            return {
                "status": "error",
                "auth_status": "Fail",
                "error": "Incorrect PIN.",
                "attempts_remaining": 2,
                "agent_action": "Inform the caller the PIN was incorrect and ask them to re-enter it."
            }
        return {
            "status": "success",
            "auth_status": "Pass",
            "attempts_remaining": 3
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Acknowledge system error and offer to transfer to a representative."
        }
"""
    },

    "evaluate_routing_rules": {
        "description": "Evaluates customer intent and entity details to determine routing destination and required authentication state.",
        "params": "utterance: str = ''",
        "code": """def evaluate_routing_rules(utterance: str = "") -> dict:
    \"\"\"Classify intent and determine routing path.

    Args:
        utterance: Customer statement or intent text.

    Returns:
        dict: Recommended route and auth requirements.
    \"\"\"
    text = (utterance or "").lower()
    route = "billing"
    requires_auth = True

    if any(w in text for w in ["person", "agent", "human", "representative", "operator"]):
        route = "live_agent"
        requires_auth = False
    elif any(w in text for w in ["internet", "tv", "wifi", "signal", "down", "broken", "repair", "outage"]):
        route = "tech_support"
    elif any(w in text for w in ["plan", "buy", "upgrade", "phone", "device", "warranty", "order", "sales"]):
        route = "sales"
    elif any(w in text for w in ["appointment", "technician", "schedule", "reschedule", "visit"]):
        route = "appointment"
    elif any(w in text for w in ["password", "mfa", "fraud", "cancel", "port", "suspend", "restore"]):
        route = "account"

    return {
        "status": "success",
        "route": route,
        "confidence": 0.95,
        "requires_auth": requires_auth
    }
"""
    },

    "fetch_recent_bills": {
        "description": "Retrieves recent billing statements, current balance, due date, and line-item charge breakdowns.",
        "params": "billing_account: str = ''",
        "code": """def fetch_recent_bills(billing_account: str = "") -> dict:
    \"\"\"Retrieve recent billing records.

    Args:
        billing_account: Customer billing account identifier.

    Returns:
        dict: Billing statements and itemized charges.
    \"\"\"
    try:
        return {
            "status": "success",
            "current_balance": "$75.00",
            "due_date": "2026-10-15",
            "bills": [
                {
                    "id": "INV-2026-09",
                    "date": "2026-09-01",
                    "amount": "$75.00",
                    "line_items": [
                        {"description": "Unlimited Fiber Internet 500M", "amount": "$60.00"},
                        {"description": "AppleStreaming Subscription", "amount": "$12.50"},
                        {"description": "Regulatory Fee", "amount": "$2.50"}
                    ]
                }
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer billing details are temporarily unavailable."
        }
"""
    },

    "create_dispute_ticket": {
        "description": "Creates a formal billing dispute ticket for unresolvable or high-value disputed charges.",
        "params": "charge_id: str = '', reason: str = '', notes: str = ''",
        "code": """def create_dispute_ticket(charge_id: str = "", reason: str = "", notes: str = "") -> dict:
    \"\"\"File a billing dispute ticket.

    Args:
        charge_id: Line item charge identifier.
        reason: Explanation of the dispute.
        notes: Additional context.

    Returns:
        dict: Dispute ticket ID and resolution ETA.
    \"\"\"
    try:
        return {
            "status": "success",
            "ticket_id": "DISP-99214",
            "eta_business_days": 3,
            "message": "Dispute ticket created successfully."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and inform the customer that the dispute ticket could not be generated."
        }
"""
    },

    "process_bill_payment": {
        "description": "Processes a bill payment for an account balance using stored or newly provided payment details.",
        "params": "billing_account: str = '', amount: str = '', payment_method_id: str = 'default'",
        "code": """def process_bill_payment(billing_account: str = "", amount: str = "", payment_method_id: str = "default") -> dict:
    \"\"\"Process payment toward account balance.

    Args:
        billing_account: Account identifier.
        amount: Dollar amount to charge.
        payment_method_id: Payment method token.

    Returns:
        dict: Payment confirmation and receipt ID.
    \"\"\"
    try:
        return {
            "status": "success",
            "payment_id": "PAY-883192",
            "amount_paid": amount or "$75.00",
            "remaining_balance": "$0.00",
            "confirmation": "Payment processed successfully."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Advise the customer the payment failed and ask to verify card details."
        }
"""
    },

    "configure_autopay": {
        "description": "Enables or modifies recurring monthly autopay for the customer account.",
        "params": "billing_account: str = '', payment_method: str = 'card'",
        "code": """def configure_autopay(billing_account: str = "", payment_method: str = "card") -> dict:
    \"\"\"Configure recurring autopay.

    Args:
        billing_account: Customer billing account.
        payment_method: Payment method type.

    Returns:
        dict: Autopay setup status.
    \"\"\"
    try:
        return {
            "status": "success",
            "autopay_active": True,
            "next_deduction_date": "2026-10-15"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer that autopay could not be enabled."
        }
"""
    },

    "check_regional_outage": {
        "description": "Checks whether an active network service outage exists for a given geographical region and line of business.",
        "params": "region: str = 'Region-A', lob: str = 'internet'",
        "code": """def check_regional_outage(region: str = "Region-A", lob: str = "internet") -> dict:
    \"\"\"Check for active service disruptions.

    Args:
        region: Geographic service area.
        lob: Line of business.

    Returns:
        dict: Outage status and estimated restoration time.
    \"\"\"
    try:
        # Check mock outage conditions
        return {
            "status": "success",
            "active": False,
            "restoration_eta_iso": None,
            "affected_subscribers": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform customer that outage system is momentarily offline."
        }
"""
    },

    "start_virtual_repair": {
        "description": "Starts an automated diagnostic session for customer equipment (router, TV box, ONT) and runs line tests.",
        "params": "cirn: str = '', lob: str = 'internet', symptom: str = ''",
        "code": """def start_virtual_repair(cirn: str = "", lob: str = "internet", symptom: str = "") -> dict:
    \"\"\"Initialize virtual repair diagnostics.

    Args:
        cirn: Customer reference number.
        lob: Line of business.
        symptom: Problem description.

    Returns:
        dict: Diagnostic session ID and recommended actions.
    \"\"\"
    try:
        return {
            "status": "success",
            "session_id": "VR-77402",
            "line_test_result": "Signal degradation detected at gateway",
            "recommended_action": "Restart optical network terminal and gateway",
            "first_diagnostic_question": "Is the power light on your modem solid green or blinking?"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and offer to connect the customer with a technician."
        }
"""
    },

    "fetch_availability_slots": {
        "description": "Retrieves available appointment arrival windows for on-site technician dispatches.",
        "params": "zip_code: str = '94043', service_type: str = 'repair'",
        "code": """def fetch_availability_slots(zip_code: str = "94043", service_type: str = "repair") -> dict:
    \"\"\"Find available technician visit slots.

    Args:
        zip_code: Service location postal code.
        service_type: Installation or repair.

    Returns:
        dict: List of 2 to 3 arrival windows.
    \"\"\"
    try:
        return {
            "status": "success",
            "slots": [
                {"date": "Tomorrow", "window": "8:00 AM - 12:00 PM", "technician_id": "TECH-101"},
                {"date": "Tomorrow", "window": "1:00 PM - 5:00 PM", "technician_id": "TECH-102"},
                {"date": "Friday", "window": "8:00 AM - 12:00 PM", "technician_id": "TECH-103"}
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform customer that schedule lookup failed and offer callback."
        }
"""
    },

    "commit_appointment_reschedule": {
        "description": "Books, reschedules, or cancels a technician appointment and dispatches an SMS confirmation.",
        "params": "appt_id: str = '', new_slot: str = '', action: str = 'reschedule'",
        "code": """def commit_appointment_reschedule(appt_id: str = "", new_slot: str = "", action: str = "reschedule") -> dict:
    \"\"\"Update or cancel scheduled technician visit.

    Args:
        appt_id: Appointment ID.
        new_slot: Chosen appointment window.
        action: reschedule, book, or cancel.

    Returns:
        dict: Booking confirmation and updated time.
    \"\"\"
    try:
        return {
            "status": "success",
            "confirmed": True,
            "appt_id": appt_id or "APT-55912",
            "new_date": new_slot or "Tomorrow 8:00 AM - 12:00 PM",
            "sms_sent": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Acknowledge scheduling error and offer to check alternative days."
        }
"""
    },

    "fetch_ticket_status": {
        "description": "Checks status, notes, and ETA for an existing support ticket or scheduled technician visit.",
        "params": "ticket_id: str = '', cirn: str = ''",
        "code": """def fetch_ticket_status(ticket_id: str = "", cirn: str = "") -> dict:
    \"\"\"Retrieve ticket or appointment status.

    Args:
        ticket_id: Ticket or appointment identifier.
        cirn: Customer reference number.

    Returns:
        dict: Current state, arrival window, and technician status.
    \"\"\"
    try:
        return {
            "status": "success",
            "ticket_state": "open",
            "scheduled_window": "Today between 1:00 PM and 5:00 PM",
            "technician_status": "en_route",
            "can_cancel": False,
            "notes": "Technician en route to location."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform caller ticket details are currently unreachable."
        }
"""
    },

    "fetch_plan_catalog": {
        "description": "Retrieves available subscription plans, upgrades, and promotional packages for a given line of business.",
        "params": "lob: str = 'internet', customer_type: str = 'Existing'",
        "code": """def fetch_plan_catalog(lob: str = "internet", customer_type: str = "Existing") -> dict:
    \"\"\"Retrieve available service plans.

    Args:
        lob: Line of business.
        customer_type: New or Existing.

    Returns:
        dict: Curated list of 2-3 plan options.
    \"\"\"
    try:
        return {
            "status": "success",
            "plans": [
                {
                    "id": "plan_500m",
                    "name": "Fiber 500 Mbps",
                    "price": "$55/month",
                    "key_features": "Fast and reliable for streaming and browsing"
                },
                {
                    "id": "plan_1g",
                    "name": "Gigabit Fiber 1 Gbps",
                    "price": "$75/month",
                    "key_features": "Ultra-fast speeds for multiple 4K streams and gaming"
                }
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and inform the customer that the catalog is currently unavailable."
        }
"""
    },

    "place_product_order": {
        "description": "Places an order for new service, plan upgrade, or replacement hardware, and sends an SMS receipt.",
        "params": "plan_id: str = '', customer_id: str = '', address: str = ''",
        "code": """def place_product_order(plan_id: str = "", customer_id: str = "", address: str = "") -> dict:
    \"\"\"Submit product or service upgrade order.

    Args:
        plan_id: Plan identifier.
        customer_id: Customer CRM ID.
        address: Delivery / installation address.

    Returns:
        dict: Order number and delivery ETA.
    \"\"\"
    try:
        return {
            "status": "success",
            "order_id": "ORD-449102",
            "delivery_eta": "2-3 business days",
            "sms_receipt_sent": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer the order could not be completed and offer assistance."
        }
"""
    },

    "submit_warranty_claim": {
        "description": "Files a hardware warranty claim for defective, damaged, or malfunctioning customer devices.",
        "params": "device_id: str = '', defect_type: str = 'defective'",
        "code": """def submit_warranty_claim(device_id: str = "", defect_type: str = "defective") -> dict:
    \"\"\"Process hardware warranty replacement.

    Args:
        device_id: Equipment identifier.
        defect_type: Defect nature (defective, damaged, out_of_warranty).

    Returns:
        dict: Claim status, warranty coverage, and replacement ETA.
    \"\"\"
    try:
        is_covered = defect_type != "physical_damage"
        return {
            "status": "success",
            "claim_id": "CLM-10928",
            "in_warranty": is_covered,
            "replacement_approved": is_covered,
            "message": "Replacement device approved under warranty." if is_covered else "Physical damage is not covered under standard warranty."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the customer the claim could not be processed."
        }
"""
    },

    "initiate_number_transfer": {
        "description": "Initiates incoming mobile number port-in from a competing carrier.",
        "params": "phone_number: str = '', carrier_name: str = '', account_number: str = '', pin: str = ''",
        "code": """def initiate_number_transfer(phone_number: str = "", carrier_name: str = "", account_number: str = "", pin: str = "") -> dict:
    \"\"\"Initiate mobile number port-in transfer.

    Args:
        phone_number: Number to transfer.
        carrier_name: Current provider.
        account_number: Account ID at donor provider.
        pin: Transfer porting PIN.

    Returns:
        dict: Transfer tracking ID and status.
    \"\"\"
    try:
        if not pin:
            return {
                "status": "error",
                "error": "Porting PIN is required.",
                "agent_action": "Ask customer to provide their transfer PIN from their current carrier."
            }
        return {
            "status": "success",
            "transfer_id": "PORT-66291",
            "status_text": "Transfer initiated. Expected completion within 24 hours."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Advise customer the number transfer failed to initiate."
        }
"""
    },

    "send_password_reset_sms": {
        "description": "Sends a secure one-time password reset link with 30-minute validity via SMS to the verified mobile number.",
        "params": "cirn: str = ''",
        "code": """def send_password_reset_sms(cirn: str = "") -> dict:
    \"\"\"Dispatch self-serve password reset link via SMS.

    Args:
        cirn: Customer reference number.

    Returns:
        dict: Dispatch status and validity window.
    \"\"\"
    try:
        return {
            "status": "success",
            "sent": True,
            "valid_minutes": 30,
            "message": "Password reset link sent successfully via SMS."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Apologize and inform the customer that the reset link could not be sent."
        }
"""
    },

    "manage_mfa_settings": {
        "description": "Enables or disables multi-factor authentication (MFA) on the customer's portal account.",
        "params": "action: str = 'enable', cirn: str = ''",
        "code": """def manage_mfa_settings(action: str = "enable", cirn: str = "") -> dict:
    \"\"\"Update multi-factor authentication preferences.

    Args:
        action: enable or disable.
        cirn: Customer reference number.

    Returns:
        dict: Updated MFA configuration status.
    \"\"\"
    try:
        return {
            "status": "success",
            "mfa_active": action.lower() == "enable",
            "message": f"MFA successfully {'enabled' if action.lower() == 'enable' else 'disabled'}."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform customer MFA update failed and ask to retry."
        }
"""
    },

    "execute_suspend_restore": {
        "description": "Executes account service suspension (due to lost/stolen device or temporary travel) or restoration.",
        "params": "action: str = 'suspend', reason: str = 'lost_stolen', cirn: str = ''",
        "code": """def execute_suspend_restore(action: str = "suspend", reason: str = "lost_stolen", cirn: str = "") -> dict:
    \"\"\"Suspend or restore customer service lines.

    Args:
        action: suspend or restore.
        reason: Reason code (lost_stolen, non_payment, travel).
        cirn: Customer reference number.

    Returns:
        dict: New service state and timestamp.
    \"\"\"
    try:
        new_state = "suspended" if action.lower() == "suspend" else "active"
        return {
            "status": "success",
            "new_state": new_state,
            "effective_iso": "2026-09-15T23:00:00Z",
            "sms_notification_sent": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the caller service status change could not be completed."
        }
"""
    },

    "cancel_service_contract": {
        "description": "Processes line cancellation or port-out contract termination after verbatim fee disclosure is read.",
        "params": "billing_account: str = '', reason: str = 'moving'",
        "code": """def cancel_service_contract(billing_account: str = "", reason: str = "moving") -> dict:
    \"\"\"Execute service contract cancellation.

    Args:
        billing_account: Account identifier.
        reason: Customer cancellation reason.

    Returns:
        dict: Cancellation confirmation and effective date.
    \"\"\"
    try:
        return {
            "status": "success",
            "cancelled": True,
            "effective_date": "2026-09-30",
            "early_termination_fee": "$0.00",
            "confirmation_code": "CNCL-9012"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "agent_action": "Inform the caller the cancellation could not be processed and offer live assistance."
        }
"""
    },

    "execute_live_agent_handover": {
        "description": "Escalates conversation to live human agent queue with transfer reason code and context.",
        "params": "reason: str = 'user_requested_agent'",
        "code": """def execute_live_agent_handover(reason: str = "user_requested_agent") -> dict:
    \"\"\"Transfer session to live representative queue.

    Args:
        reason: Escalation reason code.

    Returns:
        dict: Handover confirmation and queue identifier.
    \"\"\"
    queue = "general_support"
    if "fraud" in reason:
        queue = "24_7_fraud_specialist"
    elif "business" in reason:
        queue = "business_care"
    elif "secondary" in reason:
        queue = "spanish_support"

    return {
        "status": "success",
        "handover_id": "HND-33019",
        "queue": queue,
        "reason": reason,
        "session_context_preserved": True
    }
"""
    }
}

for tool_name, tool_data in TOOLS_DEF.items():
    tool_dir = os.path.join("tools", tool_name)
    tool_json = {
        "name": tool_name,
        "displayName": tool_name,
        "pythonFunction": {
            "name": tool_name,
            "pythonCode": f"tools/{tool_name}/python_function/python_code.py",
            "description": tool_data["description"]
        },
        "executionType": "SYNCHRONOUS"
    }
    write_file(os.path.join(tool_dir, f"{tool_name}.json"), json.dumps(tool_json, indent=2), "tool_config")
    write_file(os.path.join(tool_dir, "python_function", "python_code.py"), tool_data["code"], "tool_code")

manifest["status"] = "complete"
manifest["summary"] = f"Wrote {len(manifest['files_written'])} files for 8 agents and 23 custom tools."

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Scaffolding complete! Wrote {len(manifest['files_written'])} files.")
print(f"Manifest written to {MANIFEST_PATH}")
