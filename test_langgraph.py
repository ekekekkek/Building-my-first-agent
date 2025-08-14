#!/usr/bin/env python3
"""
Test script for LangGraph workflow
Run this to test the multi-model system before starting the backend
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_langgraph_workflow():
    """Test the LangGraph workflow with sample queries"""
    
    try:
        from langgraph.workflows.main_workflow import run_workflow_async
        from langchain_core.messages import HumanMessage
        
        print("🚀 Testing LangGraph Workflow...")
        print("=" * 50)
        
        # Test queries
        test_queries = [
            "What are the best investment strategies for 2024?",
            "How do I implement a binary search tree in Python?",
            "Tell me a joke about programming",
            "What's the weather like today?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query}")
            print("-" * 40)
            
            # Initialize state
            initial_state = {
                "user_message": query,
                "messages": [HumanMessage(content=query)]
            }
            
            # Run workflow
            try:
                result = await run_workflow_async(initial_state)
                
                if "final_response" in result:
                    print("✅ Workflow completed successfully!")
                    print(f"📤 Response: {result['final_response'][:200]}...")
                    
                    # Show routing info if available
                    if "route_to" in result:
                        print(f"🔄 Routed to: {result['route_to']}")
                    if "routing_reason" in result:
                        print(f"💭 Routing reason: {result['routing_reason']}")
                else:
                    print("❌ No final response generated")
                    print(f"Result keys: {list(result.keys())}")
                    
            except Exception as e:
                print(f"❌ Workflow error: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 50)
        print("🎉 LangGraph workflow test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed all dependencies:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_langgraph_workflow()) 