"""
WebSocket support for real-time scan updates.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime

class WebSocketManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        # scan_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, scan_id: str):
        """Accept WebSocket connection for a scan."""
        await websocket.accept()
        
        if scan_id not in self.active_connections:
            self.active_connections[scan_id] = []
        
        self.active_connections[scan_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, scan_id: str):
        """Remove WebSocket connection."""
        if scan_id in self.active_connections:
            if websocket in self.active_connections[scan_id]:
                self.active_connections[scan_id].remove(websocket)
            
            # Clean up empty scan connections
            if not self.active_connections[scan_id]:
                del self.active_connections[scan_id]
    
    async def send_scan_update(self, scan_id: str, status: str, progress: int, message: str = ""):
        """Send scan update to all connected clients for a scan."""
        if scan_id not in self.active_connections:
            return
        
        update_data = {
            "type": "scan_update",
            "scan_id": scan_id,
            "data": {
                "status": status,
                "progress": progress,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        # Send to all connected clients for this scan
        disconnected = []
        for websocket in self.active_connections[scan_id]:
            try:
                await websocket.send_text(json.dumps(update_data))
            except:
                # Mark for removal if connection is dead
                disconnected.append(websocket)
        
        # Clean up dead connections
        for websocket in disconnected:
            self.disconnect(websocket, scan_id)
    
    async def send_issue_found(self, scan_id: str, issue_data: dict):
        """Send real-time issue notification."""
        if scan_id not in self.active_connections:
            return
        
        message_data = {
            "type": "issue_found",
            "scan_id": scan_id,
            "data": {
                "issue": issue_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        disconnected = []
        for websocket in self.active_connections[scan_id]:
            try:
                await websocket.send_text(json.dumps(message_data))
            except:
                disconnected.append(websocket)
        
        for websocket in disconnected:
            self.disconnect(websocket, scan_id)

# Global WebSocket manager instance
websocket_manager = WebSocketManager()

async def websocket_endpoint(websocket: WebSocket, scan_id: str):
    """WebSocket endpoint for scan updates."""
    await websocket_manager.connect(websocket, scan_id)
    
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            
            # Handle client messages (ping/pong, etc.)
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }))
            except json.JSONDecodeError:
                pass
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, scan_id)