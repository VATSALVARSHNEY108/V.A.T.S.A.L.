"""
Quick test to verify regression fixes
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'ai_features'))

from code_generator import is_letter_request


def test_regression_fixes():
    print("Testing Regression Fixes")
    print("=" * 80)

    # Test 1: Code prompts should NOT be detected as letter requests
    print("\n✅ TEST 1: Code prompts should NOT trigger letter detection")
    print("-" * 80)

    code_prompts = [
        "build a flask application",
        "create a web application with react",
        "write code for a todo application",
        "make a calculator application in python",
        "develop an application in java"
    ]

    all_passed = True
    for prompt in code_prompts:
        is_letter = is_letter_request(prompt)
        status = "❌ FAIL" if is_letter else "✅ PASS"
        if is_letter:
            all_passed = False
        print(f"{status} | '{prompt}' -> is_letter={is_letter}")

    if all_passed:
        print("\n✅ All code prompts correctly NOT detected as letters!")
    else:
        print("\n❌ Some code prompts were incorrectly detected as letters!")

    # Test 2: Letter prompts SHOULD be detected as letter requests
    print("\n✅ TEST 2: Letter prompts SHOULD trigger letter detection")
    print("-" * 80)

    letter_prompts = [
        "write a letter to principal",
        "write a leave letter",
        "write a resignation letter",
        "write a complaint letter",
        "draft a letter to manager",
        "compose a thank you letter"
    ]

    all_passed = True
    for prompt in letter_prompts:
        is_letter = is_letter_request(prompt)
        status = "✅ PASS" if is_letter else "❌ FAIL"
        if not is_letter:
            all_passed = False
        print(f"{status} | '{prompt}' -> is_letter={is_letter}")

    if all_passed:
        print("\n✅ All letter prompts correctly detected!")
    else:
        print("\n❌ Some letter prompts were NOT detected!")

    print("\n" + "=" * 80)
    print("✅ REGRESSION TESTS COMPLETE!")


if __name__ == "__main__":
    test_regression_fixes()
