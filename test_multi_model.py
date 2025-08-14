#!/usr/bin/env python3
"""
Test script for Simplified Multi-Model System
Run this to test the multi-model system before starting the backend
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_multi_model_system():
    """Test the multi-model system with sample queries"""
    
    try:
        from simple_multi_model import run_multi_model_query
        
        print("🚀 Testing Multi-Model System...")
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
            
            # Run multi-model processing
            try:
                result = await run_multi_model_query(query)
                
                if "final_response" in result:
                    print("✅ Multi-model processing completed successfully!")
                    print(f"🔄 Routed to: {result.get('route_to', [])}")
                    print(f"💭 Routing reason: {result.get('routing_reason', '')}")
                    print(f"📤 Final Response: {result['final_response'][:200]}...")
                    
                    # Show expert responses if available
                    if "expert_responses" in result:
                        print(f"🧠 Expert responses: {list(result['expert_responses'].keys())}")
                else:
                    print("❌ No final response generated")
                    print(f"Result keys: {list(result.keys())}")
                    
            except Exception as e:
                print(f"❌ Multi-model error: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 50)
        print("🎉 Multi-model system test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed all dependencies:")
        print("pip3 install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_multi_model_system()) 