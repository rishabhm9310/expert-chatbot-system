# logic_layer.py
from pyDatalog import pyDatalog

# Declare predicate and variable terms
pyDatalog.create_terms('intent, entity, response, response_entity, policy, escalate, fallback')
pyDatalog.create_terms('I, E, Text, Confidence, Reason')
pyDatalog.create_terms('low_confidence, medium_confidence, force_escalation, urgent_escalation')
pyDatalog.create_terms('clarification, follow_up, slot, has_entity')

# --- Knowledge base: responses ---
# Response(Text) is the answer string for a given intent; entity specialization is optional.

# Billing inquiries
+response('billing_inquiry', 'Your billing cycle is monthly. You can view invoices in the Billing section of your account.')
+response('refund_status', 'Refunds are processed within 5-7 business days after approval.')
+response('invoice_request', 'You can download invoices from Account Settings -> Billing -> Invoice History. Need a specific invoice? Share the date and I\'ll help locate it.')

# Technical issues
+response('password_reset', 'To reset your password, use "Forgot Password" on the login page. Check spam for the reset email.')
+response('app_crash', 'Please update to the latest app version. If it still crashes, share logs via Settings -> Diagnostics.')
+response('bug_report', 'Thanks for reporting! Please describe the issue in detail and share screenshots if possible. Our team will investigate within 24-48 hours.')

# Order tracking
+response('order_status', 'You can track your order in My Orders -> Track. Share your order ID if you need me to check.')

# General info
+response('business_hours', 'Our support hours are 9:00-18:00 IST, Monday to Friday.')
+response('pricing', 'We offer Basic, Pro, and Enterprise plans. Pricing details are on the Plans page in your dashboard.')

# Account management
+response('cancel_subscription', 'You can cancel anytime from Account Settings -> Subscription -> Cancel. You\'ll retain access until the end of your billing period.')
+response('upgrade_plan', 'Great! You can upgrade from Account Settings -> Subscription -> Change Plan. Upgrades are prorated.')
+response('downgrade_plan', 'You can downgrade from Account Settings -> Subscription -> Change Plan. Changes take effect at the next billing cycle.')
+response('account_creation', 'Sign up at our homepage! Click "Get Started" and follow the steps. The Basic plan includes a 14-day free trial.')
+response('multiple_accounts', 'You can create separate accounts for different uses. For team features, check out our Team Plan with shared workspaces.')

# Security & Privacy
+response('account_security', 'Enable 2FA in Account Settings -> Security for extra protection. Use a strong, unique password and review login activity regularly.')
+response('data_export', 'Export your data from Account Settings -> Privacy -> Download Data. You\'ll receive a link within 24 hours.')

# Features & Integration
+response('feature_request', 'We love hearing ideas! Submit feature requests at feedback.example.com or via the Feedback button in your dashboard.')
+response('integration_help', 'We integrate with 100+ tools. Check our Integration Directory or visit docs.example.com/integrations for setup guides.')
+response('mobile_app', 'Download our app from the App Store (iOS) or Google Play Store (Android). Search "YourApp Support".')
+response('notification_settings', 'Manage notifications in Account Settings -> Notifications. You can customize email, SMS, and push alerts.')

# Trial & Special requests
+response('trial_extension', 'Trial extensions are handled case-by-case. I\'m escalating to our support team who can review your request.')
+response('shipping_policy', 'Shipping depends on the shipping option selected. Standard shipping typically takes 5-7 business days.')
+response('cancel_refund', 'If you cancel within the trial, you will not be charged. For refunds after purchase, please share your order ID to check eligibility.')
+response('payment_methods', 'We accept credit card, PayPal, and bank transfer for Enterprise plans. Add or update payment methods in Account Settings -> Billing.')
+response('subscription_pause', 'You can pause your subscription from Account Settings -> Subscription -> Pause. Pauses are limited to one per billing year.')
+response('subscription_resume', 'Resume from the same Subscription page. If your payment method failed, update it before resuming to avoid interruption.')
+response('update_payment_method', 'To update payment details, go to Account Settings -> Billing -> Payment Methods. We accept Visa, MasterCard, and Amex.')
+response('promo_codes', 'Apply promo codes at checkout. If a code is invalid, check expiry date or contact support with the code.')
+response('api_rate_limits', 'API rate limits depend on your plan. Pro allows 1,000 requests/min and Enterprise is higher — consult your plan docs.')
+response('sla_uptime', 'Our SLA guarantees 99.9% uptime for Enterprise customers. See your contract for exact terms.')
+response('data_retention', 'Data is retained according to your selected plan. Export or delete data from Account Settings -> Privacy.')
+response('gdpr_request', 'To submit a GDPR request, use Account Settings -> Privacy -> GDPR Requests or contact privacy@example.com.')
+response('connect_support_agent', 'Connecting you to a support agent. Please provide your account email and a brief description of the issue.')
+response('agent_unavailable', 'All agents are currently busy. I can create a ticket and have someone follow up within 24 hours. Would you like that?')
+response('escalation_ack', 'Your issue has been escalated to our specialist team. They will contact you shortly.')
+response('greet', 'Hello! How can I assist you today?')
+response('goodbye', 'Goodbye! If you need anything else, feel free to reach out.')
+response('smalltalk_thanks', 'You\'re welcome! Happy to help.')
+response('smalltalk_welcome', 'It\'s my pleasure to help. What would you like to do next?')
+response('unknown_query', 'I\'m not sure I understand. Can you rephrase or give more details?')

# --- Policies ---
# Some intents require escalation under conditions (e.g., account locked).
# Use + to assert facts so pyDatalog registers them

 # assert facts
