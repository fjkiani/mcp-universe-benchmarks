"""MCP Client Service - Calls MCP servers via stdio or gateway"""
import os
import json
import asyncio
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path

# Try to import MCP client library (if available)
try:
    from lbx_cli.mcpuniverse.mcp.manager import MCPManager
    from lbx_cli.mcpuniverse.mcp.client import MCPClient
    MCP_LIBRARY_AVAILABLE = True
except ImportError:
    MCP_LIBRARY_AVAILABLE = False

# Mock mode for demo (enabled by default for immediate demo use)
# Set DEMO_MOCK_MODE=false to use real MCP servers (requires API keys)
DEMO_MOCK_MODE = os.getenv("DEMO_MOCK_MODE", "true").lower() == "true"

# MCP servers path
PROJECT_ROOT = Path(__file__).parent.parent.parent
SERVERS_PATH = PROJECT_ROOT / "lbx_mcp_universe_mcp_servers_mothership" / "servers"


class MCPClientService:
    """Service to call MCP server tools"""
    
    def __init__(self):
        self._clients = {}
        self._manager = None
        
        if MCP_LIBRARY_AVAILABLE:
            try:
                # Try to initialize MCP manager
                config_path = PROJECT_ROOT / "central" / "mcp-config.yaml"
                if config_path.exists():
                    self._manager = MCPManager(config=str(config_path))
            except Exception as e:
                print(f"Warning: Could not initialize MCP Manager: {e}")
    
    async def call_tool(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP server tool
        
        Args:
            server_name: Name of MCP server (nexhealth, twilio_hipaa, videosdk, assemblyai)
            tool_name: Name of tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result as dictionary
        """
        # Mock mode for demo
        if DEMO_MOCK_MODE:
            return self._get_mock_response(server_name, tool_name, arguments)
        
        # Try MCP library first
        if self._manager and MCP_LIBRARY_AVAILABLE:
            try:
                return await self._call_via_library(server_name, tool_name, arguments)
            except Exception as e:
                print(f"MCP library call failed: {e}, trying direct stdio...")
        
        # Fallback: Direct stdio call
        try:
            return await self._call_via_stdio(server_name, tool_name, arguments)
        except Exception as e:
            print(f"Direct stdio call failed: {e}, using mock response...")
            return self._get_mock_response(server_name, tool_name, arguments)
    
    async def _call_via_library(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call MCP tool via MCP client library"""
        if not self._manager:
            raise ValueError("MCP Manager not initialized")
        
        # Build client if not cached
        if server_name not in self._clients:
            self._clients[server_name] = await self._manager.build_client(
                server_name, 
                transport="stdio"
            )
        
        client = self._clients[server_name]
        
        # Call tool
        result = await client.call_tool(tool_name, arguments)
        
        # Parse JSON string response
        if isinstance(result, str):
            return json.loads(result)
        return result
    
    async def _call_via_stdio(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call MCP tool via direct stdio subprocess"""
        server_path = SERVERS_PATH / server_name / "server.py"
        
        if not server_path.exists():
            raise FileNotFoundError(f"MCP server not found: {server_path}")
        
        # For now, return mock (direct stdio requires more complex setup)
        # In production, would use MCP stdio protocol
        return self._get_mock_response(server_name, tool_name, arguments)
    
    def _get_mock_response(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate mock response for demo"""
        
        # NexHealth mocks
        if server_name == "nexhealth":
            if tool_name == "book_appointment":
                return {
                    "appointment_id": f"appt_{arguments.get('provider_id', 'xxx')}_{arguments.get('start_time', '')[:10]}",
                    "provider_id": arguments.get("provider_id", "dr_smith"),
                    "patient_id": arguments.get("patient_id", "pat_123"),
                    "start_time": arguments.get("start_time"),
                    "end_time": arguments.get("end_time"),
                    "status": "booked",
                    "nexhealth_id": f"nex_{arguments.get('provider_id', 'xxx')}",
                    "ehr_synced": True,
                    "message": "Appointment booked successfully (MOCK)"
                }
            elif tool_name == "check_provider_availability":
                return {
                    "provider_id": arguments.get("provider_id", "dr_smith"),
                    "start_date": arguments.get("start_date"),
                    "end_date": arguments.get("end_date"),
                    "available_slots": [
                        {"time": "09:00", "available": True},
                        {"time": "10:00", "available": True},
                        {"time": "14:00", "available": True}
                    ],
                    "total_slots": 3,
                    "status": "success"
                }
            elif tool_name == "verify_insurance_eligibility":
                return {
                    "eligibility_status": "active",
                    "active": True,
                    "coverage_start": "2024-01-01",
                    "coverage_end": "2024-12-31",
                    "benefits": {
                        "copay": "$50",
                        "deductible": "$500",
                        "out_of_pocket_max": "$5000"
                    },
                    "insurance_company": arguments.get("insurance_member_id", "Unknown"),
                    "member_id": arguments.get("insurance_member_id", "ABC123"),
                    "verified_at": "2024-01-15T10:00:00Z",
                    "status": "success"
                }
        
        # Twilio HIPAA mocks
        elif server_name == "twilio_hipaa":
            if tool_name == "send_hipaa_sms":
                # Check for PHI in message
                message = arguments.get("message", "")
                phi_detected = []
                
                # Simple PHI detection
                phi_keywords = ["diabetes", "hypertension", "MRN", "SSN", "diagnosed", "medication"]
                for keyword in phi_keywords:
                    if keyword.lower() in message.lower():
                        phi_detected.append(keyword)
                
                if phi_detected and not arguments.get("allow_phi", False):
                    return {
                        "error": "PHI detected in message",
                        "phi_types": phi_detected,
                        "message_preview": message[:100],
                        "suggestion": "Use generic message",
                        "hipaa_compliant": False,
                        "blocked": True
                    }
                
                return {
                    "message_sid": "SM" + "x" * 32,
                    "status": "queued",
                    "to": arguments.get("to", "+15551234567"),
                    "from": arguments.get("from_number", "+15559876543"),
                    "body": message,
                    "num_segments": 1,
                    "direction": "outbound-api",
                    "date_created": "2024-01-15T10:00:00Z",
                    "hipaa_compliant": True,
                    "phi_detected": phi_detected,
                    "phi_filtered": len(phi_detected) > 0
                }
        
        # VideoSDK mocks
        elif server_name == "videosdk":
            if tool_name == "create_video_room" or tool_name == "create_room":
                room_id = arguments.get("custom_room_id") or f"room_{arguments.get('room_name', 'xxx')}"
                return {
                    "room_id": room_id,
                    "room_name": arguments.get("room_name", "Consultation Room"),
                    "enabled_recording": arguments.get("enabled_recording", True),
                    "enabled_screen_share": arguments.get("enabled_screen_share", True),
                    "enabled_chat": arguments.get("enabled_chat", True),
                    "status": "created",
                    "patient_link": f"https://videosdk.live/room/{room_id}?token=patient_token",
                    "provider_link": f"https://videosdk.live/room/{room_id}?token=provider_token"
                }
            elif tool_name == "generate_token":
                return {
                    "token": "demo_mock_token_123",
                    "join_link": "https://videosdk.live/room/mock?token=demo_mock_token_123",
                    "expires_in": 3600
                }
            elif tool_name == "start_recording":
                return {
                    "recording_id": f"rec_{arguments.get('room_id', 'mock')}",
                    "status": "recording"
                }
            elif tool_name == "stop_recording":
                return {
                    "recording_url": "https://videosdk.live/mock_recording.mp4",
                    "download_url": "https://videosdk.live/mock_recording.mp4",
                    "status": "stopped"
                }
        
        # AssemblyAI mocks
        elif server_name == "assemblyai":
            if tool_name == "transcribe_medical" or tool_name == "transcribe_audio":
                mock_transcript = (
                    "Provider: Hello, I'm Dr. Smith. I understand you're experiencing a severe headache with some visual changes today?\n"
                    "Patient: Yes, it started about two hours ago. I got these jagged, flashing lights in my right eye, and then a really bad throbbing pain on the left side of my head.\n"
                    "Provider: I see. That visual disturbance is what we call an aura, and it's classic for a migraine. Have you had these before?\n"
                    "Patient: I used to get them in college, but I haven't had one in years. I was worried it might be something worse.\n"
                    "Provider: It's good you got it checked out. Given the classic pattern and your history, a migraine is the most likely culprit. Are you having any weakness, numbness, or trouble speaking?\n"
                    "Patient: No, nothing like that. Just the pain and a bit of nausea.\n"
                    "Provider: Okay, your intake vitals looked stable. Blood pressure is 120/80. I'll prescribe some Sumatriptan to help abort the migraine. I also want you to rest in a dark, quiet room and stay hydrated.\n"
                    "Patient: Thank you, Dr. Smith. I'll do that. \n"
                    "Provider: If the pain doesn't improve in the next several hours, or if you develop new symptoms like weakness, please go to the nearest emergency room. Otherwise, let's schedule a follow-up in 4 weeks to see if these are recurring."
                )
                return {
                    "transcript_id": "trans_" + "x" * 20,
                    "status": "completed",
                    "transcript": mock_transcript,
                    "confidence": 0.965,
                    "audio_duration": 120,
                    "medical_entities": {
                        "symptoms": ["chest pain"],
                        "duration": ["2 hours"],
                        "vital_signs": ["blood pressure 140/90"],
                        "medications": [],
                        "conditions": []
                    }
                }
        
        # Default mock
        return {
            "status": "success",
            "message": f"Mock response for {server_name}.{tool_name}",
            "arguments": arguments
        }


# Global instance
mcp_client_service = MCPClientService()

