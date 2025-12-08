
import json
import os
from pathlib import Path
from src.orchestrator.workflow import WorkflowOrchestrator

# Raw product data (ONLY input to the system)
RAW_PRODUCT_DATA = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": "Vitamin C, Hyaluronic Acid",
    "benefits": "Brightening, Fades dark spots",
    "how_to_use": "Apply 2-3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}

def save_json_output(data: dict, filename: str, output_dir: str = "output"):
    """Save JSON output to file"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save JSON with pretty formatting
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved: {filepath}")

def main():
    """
    Main entry point for the multi-agent content generation system
    """
    print("\n" + "="*70)
    print("KASPARRO AI - Multi-Agent Content Generation System")
    print("="*70 + "\n")
    
    # Initialize orchestrator
    orchestrator = WorkflowOrchestrator()
    
    # Execute pipeline
    try:
        outputs = orchestrator.execute_pipeline(RAW_PRODUCT_DATA)
        
        # Save outputs
        print("\n[OUTPUT] Saving generated pages...\n")
        save_json_output(outputs["faq"], "faq.json")
        save_json_output(outputs["product_page"], "product_page.json")
        save_json_output(outputs["comparison"], "comparison_page.json")
        
        # Print summary
        print("\n" + "="*70)
        print("PIPELINE SUMMARY")
        print("="*70)
        status = orchestrator.get_pipeline_status()
        print(f"Final State: {status['current_state']}")
        print(f"Product Parsed: {status['product_parsed']}")
        print(f"Questions Generated: {status['questions_generated']}")
        print(f"Comparison Generated: {status['comparison_generated']}")
        print(f"\nOutputs Generated:")
        for page_type, ready in status['outputs_ready'].items():
            print(f"  - {page_type}.json: {'✓' if ready else '✗'}")
        print("="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())