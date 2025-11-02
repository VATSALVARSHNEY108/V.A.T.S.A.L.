"""
Test Letter Generator
Demonstrates the new letter writing functionality with various letter types
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'ai_features'))

from letter_templates import generate_letter, list_letter_types, show_letter_preview
from code_generator import generate_code


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_letter_generation():
    """Test various letter generation scenarios"""

    print("🎯 LETTER GENERATOR TEST SUITE")
    print_separator()

    # Test 1: Leave letter to principal
    print("TEST 1: Leave Letter to Principal for 2 Days")
    print("-" * 80)
    result1 = generate_code("write a letter to principal for 2 days leave")
    if result1["success"]:
        print("✅ Letter Generated Successfully!")
        print(f"📝 Letter Type: {result1.get('letter_name', 'N/A')}")
        print("\nLetter Content:")
        print(result1["code"])
    else:
        print(f"❌ Error: {result1.get('error')}")

    print_separator()

    # Test 2: Leave letter for sick leave
    print("TEST 2: Sick Leave Letter")
    print("-" * 80)
    result2 = generate_letter("write a letter to manager for 3 days sick leave")
    if result2["success"]:
        print("✅ Letter Generated Successfully!")
        print(f"📝 Letter Type: {result2['letter_name']}")
        print("\nLetter Content:")
        print(result2["letter"])
    else:
        print(f"❌ Error: {result2.get('error')}")

    print_separator()

    # Test 3: Complaint letter
    print("TEST 3: Complaint Letter")
    print("-" * 80)
    result3 = generate_letter("write a complaint letter")
    if result3["success"]:
        print("✅ Letter Generated Successfully!")
        print(f"📝 Letter Type: {result3['letter_name']}")
        print("\nLetter Content:")
        print(result3["letter"])
    else:
        print(f"❌ Error: {result3.get('error')}")

    print_separator()

    # Test 4: Thank you letter
    print("TEST 4: Thank You Letter")
    print("-" * 80)
    result4 = generate_letter("write a thank you letter")
    if result4["success"]:
        print("✅ Letter Generated Successfully!")
        print(f"📝 Letter Type: {result4['letter_name']}")
        print("\nLetter Content:")
        print(result4["letter"])
    else:
        print(f"❌ Error: {result4.get('error')}")

    print_separator()

    # Test 5: Custom values
    print("TEST 5: Leave Letter with Custom Values")
    print("-" * 80)
    custom_values = {
        "sender_name": "Vatsal Varshney",
        "recipient_name": "Mr. Sharma",
        "recipient_title": "Principal",
        "organization": "ABC School",
        "leave_days": "3",
        "leave_reason": "family wedding",
        "start_date": "November 5, 2025",
        "end_date": "November 7, 2025"
    }
    result5 = generate_letter("write a leave letter", custom_values=custom_values)
    if result5["success"]:
        print("✅ Letter Generated Successfully with Custom Values!")
        print(f"📝 Letter Type: {result5['letter_name']}")
        print("\nLetter Content:")
        print(result5["letter"])
    else:
        print(f"❌ Error: {result5.get('error')}")

    print_separator()

    # Show available letter types
    print("📋 AVAILABLE LETTER TYPES:")
    print("-" * 80)
    letter_types = list_letter_types()
    for letter_type, name in letter_types.items():
        print(f"  • {letter_type}: {name}")

    print_separator()

    # Test integration with code generator
    print("TEST 6: Integration with Code Generator")
    print("-" * 80)
    test_commands = [
        "write a resignation letter",
        "write an invitation letter",
        "write a job application letter",
        "write a permission letter"
    ]

    for command in test_commands:
        print(f"\nCommand: '{command}'")
        result = generate_code(command)
        if result["success"]:
            print(f"✅ Detected as: {result.get('letter_name', 'Code generation')}")
            print(f"   Source: {result.get('source', 'N/A')}")
        else:
            print(f"❌ Failed: {result.get('error')}")

    print_separator()

    print("✅ ALL TESTS COMPLETED!")
    print("\n💡 USAGE EXAMPLES:")
    print("   • 'write a letter to principal for 2 days holiday'")
    print("   • 'write a complaint letter'")
    print("   • 'write a thank you letter'")
    print("   • 'write a resignation letter'")
    print("   • 'write a job application letter'")
    print("   • 'write an appreciation letter'")
    print("   • 'write an apology letter'")
    print("   • 'write an invitation letter'")
    print("\n📝 All letters can be customized by passing a custom_values dictionary!")


if __name__ == "__main__":
    test_letter_generation()