+policy('force_escalation_required', 'account_locked')
+policy('force_escalation_required', 'payment_dispute')
+policy('force_escalation_required', 'trial_extension')
+policy('force_escalation_required', 'data_export')  # May need verification
+policy('force_escalation_required', 'cancel_subscription')  # Retention team handles
+policy('urgent_escalation', 'fraud_report')
+policy('urgent_escalation', 'data_breach')

# --- Shipping & Returns ---
+response('shipping_estimate', 'Shipping estimates vary by destination and shipping method. Provide your postal code for a more accurate estimate.')
+response('tracking_number_help', 'You can find your tracking number in the order confirmation email or on the receipt.')
+response('start_return', 'To start a return, go to My Orders -> Return Item and follow the steps. Need help with a specific order? Share the order ID.')
+response('return_policy', 'Items can be returned within 30 days in original condition. Some items (like perishables) may be excluded.')

# --- Developer / API ---
+response('api_docs', 'Our API docs are at docs.example.com/api. Which endpoint are you interested in?')
+response('webhook_setup', 'To set up a webhook, provide a secure HTTPS endpoint and an optional secret for signature verification.')
+response('sso_setup', 'We support SAML and OIDC SSO providers. Which identity provider are you using?')
+response('rate_limit_exceeded', 'You\'ve hit the rate limit. Consider exponential backoff or upgrading your plan for higher limits.')

# --- Onboarding & Usage ---
+response('getting_started', 'Start by creating a project, inviting team members, and connecting one integration. Would you like a guided tour?')
+response('first_steps', 'Try creating a sample item and inviting a teammate to collaborate. Want me to walk through those steps?')

# --- Security & SSO ---
+response('account_recovery', 'If you can\'t access your account, use the account recovery flow at the login page or contact support with your registered email.')
+response('sso_error', 'SSO errors can result from clock skew or incorrect metadata. Double-check the provider configuration and certificates.')

# --- Webhooks & Integrations ---
+response('webhook_events', 'We can send events for order.created, order.updated, invoice.paid and more. Which events do you need?')
+response('webhook_retry_policy', 'We retry webhook delivery with exponential backoff up to 5 attempts. Failed deliveries are logged in the Dashboard.')

# --- Performance & Reliability ---
+response('slow_performance', 'Sorry about the slowness. Can you share when it happens and a sample request so we can investigate?')
+response('incident_status', 'Our status page (status.example.com) shows live incidents and maintenances. Provide an incident ID if you have one.')

# --- Analytics & Logging ---
+response('analytics_setup', 'Connect your analytics property ID in Settings -> Integrations. We support Google Analytics and segments.')
+response('logs_access', 'Access logs from the Dashboard -> Diagnostics. For deeper analysis we can provide export options.')

# --- Legal & Compliance ---
+response('subpoena_request', 'Legal requests like subpoenas should be sent to legal-requests@example.com with valid documentation.')
+response('privacy_policy', 'Our privacy policy is at example.com/privacy. For specific data questions, provide your account email and timeframe.')
+policy('legal_escalation', 'subpoena_request')

# --- Accessibility & Localization ---
+response('accessibility', 'We aim to support accessibility standards (WCAG). Please report any accessibility issue with steps to reproduce.')
+response('localization', 'We support English, Spanish, and French in the UI. Which language do you prefer?')

# --- Entity & slot additions for new categories ---
+slot('tracking_number')
+slot('return_id')
+slot('sso_provider')
+slot('webhook_url')
+slot('incident_id')
+slot('analytics_property')

# --- Entity-aware sample responses ---
+response_entity('shipping_estimate', 'postal_code', 'Estimated delivery to {postal_code}: 3-7 business days.')
+response_entity('tracking_number_help', 'tracking_number', 'Looking up tracking number {tracking_number} now...')
+response_entity('start_return', 'order_id', 'Initiating return for order {order_id}. I\'ll send you the return label instructions.')
+response_entity('webhook_setup', 'webhook_url', 'Validating webhook URL {webhook_url} and checking reachability...')


# Escalate on low confidence or forced policy triggers
# We express escalation conditions with helper rules.

low_confidence(Confidence) <= (Confidence < 0.4)  # very low
medium_confidence(Confidence) <= (Confidence >= 0.4) & (Confidence < 0.75)

force_escalation(I) <= policy('force_escalation_required', I)
urgent_escalation(I) <= policy('urgent_escalation', I)

# Escalation rules:
escalate(I, Confidence, Reason) <= (low_confidence(Confidence)) & (Reason == 'low_confidence')
escalate(I, Confidence, Reason) <= (force_escalation(I)) & (Reason == 'policy')
escalate(I, Confidence, Reason) <= (urgent_escalation(I)) & (Reason == 'urgent')

# Clarification / follow-up rules
# If medium confidence, ask a clarification question rather than escalating
clarification(I, 'Could you give a bit more detail?') <= medium_confidence(Confidence) & (I == I)
follow_up('refund_status', 'Do you have a refund ID or order ID?')
follow_up('order_status', 'Please share your order ID so I can look it up.')

 # Entity-aware responses: prefer `response_entity(intent, entity, text)` when entity present
response_entity('order_status', 'order_id', 'Thanks — checking order {order_id}.')
response_entity('refund_status', 'refund_id', 'Thanks — checking refund {refund_id}.')

# has_entity(I, E) can be asserted at runtime when an entity is detected
# slot definitions (informational)
slot('order_id')
slot('refund_id')
slot('account_email')

# Fallback when no response or entity-based response is defined
fallback(I) <= ~(response(I, Text)) & ~(response_entity(I, E, Text))
