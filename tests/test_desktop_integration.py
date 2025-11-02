#!/usr/bin/env python3
"""
Test script to verify Desktop File Controller integration with GUI
"""

import sys

def test_imports():
    """Test that all imports work"""
    print("🧪 Testing imports...")
    try:
        from desktop_controller_integration import DesktopFileController
        print("  ✅ desktop_controller_integration imported")
        
        # Test initialization
        controller = DesktopFileController()
        print(f"  ✅ Controller initialized: {controller.desktop_path}")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_gui_integration():
    """Test GUI integration without running GUI"""
    print("\n🧪 Testing GUI integration...")
    try:
        # Import GUI file
        import gui_app
        print("  ✅ gui_app.py imports successfully")
        
        # Check if class has desktop_controller
        if hasattr(gui_app.AutomationControllerGUI, 'launch_batch_controller'):
            print("  ✅ launch_batch_controller method exists")
        else:
            print("  ❌ launch_batch_controller method not found")
            return False
            
        if hasattr(gui_app.AutomationControllerGUI, 'list_desktop_items'):
            print("  ✅ list_desktop_items method exists")
        else:
            print("  ❌ list_desktop_items method not found")
            return False
            
        if hasattr(gui_app.AutomationControllerGUI, 'create_desktop_folder'):
            print("  ✅ create_desktop_folder method exists")
        else:
            print("  ❌ create_desktop_folder method not found")
            return False
            
        if hasattr(gui_app.AutomationControllerGUI, 'organize_desktop'):
            print("  ✅ organize_desktop method exists")
        else:
            print("  ❌ organize_desktop method not found")
            return False
            
        if hasattr(gui_app.AutomationControllerGUI, 'search_desktop_files'):
            print("  ✅ search_desktop_files method exists")
        else:
            print("  ❌ search_desktop_files method not found")
            return False
        
        print("  ✅ All 5 desktop controller methods found in GUI")
        return True
        
    except Exception as e:
        print(f"  ❌ GUI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_controller_functions():
    """Test controller functions"""
    print("\n🧪 Testing controller functions...")
    try:
        from desktop_controller_integration import DesktopFileController
        controller = DesktopFileController()
        
        # Test list_items
        result = controller.list_items()
        if result.get("success"):
            print(f"  ✅ list_items() works - found {result.get('count', 0)} items")
        else:
            print(f"  ⚠️  list_items() returned: {result.get('message')}")
        
        # Test launch_batch_controller (won't actually launch, just check it runs)
        result = controller.launch_batch_controller()
        print(f"  ✅ launch_batch_controller() callable - {result.get('message', 'OK')}")
        
        return True
    except Exception as e:
        print(f"  ❌ Controller functions test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Desktop File Controller Integration Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("GUI Integration", test_gui_integration()))
    results.append(("Controller Functions", test_controller_functions()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Integration is complete.")
    else:
        print("⚠️  Some tests failed. Check errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
