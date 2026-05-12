/// <reference types="vite/client" />
/**
 * Central API configuration — all pages import API_BASE from here.
 * Set VITE_API_URL in .env.local for local dev,
 * or in Netlify/Render env vars for production.
 */
export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

export const ENDPOINTS = {
    // Healthcare Demo
    verifyInsurance: `${API_BASE}/api/v1/demo/healthcare/verify-insurance`,
    transcribeAudio: `${API_BASE}/api/v1/demo/healthcare/transcribe-audio`,
    sendSms: `${API_BASE}/api/v1/demo/healthcare/send-sms`,
    bookAppointment: `${API_BASE}/api/v1/demo/healthcare/book-appointment`,
    createPatient: `${API_BASE}/api/v1/demo/healthcare/create-patient`,
    triage: `${API_BASE}/api/v1/demo/healthcare/triage`,
    createVideoRoom: `${API_BASE}/api/v1/demo/healthcare/create-video-room`,
    // Agent
    agentChat: `${API_BASE}/api/v1/agent/chat`,
    agentHealth: `${API_BASE}/api/v1/agent/health`,
    // Dashboard
    servers: `${API_BASE}/api/v1/servers`,
    sprintMetrics: `${API_BASE}/api/v1/sprint/metrics`,
} as const
