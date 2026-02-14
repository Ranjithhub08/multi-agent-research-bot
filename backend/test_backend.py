import asyncio
import sys
import os

# Add the parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.orchestrator import ResearchOrchestrator

async def test_full_workflow():
    print("🚀 Initializing Test for Autonomous Research Swarm...")
    orchestrator = ResearchOrchestrator()
    topic = "Impact of Multi-Agent Systems on Software Engineering 2024"
    
    print(f"📝 Testing topic: {topic}\n")
    
    # Test streaming
    print("📡 Testing Real-time Stream Logging:")
    async for update in orchestrator.run_with_stream(topic):
        agent = update.get("agent", "Unknown")
        message = update.get("message", "No message")
        print(f"   [{agent}] -> {message}")
        if "finalReport" in update:
            print("\n✅ Final Report Received!\n")
            print("-" * 50)
            print(update["finalReport"][:500] + "...")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_full_workflow())
