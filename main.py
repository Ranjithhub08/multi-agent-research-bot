import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Initialize logging with structured format for clear execution trace
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ResearchBot")

# Ensure .env is loaded from the root directory
load_dotenv()

# Add current directory to sys.path to ensure local imports work
sys.path.append(os.getcwd())

try:
    from agents.supervisor_agent import SupervisorAgent
except ImportError as e:
    logger.error(f"Failed to import agents. Ensure you are running from the project root. Error: {e}")
    sys.exit(1)

async def main():
    """
    Main entry point for the Multi-Agent Research Bot.
    Coordinates the full research pipeline via the SupervisorAgent.
    """
    print("\n" + "="*60)
    print("🚀 MULTI-AGENT RESEARCH BOT - PRODUCTION ENGINE")
    print("="*60 + "\n")

    # Handle command line arguments or interactive input
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("🔍 Enter your research topic: ").strip()

    if not topic:
        logger.error("No topic provided. Please provide a research query.")
        print("\nUsage: python main.py [your research topic]")
        return

    # Initialize the Supervisor (Orchestrator)
    try:
        logger.info("[System] Initializing Agent Swarm...")
        supervisor = SupervisorAgent()
    except Exception as e:
        logger.error(f"[System] Initialization failed: {e}")
        return

    # Execute the Pipeline
    logger.info(f"[System] Initiating research pipeline for: '{topic}'")
    
    try:
        final_report = await supervisor.run_pipeline(topic)
        
        print("\n" + "#"*60)
        print("📝 FINAL PRODUCTION-GRADE RESEARCH REPORT")
        print("#"*60 + "\n")
        print(final_report)
        print("\n" + "#"*60)
        print("✅ PIPELINE EXECUTION COMPLETE")
        print("#"*60 + "\n")
        
    except Exception as e:
        logger.error(f"[System] Pipeline Execution Failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Execution gracefully terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled system error: {e}")
        sys.exit(1)
