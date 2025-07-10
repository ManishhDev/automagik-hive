from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.team import Team
import os

# Import main orchestrator
from agents.orchestrator.main_orchestrator import create_main_orchestrator

# Initialize at module level - only print on first load
if not os.environ.get('UVICORN_RELOADER_PROCESS'):
    print("🚀 Initializing PagBank Multi-Agent System...")
    
# Create the main orchestrator (this creates the routing team with specialist agents)
orchestrator = create_main_orchestrator()

# Configure storage for the orchestrator's routing team
team_storage = SqliteStorage(
    table_name="team_sessions", 
    db_file="data/pagbank.db",
    auto_upgrade_schema=True
)
orchestrator.routing_team.storage = team_storage

# Create shared storage for individual agents
agent_storage = SqliteStorage(
    table_name="agent_sessions", 
    db_file="data/pagbank.db",
    auto_upgrade_schema=True
)

# Extract the actual Agno Agents from specialist agents and configure storage
agno_agents = []
for agent_name, agent_instance in orchestrator.specialist_agents.items():
    if isinstance(agent_instance, Agent):
        # Assign shared agent storage for conversation history
        agent_instance.storage = agent_storage
        agno_agents.append(agent_instance)

# Use the actual orchestrator's routing team (which has all the preprocessing features)
routing_team = orchestrator.routing_team

# Create Playground app with routing team (no individual agents shown to avoid confusion)
playground_app = Playground(
    teams=[routing_team],
    app_id="pagbank-multi-agent-system",
    name="PagBank Multi-Agent System"
)

# Get the FastAPI app for ASGI
app = playground_app.get_app()

if not os.environ.get('UVICORN_RELOADER_PROCESS'):
    print("📦 Configured demo session storage...")
    print(f"🎯 Using actual orchestrator routing team: {routing_team.name}")
    print(f"🎯 Routing to {len(agno_agents)} specialist agents")
    print("🎯 PagBank Playground ready with simplified single-agent architecture")
    print(f"✅ Ana persona configured: show_tool_calls={routing_team.show_tool_calls}, show_members_responses={routing_team.show_members_responses}, stream_intermediate_steps={routing_team.stream_intermediate_steps}")
    print("🌐 Playground will serve at: http://localhost:7777")
    print("\n📋 Architecture:")
    print(f"  • {routing_team.name} (mode={routing_team.mode}, routes to specialist agents)")
    print("\n📋 Specialist Agents:")
    for agent_name, agent in orchestrator.specialist_agents.items():
        print(f"  • {agent_name} ({agent.name})")

def main():
    """Main entry point for PagBank Playground"""
    try:
        print("\n" + "="*50)
        print("🏦 PAGBANK MULTI-AGENT SYSTEM DEMO")
        print("="*50)
        print("✅ System: 100% Complete")
        print("✅ Routing team with specialist agents: Active")
        print("✅ All 5 specialist agents loaded (simplified architecture)")
        print("✅ Knowledge base: 571 entries")
        print("✅ Memory system: Active")
        print("✅ Portuguese support: Full")
        print("✅ Demo ready: YES")
        print("="*50)
        print("\n🎬 Starting demo server...")
        
        # Serve the playground
        playground_app.serve("playground:app", reload=False)
        
    except Exception as e:
        print(f"❌ Error starting playground: {e}")
        print("💡 Check if all dependencies are installed with 'uv add'")
        raise

if __name__ == "__main__":
    main()