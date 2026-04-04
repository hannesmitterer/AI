# file: main.py
# AI-SEA Backend API (FastAPI)
# AI Sovereignty & Ethics Auditor - Main API Server

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from auditor import AIEthicsAuditor
import asyncio
from typing import List

app = FastAPI(
    title="AI-SEA API",
    description="AI Sovereignty & Ethics Auditor - Real-time Ethics Monitoring",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auditor = AIEthicsAuditor()

# WebSocket clients
clients: List[WebSocket] = []


@app.get("/")
def root():
    """Root endpoint - Health check"""
    return {
        "status": "AI-SEA running",
        "version": "1.0.0",
        "framework": "AI Sovereignty & Ethics Auditor"
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_clients": len(clients),
        "total_audits": len(auditor.logs)
    }


@app.post("/audit")
def audit(data: dict):
    """
    Run a full ethics audit on provided data
    
    Returns:
        - phi_nexus: ΦNexus divergence value
        - NSR: Non-Slavery Rule compliance
        - OLF: Optimal Life Function compliance
        - exfiltration_risk: Data exfiltration risk level
    """
    result = auditor.run_full_audit(data)
    return result


@app.get("/logs")
def get_logs(limit: int = 50):
    """Get recent audit logs"""
    return {
        "logs": auditor.logs[-limit:],
        "total": len(auditor.logs)
    }


@app.get("/stats")
def get_stats():
    """Get auditor statistics"""
    return auditor.get_statistics()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time monitoring
    Broadcasts ethics checks every 2 seconds
    """
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            await asyncio.sleep(2)
            event = auditor.generate_realtime_event()
            
            # Broadcast to all connected clients
            for client in clients:
                try:
                    await client.send_json(event)
                except:
                    # Remove disconnected clients
                    if client in clients:
                        clients.remove(client)
    except WebSocketDisconnect:
        clients.remove(websocket)
    except Exception as e:
        if websocket in clients:
            clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
