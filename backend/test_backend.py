import asyncio
import sys
import os

# Add the parent directory to path so we can import backend as a package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agent_manager import AgentManager

async def test_full_workflow():
    print("🚀 Initializing Swarm Test...")
    manager = AgentManager()
    topic = "Future of Multi-Agent Systems 2025"
    
    print(f"📝 Topic: {topic}\n")
    
    async for update in manager.run_with_stream(topic):
        agent = update.get("agent", "Unknown")
        message = update.get("message", "No message")
        print(f"   [{agent}] -> {message}")
        if "finalReport" in update:
            print("\n✅ MISSION COMPLETE\n")
            print(update["finalReport"][:300] + "...")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())
