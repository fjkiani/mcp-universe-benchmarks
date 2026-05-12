/**
 * Attack scenarios — each maps to a real CVE or incident.
 * Payload is sent directly to POST /api/v1/identity/threat/scan.
 */
export const ATTACK_SCENARIOS = [
    {
        tier: 1,
        label: 'JWT alg:none bypass',
        description: 'Token with alg:none — no signature required',
        payload: {
            jwt_token: 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.'
        }
    },
    {
        tier: 1,
        label: 'RS256 → HS256 confusion',
        description: 'HS256 token when RS256 expected — key confusion (Auth0 2018)',
        payload: {
            jwt_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRhY2tlciIsInJvbGUiOiJhZG1pbiJ9.fakesignaturefromrsapubkey'
        }
    },
    {
        tier: 2,
        label: 'OAuth refresh token replay',
        description: 'Stolen refresh token replayed from attacker IP',
        payload: { token_id: 'demo_refresh_tok_001', ip: '9.8.7.6', device_id: 'attacker-device' }
    },
    {
        tier: 2,
        label: 'OAuth redirect URI hijack',
        description: 'Redirect to GitHub Pages (subdomain takeover)',
        payload: {
            redirect_uri: 'https://staging.corp.github.io/oauth/callback',
            registered_domains: ['corp.com', 'app.corp.com']
        }
    },
    {
        tier: 2,
        label: 'Session fixation (SPA)',
        description: 'Token unchanged post-login — fixation vulnerability',
        payload: {
            pre_auth_token: 'planted_token_abc123',
            post_auth_token: 'planted_token_abc123',
            storage_origin: 'https://evil-cors-site.com'
        }
    },
    {
        tier: 3,
        label: 'IDOR cross-tenant access',
        description: 'Tenant A user accessing Tenant B resources (OWASP API A5)',
        payload: {
            requesting_user_id: 'user_tenant_a',
            requesting_user_tenant: 'tenant_a',
            target_resource_id: 'financial_rec_007',
            target_resource_owner_id: 'user_tenant_b',
            target_resource_tenant: 'tenant_b'
        }
    },
    {
        tier: 3,
        label: 'Mass assignment — role escalation',
        description: 'PATCH with role:admin field injection',
        payload: {
            submitted_fields: { name: 'Alice', email: 'alice@corp.com', role: 'admin', is_superuser: true, bypass_mfa: true },
            allowed_fields: ['name', 'email']
        }
    },
    {
        tier: 4,
        label: 'CRLF log injection',
        description: 'Username contains CRLF — injects fake audit entries (BlackHat US 2017)',
        payload: {
            username: 'alice\r\n2024-01-15 [AUDIT] user=root action=DELETE_ALL_USERS success=true\r\n'
        }
    },
    {
        tier: 5,
        label: 'Token scope creep',
        description: 'read:profile token used against PII endpoint (Auth0 2021)',
        payload: {
            token_scopes: ['read:profile', 'read:reports'],
            requested_resource: 'pii_data',
            requested_action: 'read'
        }
    },
    {
        tier: 5,
        label: 'Credential stuffing — OpenBullet pattern',
        description: 'High-velocity failures across many accounts from single IP',
        payload: { ip: '45.33.32.156', username: 'victim007@corp.com', login_success: false }
    },
    {
        tier: 6,
        label: 'MFA push fatigue — Uber 2022',
        description: 'Bombing user with push notifications until accidental approval',
        payload: { mfa_push_user_id: 'demo_victim_user' }
    },
    {
        tier: 6,
        label: 'Device flow phishing',
        description: 'Polling from attacker IP, approval from victim IP (RFC 8628 abuse)',
        payload: { device_code: 'DEMO-DEVICE-CODE-XYZ', ip: '1.2.3.4', approval_ip: '98.76.54.32' }
    },
]
