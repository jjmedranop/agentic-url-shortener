from agent_orchestrator.graph import app_orchestrator
import sys

def run_pipeline(requirement_text: str):
    print(f"\n🚀 Initializing Agentic Pipeline for requirement: '{requirement_text}'\n")
    
    initial_state = {
        "requirement": requirement_text,
        "ambiguities": [],
        "is_ambiguous": False,
        "generated_code": "",
        "test_results": "",
        "retry_count": 0,
        "human_approved": False
    }
    
    # Execute the graph
    for event in app_orchestrator.stream(initial_state):
        for node, state in event.items():
            print(f"--- Finished Node: {node} ---")
            if state.get("is_ambiguous"):
                print(f"⚠️ Ambiguity Alert: {state['ambiguities']}")
                print("🛑 Halting execution. Please re-run with clearer inputs.")
                return
            if state.get("test_results"):
                print(f"🧪 Test Log Status: {state['test_results']}")
                
    # Human Approval Gate Interruption simulation
    print("\n✋ ENTRY GATE: Human Verification Checkpoint Required.")
    user_input = input("Review code in 'url_shortener_app/main.py'. Approve release? (yes/no): ")
    if user_input.strip().lower() == "yes":
        print("✅ Release authorized successfully. Pipeline complete.")
    else:
        print("❌ Action rejected by human supervisor. Aborting change rollout.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_evaluation.py [greenfield|brownfield|ambiguous]")
        sys.exit(1)
        
    scenario = sys.argv[1].lower()
    
    if scenario == "greenfield":
        # Scenario 1: Pure new feature build tracking link metric data
        run_pipeline("Add a hit counter analytics endpoint tracking GET requests matching a short URL string code.")
        
    elif scenario == "brownfield":
        # Scenario 2: Patching/Refactoring existing application state
        run_pipeline("Modify the random URL code generation function to check if the generated string code already exists in our database store.")
        
    elif scenario == "ambiguous":
        # Scenario 3: Missing metrics or validation context
        run_pipeline("Make the link redirection feature look better and faster somehow.")
