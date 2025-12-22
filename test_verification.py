from qa_brain import ask_qa_streaming

print("Testing QA Brain...")
response = ask_qa_streaming("Create a test case for User Login")
if response and "Test Case" in response:
    print("\n✅ Verification SUCCESS: Model generated a test case.")
else:
    print(f"\n❌ Verification FAILED. Response length: {len(response) if response else 0}")
    print(response)
