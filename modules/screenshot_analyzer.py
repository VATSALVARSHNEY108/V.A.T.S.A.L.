"""
Screenshot Analyzer Module
Re-exports screenshot analysis functions for backward compatibility
Uses lazy imports to avoid circular dependencies

UPDATED: Now uses the new dedicated screenshot_analysis module
"""

__all__ = [
    'analyze_screenshot',
    'suggest_improvements',
    'analyze_screen_for_errors',
    'get_quick_tips',
    'analyze_code_on_screen',
    'analyze_website_design',
    'extract_text_from_screenshot',
    'find_element_in_screenshot',
    'get_screenshot_summary',
    'compare_screenshots'
]

def analyze_screenshot(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import analyze_screenshot as _func
    return _func(*args, **kwargs)

def suggest_improvements(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import suggest_improvements as _func
    return _func(*args, **kwargs)

def analyze_screen_for_errors(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import analyze_screen_for_errors as _func
    return _func(*args, **kwargs)

def get_quick_tips(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import get_quick_tips as _func
    return _func(*args, **kwargs)

def analyze_code_on_screen(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import analyze_code_on_screen as _func
    return _func(*args, **kwargs)

def analyze_website_design(*args, **kwargs):
    from modules.ai_features.screenshot_analysis import analyze_website_design as _func
    return _func(*args, **kwargs)

def extract_text_from_screenshot(*args, **kwargs):
    from modules.ai_features.vision_ai import extract_text_from_screenshot as _func
    return _func(*args, **kwargs)

def find_element_in_screenshot(*args, **kwargs):
    from modules.ai_features.vision_ai import find_element_in_screenshot as _func
    return _func(*args, **kwargs)

def get_screenshot_summary(*args, **kwargs):
    from modules.ai_features.vision_ai import get_screenshot_summary as _func
    return _func(*args, **kwargs)

def compare_screenshots(*args, **kwargs):
    from modules.ai_features.vision_ai import compare_screenshots as _func
    return _func(*args, **kwargs)
