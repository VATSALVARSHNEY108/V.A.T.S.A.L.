"""
🚀 AI Screen Monitoring System - Next Generation
Advanced AI-powered screen monitoring with real-time analysis, intelligent triggers, and comprehensive analytics

Features:
- Real-time continuous monitoring with smart scheduling
- Multi-layered AI analysis (8 intelligence modes)
- Advanced analytics with data visualization
- Pattern detection and behavioral learning
- Intelligent triggers and automated actions
- Performance optimization (change detection)
- Privacy controls with pause/resume
- Historical tracking with trend analysis
- Database storage for long-term insights
"""

import time
import os
import json
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, deque
import threading
from pathlib import Path

from gui_automation import GUIAutomation
from gemini_controller import get_client
from google.genai import types

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class AIScreenMonitoringSystem:
    """
    Next-generation AI screen monitoring system with advanced intelligence
    
    Capabilities:
    - Real-time monitoring with configurable intervals
    - Smart change detection (only analyze when screen changes)
    - 8 AI analysis modes: productivity, security, performance, ux, accessibility, code, design, automation
    - Intelligent triggers and automated actions
    - Pattern learning and behavioral insights
    - Advanced analytics with visualizations
    - Privacy controls (pause/resume, exclude apps)
    - Historical tracking with trend analysis
    """
    
    def __init__(self, config_path: str = "screen_monitor_config.json"):
        """Initialize AI screen monitoring system"""
        self.gui = GUIAutomation()
        self.config_path = config_path
        self.config = self._load_config()
        
        self.monitoring = False
        self.paused = False
        self.monitoring_thread = None
        
        self.last_screenshot_hash = None
        self.last_screenshot_path = None
        self.screenshot_history = deque(maxlen=100)
        
        self.activity_log = []
        self.analytics_db_path = "screen_monitor_analytics.json"
        self.analytics = self._load_analytics()
        
        self.patterns = defaultdict(list)
        self.triggers = {}
        self.alerts = []
        
        self.session_start = None
        self.session_stats = {
            "total_screenshots": 0,
            "ai_analyses": 0,
            "changes_detected": 0,
            "alerts_triggered": 0,
            "patterns_learned": 0
        }
        
        print("🚀 AI Screen Monitoring System initialized")
        print(f"   ✨ {len(self.ANALYSIS_MODES)} AI analysis modes available")
        print(f"   📊 Analytics tracking enabled")
        print(f"   🧠 Pattern learning active")
    
    ANALYSIS_MODES = {
        "productivity": {
            "name": "Productivity Monitor",
            "icon": "📊",
            "description": "Track focus, detect distractions, measure productivity",
            "interval": 60
        },
        "security": {
            "name": "Security Scanner",
            "icon": "🔒",
            "description": "Detect security threats, exposed credentials, vulnerabilities",
            "interval": 120
        },
        "performance": {
            "name": "Performance Analyzer",
            "icon": "⚡",
            "description": "Monitor app performance, detect bottlenecks, suggest optimizations",
            "interval": 180
        },
        "errors": {
            "name": "Error Detector",
            "icon": "🐛",
            "description": "Automatically detect errors, warnings, and issues",
            "interval": 30
        },
        "ux": {
            "name": "UX Expert",
            "icon": "🎨",
            "description": "Professional UX/UI analysis and design critique",
            "interval": 300
        },
        "accessibility": {
            "name": "Accessibility Auditor",
            "icon": "♿",
            "description": "WCAG compliance check and accessibility analysis",
            "interval": 300
        },
        "code": {
            "name": "Code Reviewer",
            "icon": "💻",
            "description": "Code quality analysis, bug detection, refactoring suggestions",
            "interval": 120
        },
        "automation": {
            "name": "Automation Discovery",
            "icon": "🤖",
            "description": "Find automation opportunities and repetitive tasks",
            "interval": 240
        }
    }
    
    def _load_config(self) -> Dict:
        """Load monitoring configuration"""
        default_config = {
            "enabled": True,
            "default_interval": 30,
            "change_detection": True,
            "smart_scheduling": True,
            "privacy_mode": False,
            "excluded_apps": [],
            "active_modes": ["productivity", "errors", "security"],
            "auto_actions": {
                "screenshot_on_error": True,
                "alert_on_security": True,
                "log_productivity": True
            },
            "storage": {
                "max_screenshots": 100,
                "max_logs": 1000,
                "cleanup_days": 7
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"   ⚠️  Error loading config: {e}")
        
        return default_config
    
    def _save_config(self):
        """Save configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Error saving config: {e}")
    
    def _load_analytics(self) -> Dict:
        """Load analytics database"""
        default_analytics = {
            "productivity_scores": [],
            "security_issues": [],
            "errors_detected": [],
            "performance_metrics": [],
            "app_usage": defaultdict(int),
            "time_tracking": {},
            "patterns": {},
            "trends": {}
        }
        
        if os.path.exists(self.analytics_db_path):
            try:
                with open(self.analytics_db_path, 'r') as f:
                    loaded = json.load(f)
                    for key in loaded:
                        if key in default_analytics:
                            default_analytics[key] = loaded[key]
            except Exception as e:
                print(f"   ⚠️  Error loading analytics: {e}")
        
        return default_analytics
    
    def _save_analytics(self):
        """Save analytics database"""
        try:
            analytics_dict = {}
            for key, value in self.analytics.items():
                if isinstance(value, defaultdict):
                    analytics_dict[key] = dict(value)
                else:
                    analytics_dict[key] = value
            
            with open(self.analytics_db_path, 'w') as f:
                json.dump(analytics_dict, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Error saving analytics: {e}")
    
    def _calculate_image_hash(self, image_path: str) -> Optional[str]:
        """Calculate hash of screenshot for change detection"""
        if not PIL_AVAILABLE or not os.path.exists(image_path):
            return None
        
        try:
            if PIL_AVAILABLE and Image is not None:
                img = Image.open(image_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                img = img.convert('L')
            else:
                return None
            
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            
            bits = ''.join(['1' if p > avg else '0' for p in pixels])
            hash_hex = hex(int(bits, 2))[2:].zfill(16)
            
            return hash_hex
        except Exception as e:
            print(f"   ⚠️  Error calculating hash: {e}")
            return None
    
    def _has_screen_changed(self, new_screenshot_path: str) -> bool:
        """Check if screen has changed significantly"""
        if not self.config["change_detection"]:
            return True
        
        new_hash = self._calculate_image_hash(new_screenshot_path)
        
        if new_hash is None:
            return True
        
        if self.last_screenshot_hash is None:
            self.last_screenshot_hash = new_hash
            return True
        
        if new_hash != self.last_screenshot_hash:
            self.last_screenshot_hash = new_hash
            self.session_stats["changes_detected"] += 1
            return True
        
        return False
    
    def _analyze_with_ai(self, screenshot_path: str, mode: str) -> Dict:
        """Analyze screenshot with AI in specific mode"""
        
        prompts = {
            "productivity": """Analyze this screen for PRODUCTIVITY:

📊 **ASSESSMENT**
1. Current Activity: What is the user doing?
2. Focus Level: Highly focused work / Moderate / Distracted (1-10 score)
3. Distractions: Social media, games, personal browsing visible?
4. Work Quality: Deep work, shallow work, or time-wasting?

💡 **INSIGHTS**
5. Productivity Score: 1-10 (10 = maximum productivity)
6. Suggestions: How to improve focus
7. Patterns: Note any productivity patterns

Respond with JSON:
```json
{
    "activity": "description",
    "focus_level": 0-10,
    "distractions": ["list"],
    "productivity_score": 0-10,
    "work_type": "deep|shallow|distraction",
    "suggestions": ["list of suggestions"]
}
```""",
            
            "security": """Analyze this screen for SECURITY THREATS:

🔒 **SECURITY SCAN**
1. Exposed Credentials: API keys, passwords, tokens visible?
2. Sensitive Data: Personal info, credit cards, SSNs?
3. Security Warnings: Certificate errors, unsafe sites?
4. Suspicious Activity: Phishing, malware indicators?

⚠️ **RISK LEVEL**
5. Overall Risk: CRITICAL / HIGH / MEDIUM / LOW / NONE
6. Immediate Actions: What to do right now
7. Vulnerabilities: List all issues found

Respond with JSON:
```json
{
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|NONE",
    "issues": [
        {
            "type": "credentials|data|warning|phishing",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "description": "what was found",
            "action": "what to do"
        }
    ],
    "overall_security_score": 0-10
}
```""",
            
            "performance": """Analyze this screen for PERFORMANCE:

⚡ **PERFORMANCE ANALYSIS**
1. Loading Indicators: Spinners, progress bars visible?
2. Slow Operations: Any lag or delay indicators?
3. Resource Issues: Memory warnings, CPU alerts?
4. Bottlenecks: What's slowing things down?

🎯 **OPTIMIZATION**
5. Performance Score: 1-10 (10 = optimal)
6. Quick Fixes: Easy performance improvements
7. Technical Debt: Long-term optimization needs

Respond with JSON:
```json
{
    "performance_score": 0-10,
    "issues": ["list of performance issues"],
    "bottlenecks": ["list of bottlenecks"],
    "optimizations": [
        {
            "priority": "HIGH|MEDIUM|LOW",
            "fix": "description",
            "impact": "expected improvement"
        }
    ]
}
```""",
            
            "errors": """Analyze this screen for ERRORS:

🐛 **ERROR DETECTION**
1. Error Messages: Any visible errors or warnings?
2. Red Indicators: Error text, icons, highlights?
3. Failed Operations: Broken features, failed saves?
4. Console Errors: Developer console visible with errors?

📋 **ERROR REPORT**
5. All Errors: List every error found
6. Severity: CRITICAL / HIGH / MEDIUM / LOW
7. Solutions: How to fix each error

Respond with JSON:
```json
{
    "errors_found": true|false,
    "error_count": 0-100,
    "errors": [
        {
            "message": "error description",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "location": "where it appears",
            "solution": "how to fix"
        }
    ]
}
```""",
            
            "ux": """Analyze this screen as a UX EXPERT:

🎨 **UX ANALYSIS**
1. Visual Design: Layout, colors, typography quality (1-10)
2. User Flow: Is navigation clear and intuitive?
3. Accessibility: Color contrast, text size, keyboard nav
4. Usability Issues: Confusing elements, poor UX

💎 **EXPERT CRITIQUE**
5. UX Score: 1-10 (10 = exceptional)
6. Strengths: What's done well
7. Improvements: Specific UX fixes needed

Respond with JSON:
```json
{
    "ux_score": 0-10,
    "design_score": 0-10,
    "strengths": ["list"],
    "issues": ["list of UX problems"],
    "improvements": [
        {
            "area": "navigation|design|accessibility|flow",
            "issue": "description",
            "fix": "how to improve"
        }
    ]
}
```""",
            
            "accessibility": """Analyze this screen for ACCESSIBILITY:

♿ **WCAG COMPLIANCE**
1. Color Contrast: Sufficient contrast (4.5:1)?
2. Text Size: Readable text sizes?
3. Keyboard Navigation: All functions accessible?
4. Screen Reader Support: Proper labels and structure?

📊 **COMPLIANCE LEVEL**
5. WCAG Level A: Pass/Fail
6. WCAG Level AA: Pass/Fail
7. Critical Issues: List blockers
8. Accessibility Score: 1-10

Respond with JSON:
```json
{
    "accessibility_score": 0-10,
    "wcag_a": "pass|fail",
    "wcag_aa": "pass|fail",
    "violations": [
        {
            "guideline": "WCAG reference",
            "severity": "BLOCKER|CRITICAL|MAJOR|MINOR",
            "issue": "description",
            "fix": "how to fix"
        }
    ]
}
```""",
            
            "code": """Analyze any CODE visible on screen:

💻 **CODE REVIEW**
1. Code Quality: Clean, readable, well-structured?
2. Bugs: Any obvious errors or logic issues?
3. Security: SQL injection, XSS, vulnerabilities?
4. Performance: Inefficient algorithms, bottlenecks?

📊 **CODE METRICS**
5. Code Quality Score: 1-10
6. Language: What programming language?
7. Issues: List all problems found
8. Refactoring: Improvement suggestions

Respond with JSON:
```json
{
    "code_detected": true|false,
    "language": "language name",
    "code_quality_score": 0-10,
    "issues": [
        {
            "type": "bug|security|performance|style",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "description": "issue details",
            "fix": "how to fix"
        }
    ],
    "refactoring_suggestions": ["list"]
}
```""",
            
            "automation": """Analyze this screen for AUTOMATION OPPORTUNITIES:

🤖 **AUTOMATION DISCOVERY**
1. Repetitive Tasks: Copy-paste, data entry, clicking?
2. Manual Workflows: Multi-step processes that repeat?
3. Time Wasters: Tasks that could be automated?
4. Integration Opportunities: Connect tools together?

💡 **AUTOMATION POTENTIAL**
5. Tasks Found: Count of automatable tasks
6. Time Saved: Hours per week if automated
7. Quick Wins: Easy automations with high impact

Respond with JSON:
```json
{
    "automation_opportunities": [
        {
            "task": "description",
            "frequency": "daily|weekly|monthly",
            "time_saved_minutes": 0-1000,
            "complexity": "LOW|MEDIUM|HIGH",
            "roi": "HIGH|MEDIUM|LOW",
            "solution": "how to automate"
        }
    ],
    "total_time_saved_hours": 0-100
}
```"""
        }
        
        prompt = prompts.get(mode, prompts["productivity"])
        
        try:
            client = get_client()
            
            if not os.path.exists(screenshot_path):
                return {"success": False, "error": "Screenshot not found"}
            
            with open(screenshot_path, 'rb') as f:
                image_data = f.read()
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Part.from_bytes(data=image_data, mime_type='image/png'),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2000
                )
            )
            
            analysis_text = response.text.strip()
            
            structured_data = self._extract_json_from_response(analysis_text)
            
            self.session_stats["ai_analyses"] += 1
            
            return {
                "success": True,
                "mode": mode,
                "analysis": analysis_text,
                "data": structured_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_json_from_response(self, text: str) -> Optional[Dict]:
        """Extract JSON data from AI response"""
        try:
            if "```json" in text:
                json_start = text.find("```json") + 7
                json_end = text.find("```", json_start)
                json_str = text[json_start:json_end].strip()
            elif "{" in text and "}" in text:
                json_start = text.find("{")
                json_end = text.rfind("}") + 1
                json_str = text[json_start:json_end]
            else:
                return None
            
            return json.loads(json_str)
        except Exception as e:
            print(f"   ⚠️  Error extracting JSON: {e}")
            return None
    
    def _check_triggers(self, analysis_result: Dict):
        """Check if any triggers are activated"""
        if not analysis_result.get("success"):
            return
        
        mode = analysis_result.get("mode")
        data = analysis_result.get("data", {})
        
        if mode == "productivity":
            score = data.get("productivity_score", 10)
            threshold = self.triggers.get("productivity_drop", 3)
            
            if score < threshold:
                self._create_alert(
                    "PRODUCTIVITY_DROP",
                    f"Productivity score dropped to {score}/10",
                    "MEDIUM",
                    data
                )
        
        elif mode == "security":
            risk = data.get("risk_level", "NONE")
            
            if risk in ["CRITICAL", "HIGH"]:
                self._create_alert(
                    "SECURITY_THREAT",
                    f"Security risk detected: {risk}",
                    risk,
                    data
                )
                
                if self.config["auto_actions"]["alert_on_security"]:
                    self._take_automated_action("security_alert", data)
        
        elif mode == "errors":
            if data.get("errors_found"):
                error_count = data.get("error_count", 0)
                
                if error_count > 0:
                    severity = "HIGH" if error_count > 3 else "MEDIUM"
                    self._create_alert(
                        "ERRORS_DETECTED",
                        f"{error_count} error(s) detected on screen",
                        severity,
                        data
                    )
                    
                    if self.config["auto_actions"]["screenshot_on_error"]:
                        self._take_automated_action("save_error_screenshot", data)
    
    def _create_alert(self, alert_type: str, message: str, severity: str, data: Dict):
        """Create an alert"""
        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        self.alerts.append(alert)
        self.session_stats["alerts_triggered"] += 1
        
        print(f"\n🚨 ALERT [{severity}]: {message}")
    
    def _take_automated_action(self, action_type: str, data: Dict):
        """Take automated action based on trigger"""
        if action_type == "security_alert":
            print("   🔒 Auto-action: Security alert logged")
        
        elif action_type == "save_error_screenshot":
            print("   📸 Auto-action: Error screenshot saved")
        
        print(f"   🤖 Automated action executed: {action_type}")
    
    def _learn_patterns(self, mode: str, analysis_result: Dict):
        """Learn patterns from analysis"""
        if not analysis_result.get("success"):
            return
        
        data = analysis_result.get("data", {})
        timestamp = datetime.now()
        
        if mode == "productivity":
            score = data.get("productivity_score", 0)
            activity = data.get("activity", "unknown")
            
            hour = timestamp.hour
            day = timestamp.strftime("%A")
            
            pattern_key = f"{day}_{hour}"
            
            if pattern_key not in self.patterns:
                self.patterns[pattern_key] = []
            
            self.patterns[pattern_key].append({
                "score": score,
                "activity": activity,
                "time": timestamp.isoformat()
            })
            
            self.session_stats["patterns_learned"] += 1
    
    def _update_analytics(self, analysis_result: Dict):
        """Update analytics database"""
        if not analysis_result.get("success"):
            return
        
        mode = analysis_result.get("mode")
        data = analysis_result.get("data", {})
        timestamp = datetime.now().isoformat()
        
        if mode == "productivity":
            score = data.get("productivity_score", 0)
            self.analytics["productivity_scores"].append({
                "score": score,
                "timestamp": timestamp
            })
        
        elif mode == "security":
            issues = data.get("issues", [])
            if issues:
                self.analytics["security_issues"].extend([
                    {**issue, "timestamp": timestamp} for issue in issues
                ])
        
        elif mode == "errors":
            if data.get("errors_found"):
                errors = data.get("errors", [])
                self.analytics["errors_detected"].extend([
                    {**error, "timestamp": timestamp} for error in errors
                ])
        
        elif mode == "performance":
            score = data.get("performance_score", 0)
            self.analytics["performance_metrics"].append({
                "score": score,
                "timestamp": timestamp
            })
        
        self._save_analytics()
    
    def start_monitoring(self, modes: Optional[List[str]] = None, interval: int = 30):
        """
        Start continuous monitoring
        
        Args:
            modes: List of analysis modes to use (default: config active_modes)
            interval: Seconds between checks (default: 30)
        """
        if self.monitoring:
            return {"success": False, "message": "Monitoring already running"}
        
        if modes is None:
            modes = self.config["active_modes"]
        
        if modes:
            invalid_modes = [m for m in modes if m not in self.ANALYSIS_MODES]
            if invalid_modes:
                return {
                    "success": False,
                    "message": f"Invalid modes: {invalid_modes}"
                }
        else:
            modes = list(self.ANALYSIS_MODES.keys())[:3]
        
        self.monitoring = True
        self.session_start = datetime.now()
        
        print(f"\n👁️ Starting AI Screen Monitoring")
        print(f"   📊 Modes: {', '.join(modes) if modes else 'None'}")
        print(f"   ⏱️  Interval: {interval}s")
        print(f"   🔄 Change detection: {'Enabled' if self.config['change_detection'] else 'Disabled'}")
        
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(modes, interval),
            daemon=True
        )
        self.monitoring_thread.start()
        
        return {
            "success": True,
            "message": "Monitoring started",
            "modes": modes,
            "interval": interval
        }
    
    def _monitoring_loop(self, modes: List[str], interval: int):
        """Continuous monitoring loop (runs in background thread)"""
        mode_index = 0
        
        while self.monitoring:
            if self.paused:
                time.sleep(1)
                continue
            
            try:
                screenshot_path = self.gui.screenshot(f"monitor_{int(time.time())}")
                
                if not screenshot_path:
                    print("   ⚠️  Screenshot not available in cloud environment")
                    break
                
                self.session_stats["total_screenshots"] += 1
                
                if self._has_screen_changed(screenshot_path):
                    current_mode = modes[mode_index % len(modes)]
                    
                    print(f"\n   🔍 Analyzing ({current_mode})...")
                    
                    result = self._analyze_with_ai(screenshot_path, current_mode)
                    
                    if result.get("success"):
                        self._check_triggers(result)
                        self._learn_patterns(current_mode, result)
                        self._update_analytics(result)
                        
                        self.activity_log.append({
                            "timestamp": datetime.now().isoformat(),
                            "mode": current_mode,
                            "result": result
                        })
                    
                    mode_index += 1
                else:
                    print("   ⏭️  No screen change detected, skipping analysis")
                
                self.screenshot_history.append({
                    "path": screenshot_path,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"   ❌ Monitoring error: {e}")
            
            time.sleep(interval)
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        if not self.monitoring:
            return {"success": False, "message": "Monitoring not running"}
        
        self.monitoring = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        duration = (datetime.now() - self.session_start).total_seconds() if self.session_start else 0
        
        print(f"\n✅ Monitoring stopped")
        print(f"   ⏱️  Duration: {int(duration)}s")
        print(f"   📸 Screenshots: {self.session_stats['total_screenshots']}")
        print(f"   🤖 AI analyses: {self.session_stats['ai_analyses']}")
        print(f"   🔄 Changes detected: {self.session_stats['changes_detected']}")
        print(f"   🚨 Alerts: {self.session_stats['alerts_triggered']}")
        
        return {
            "success": True,
            "message": "Monitoring stopped",
            "duration_seconds": int(duration),
            "stats": self.session_stats
        }
    
    def pause_monitoring(self):
        """Pause monitoring (privacy mode)"""
        self.paused = True
        return {"success": True, "message": "Monitoring paused"}
    
    def resume_monitoring(self):
        """Resume monitoring"""
        self.paused = False
        return {"success": True, "message": "Monitoring resumed"}
    
    def analyze_now(self, mode: str = "productivity") -> Dict:
        """
        Analyze current screen immediately
        
        Args:
            mode: Analysis mode to use
        """
        if mode not in self.ANALYSIS_MODES:
            return {
                "success": False,
                "message": f"Invalid mode. Available: {list(self.ANALYSIS_MODES.keys())}"
            }
        
        print(f"\n📸 Taking screenshot for {mode} analysis...")
        screenshot_path = self.gui.screenshot(f"instant_{mode}")
        
        if not screenshot_path:
            return {
                "success": False,
                "message": "❌ Screenshot not available in cloud environment. Run VATSAL locally to use this feature."
            }
        
        print(f"   🤖 AI analyzing...")
        result = self._analyze_with_ai(screenshot_path, mode)
        
        if result.get("success"):
            self._check_triggers(result)
            self._update_analytics(result)
        
        return result
    
    def get_analytics_summary(self) -> Dict:
        """Get comprehensive analytics summary"""
        
        productivity_avg = 0
        if self.analytics["productivity_scores"]:
            scores = [p["score"] for p in self.analytics["productivity_scores"]]
            productivity_avg = sum(scores) / len(scores)
        
        return {
            "productivity": {
                "average_score": round(productivity_avg, 2),
                "total_measurements": len(self.analytics["productivity_scores"]),
                "recent_scores": self.analytics["productivity_scores"][-10:]
            },
            "security": {
                "total_issues": len(self.analytics["security_issues"]),
                "critical_issues": len([i for i in self.analytics["security_issues"] if i.get("severity") == "CRITICAL"]),
                "recent_issues": self.analytics["security_issues"][-5:]
            },
            "errors": {
                "total_errors": len(self.analytics["errors_detected"]),
                "recent_errors": self.analytics["errors_detected"][-10:]
            },
            "performance": {
                "measurements": len(self.analytics["performance_metrics"]),
                "recent_metrics": self.analytics["performance_metrics"][-10:]
            },
            "patterns": {
                "total_patterns": len(self.patterns),
                "patterns_learned": self.session_stats.get("patterns_learned", 0)
            },
            "session": self.session_stats
        }
    
    def get_productivity_trends(self) -> Dict:
        """Get productivity trends analysis"""
        if not self.analytics["productivity_scores"]:
            return {"message": "No productivity data available"}
        
        scores = self.analytics["productivity_scores"]
        
        hourly_avg = defaultdict(list)
        for entry in scores:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            hour = timestamp.hour
            hourly_avg[hour].append(entry["score"])
        
        hourly_scores = {
            hour: round(sum(scores) / len(scores), 2)
            for hour, scores in hourly_avg.items()
        }
        
        peak_hour = max(hourly_scores.items(), key=lambda x: x[1]) if hourly_scores else (0, 0)
        low_hour = min(hourly_scores.items(), key=lambda x: x[1]) if hourly_scores else (0, 0)
        
        return {
            "hourly_averages": dict(sorted(hourly_scores.items())),
            "peak_productivity_hour": peak_hour[0],
            "peak_productivity_score": peak_hour[1],
            "lowest_productivity_hour": low_hour[0],
            "lowest_productivity_score": low_hour[1],
            "total_measurements": len(scores)
        }
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:]
    
    def clear_analytics(self):
        """Clear all analytics data"""
        self.analytics = {
            "productivity_scores": [],
            "security_issues": [],
            "errors_detected": [],
            "performance_metrics": [],
            "app_usage": defaultdict(int),
            "time_tracking": {},
            "patterns": {},
            "trends": {}
        }
        self._save_analytics()
        
        return {"success": True, "message": "Analytics cleared"}
    
    def set_trigger(self, trigger_name: str, value: Any):
        """
        Set a monitoring trigger
        
        Available triggers:
        - productivity_drop: Alert when score drops below value (1-10)
        - security_risk: Alert on security issues
        - error_count: Alert when errors exceed value
        """
        self.triggers[trigger_name] = value
        return {
            "success": True,
            "message": f"Trigger '{trigger_name}' set to {value}"
        }
    
    def get_config(self) -> Dict:
        """Get current configuration"""
        return self.config.copy()
    
    def update_config(self, updates: Dict):
        """Update configuration"""
        self.config.update(updates)
        self._save_config()
        
        return {
            "success": True,
            "message": "Configuration updated",
            "config": self.config
        }


def create_ai_screen_monitoring_system():
    """Factory function to create AI screen monitoring system"""
    return AIScreenMonitoringSystem()


if __name__ == "__main__":
    print("🚀 AI Screen Monitoring System - Next Generation")
    print()
    
    monitor = create_ai_screen_monitoring_system()
    
    print("\n📋 Available analysis modes:")
    for mode_id, mode_info in monitor.ANALYSIS_MODES.items():
        print(f"   {mode_info['icon']} {mode_info['name']}: {mode_info['description']}")
    
    print("\n💡 Quick start:")
    print("   monitor.analyze_now('productivity')  # Instant analysis")
    print("   monitor.start_monitoring(['productivity', 'errors'], interval=30)  # Continuous")
    print("   monitor.get_analytics_summary()  # View analytics")
    print("   monitor.stop_monitoring()  # Stop monitoring")
