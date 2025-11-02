"""
🚀 Advanced Smart Screen Monitor - Most Powerful Version
AI-powered screen monitoring with advanced intelligence, automation, and insights
"""

import time
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from gui_automation import GUIAutomation
from gemini_controller import get_client
from google.genai import types


class AdvancedSmartScreenMonitor:
    """
    Most powerful AI screen monitoring system with:
    - Advanced AI analysis and object detection
    - Real-time monitoring with intelligent triggers
    - Security scanning and vulnerability detection
    - Automated action suggestions and execution
    - Pattern recognition and learning
    - Advanced analytics and reporting
    - Multi-modal intelligence
    """
    
    def __init__(self):
        """Initialize advanced smart screen monitor"""
        self.gui = GUIAutomation()
        self.monitoring = False
        self.last_screenshot = None
        self.activity_log = []
        self.patterns = {}
        self.alerts = []
        self.analytics = {
            "productivity_scores": [],
            "errors_detected": [],
            "security_issues": [],
            "performance_metrics": []
        }
        self.learning_data = {}
        print("🚀 Advanced Smart Screen Monitor initialized")
        print("   ✨ Enhanced with multi-modal AI intelligence")
    
    def advanced_screen_analysis(self, mode: str = "comprehensive") -> Dict:
        """
        Advanced AI analysis with multiple intelligence layers
        
        Modes:
        - comprehensive: Full multi-modal analysis
        - security: Security and vulnerability scanning
        - performance: Performance and optimization analysis
        - ux_expert: Professional UX/UI analysis
        - accessibility: Accessibility compliance check
        - code_review: Deep code analysis and refactoring suggestions
        - design_critique: Professional design critique
        - automation_discovery: Find automation opportunities
        """
        print(f"\n🧠 Advanced AI Analysis Mode: {mode.upper()}")
        screenshot_path = self.gui.screenshot(f"advanced_{mode}")
        
        if not screenshot_path:
            return self._cloud_unavailable_message()
        
        self.last_screenshot = screenshot_path
        
        prompts = {
            "comprehensive": """Perform COMPREHENSIVE multi-modal analysis:

📊 **SCREEN INTELLIGENCE**
1. Application/Context: What's happening, what app/website
2. User Activity: What the user is doing, their workflow state
3. Content Analysis: Key information, data, messages visible
4. UI Elements: Important buttons, forms, navigation elements

🎯 **SMART INSIGHTS**
5. Productivity Assessment: Focus level, distractions, efficiency score (1-10)
6. Task Context: Current task, progress indicators, completion status
7. Attention Points: What should user focus on right now
8. Workflow State: Where in their workflow, next logical steps

⚠️ **ISSUE DETECTION**
9. Errors/Warnings: Any problems, alerts, or issues visible
10. Performance Indicators: Loading states, slow operations, bottlenecks
11. Security Concerns: Sensitive data visible, security warnings
12. UX Problems: Confusing elements, poor usability, accessibility issues

💡 **ACTIONABLE RECOMMENDATIONS**
13. Immediate Actions: What to do right now
14. Quick Wins: Small improvements with big impact
15. Automation Opportunities: Repetitive tasks that could be automated
16. Optimization Suggestions: How to work more efficiently

🔮 **PREDICTIVE INSIGHTS**
17. Next Likely Action: What user will probably do next
18. Potential Issues: Problems that might occur
19. Time Estimates: How long current task might take
20. Resource Needs: What resources/info user might need

Provide detailed, actionable insights with confidence scores.""",

            "security": """DEEP SECURITY ANALYSIS:

🛡️ **VULNERABILITY SCANNING**
1. Exposed Credentials: API keys, passwords, tokens visible
2. Sensitive Data: Personal info, credit cards, SSNs exposed
3. Security Warnings: Certificate errors, unsafe connections
4. Permissions: Unusual permission requests or access

🔒 **SECURITY BEST PRACTICES**
5. HTTPS Status: Check for secure connections
6. Authentication: Login states, session management
7. Data Exposure: What sensitive data is visible on screen
8. Privacy Concerns: Privacy violations, tracking, data collection

⚠️ **THREAT DETECTION**
9. Phishing Indicators: Suspicious URLs, fake login pages
10. Malware Signs: Unusual popups, system warnings
11. Social Engineering: Suspicious messages, urgent requests
12. Code Vulnerabilities: Security flaws in visible code

🚨 **RISK ASSESSMENT**
- Overall Security Score: 1-10 (10 = most secure)
- Critical Issues: List any immediate threats
- Recommendations: Specific actions to improve security
- Compliance: GDPR, accessibility, security standards

Rate severity as: CRITICAL / HIGH / MEDIUM / LOW""",

            "performance": """PERFORMANCE & OPTIMIZATION ANALYSIS:

⚡ **PERFORMANCE METRICS**
1. Loading Indicators: Spinners, progress bars, loading states
2. Response Times: Slow operations, delays, lag indicators
3. Resource Usage: Memory warnings, CPU usage indicators
4. Bottlenecks: Slow queries, render issues, blocking operations

🎯 **OPTIMIZATION OPPORTUNITIES**
5. Code Efficiency: Inefficient algorithms, unnecessary operations
6. Database Queries: N+1 queries, missing indexes, slow joins
7. Frontend Performance: Large bundles, unoptimized images, render blocking
8. Network Issues: Too many requests, large payloads, missing caching

🔧 **SPECIFIC IMPROVEMENTS**
9. Quick Fixes: Easy optimizations with immediate impact
10. Architecture Changes: Structural improvements needed
11. Best Practices: What's being done well vs. needs improvement
12. Technology Choices: Better tools or libraries to use

📊 **METRICS & BENCHMARKS**
- Performance Score: 1-10 (10 = optimal)
- Critical Bottlenecks: List top 3 issues
- Expected Improvements: Quantify potential gains
- Implementation Priority: What to fix first

Provide specific, actionable optimization strategies.""",

            "ux_expert": """PROFESSIONAL UX/UI EXPERT ANALYSIS:

🎨 **VISUAL DESIGN**
1. Visual Hierarchy: Is the important info prominent?
2. Color Theory: Color choices, contrast ratios, accessibility
3. Typography: Font choices, sizes, readability, hierarchy
4. Spacing & Layout: White space, alignment, balance, grid usage
5. Consistency: Design system adherence, pattern consistency

👁️ **USER EXPERIENCE**
6. Navigation: Clarity, discoverability, intuitive flow
7. Feedback: Loading states, success/error messages, confirmations
8. User Journey: Is the flow logical and efficient?
9. Cognitive Load: Is it overwhelming or easy to understand?
10. Error Prevention: Are mistakes prevented or easy to fix?

♿ **ACCESSIBILITY**
11. WCAG Compliance: AA/AAA standards, contrast ratios
12. Screen Reader Support: Alt text, ARIA labels, semantic HTML
13. Keyboard Navigation: Can everything be accessed via keyboard?
14. Text Readability: Size, contrast, line height, spacing

🚀 **INTERACTION DESIGN**
15. CTAs: Clear call-to-actions, button prominence
16. Forms: Field labels, validation, error handling
17. Micro-interactions: Hover states, transitions, animations
18. Mobile Responsiveness: Touch targets, responsive design

💎 **PROFESSIONAL CRITIQUE**
- UX Score: 1-10 (10 = exceptional UX)
- Design Score: 1-10 (10 = professional quality)
- Top 3 Strengths: What's done exceptionally well
- Top 5 Improvements: Specific, actionable changes
- Industry Standards: How it compares to best practices

Provide expert-level critique with specific examples.""",

            "accessibility": """ACCESSIBILITY COMPLIANCE ANALYSIS:

♿ **WCAG 2.1 COMPLIANCE CHECK**

**Level A (Must Have)**
1. Text Alternatives: Images have alt text?
2. Keyboard Access: All functions keyboard accessible?
3. Sufficient Contrast: Text readable (4.5:1 minimum)?
4. No Keyboard Traps: Can navigate in/out freely?

**Level AA (Should Have)**
5. Enhanced Contrast: Better readability (7:1 for large text)?
6. Resize Text: Can text scale to 200% without loss?
7. Multiple Ways: More than one way to navigate?
8. Consistent Navigation: Predictable navigation patterns?

**Level AAA (Nice to Have)**
9. Enhanced Contrast: Maximum readability (7:1 all text)?
10. No Images of Text: Text is actual text, not images?
11. Visual Presentation: Optimal spacing and formatting?

🔍 **SPECIFIC ACCESSIBILITY CHECKS**
12. Color Usage: Info not conveyed by color alone?
13. Focus Indicators: Clear focus states visible?
14. Form Labels: All inputs properly labeled?
15. Heading Structure: Logical heading hierarchy (h1-h6)?
16. Link Purpose: Link text descriptive and clear?
17. Error Identification: Errors clearly identified?
18. Touch Targets: Buttons/links large enough (44x44px)?

⚠️ **BARRIERS IDENTIFIED**
- List all accessibility violations
- Rate severity: BLOCKER / CRITICAL / MAJOR / MINOR
- Affected user groups: Visual, motor, cognitive, hearing
- Legal compliance: ADA, Section 508, WCAG level

✅ **COMPLIANCE SCORE**
- WCAG Level A: Pass/Fail (% compliant)
- WCAG Level AA: Pass/Fail (% compliant)
- WCAG Level AAA: Pass/Fail (% compliant)
- Overall Accessibility Score: 1-10

Provide specific fixes for each violation.""",

            "code_review": """EXPERT CODE REVIEW & REFACTORING:

🔍 **CODE QUALITY ANALYSIS**
1. Architecture: Design patterns, structure, organization
2. Naming: Variables, functions, classes - clear and consistent?
3. Readability: Comments, formatting, self-documenting code
4. Complexity: Cyclomatic complexity, nested logic
5. DRY Principle: Code duplication, reusability

🐛 **BUG DETECTION**
6. Logic Errors: Off-by-one, null checks, edge cases
7. Type Safety: Type mismatches, unsafe operations
8. Error Handling: Try-catch blocks, error propagation
9. Race Conditions: Concurrency issues, async problems
10. Memory Leaks: Resource cleanup, reference management

🚀 **PERFORMANCE ISSUES**
11. Algorithm Efficiency: O(n²) that could be O(n)?
12. Database Queries: N+1 problems, missing indexes
13. Unnecessary Operations: Redundant calculations, loops
14. Caching Opportunities: What should be cached?
15. Lazy Loading: What could be loaded on demand?

🔒 **SECURITY VULNERABILITIES**
16. Input Validation: SQL injection, XSS, CSRF risks
17. Authentication: Password handling, session management
18. Data Exposure: Sensitive data in logs, errors, URLs
19. Dependency Issues: Outdated libraries, known vulnerabilities
20. API Security: Rate limiting, authentication, validation

♻️ **REFACTORING SUGGESTIONS**
21. Extract Methods: Long functions to break down
22. Design Patterns: Where to apply patterns (Factory, Strategy, etc.)
23. SOLID Principles: Single responsibility, open/closed violations
24. Test Coverage: What needs tests, missing edge cases
25. Modern Practices: Update to current best practices

📊 **CODE METRICS**
- Code Quality Score: 1-10
- Maintainability Index: 1-100
- Technical Debt: Low/Medium/High
- Refactoring Priority: What to fix first

Provide specific line-by-line suggestions with code examples.""",

            "design_critique": """PROFESSIONAL DESIGN CRITIQUE:

🎨 **VISUAL DESIGN PRINCIPLES**

**Hierarchy & Focus**
1. Visual Weight: What draws the eye first?
2. F-Pattern / Z-Pattern: Does layout match reading patterns?
3. Focal Points: Clear primary and secondary elements?
4. Information Architecture: Logical grouping and structure?

**Color & Aesthetics**
5. Color Harmony: Complementary, analogous, triadic schemes?
6. Brand Consistency: Colors match brand identity?
7. Color Psychology: Do colors evoke right emotions?
8. Contrast & Legibility: Can everything be read easily?

**Typography Excellence**
9. Type Scale: Proper heading hierarchy (H1-H6)?
10. Font Pairing: Do fonts work well together?
11. Line Length: 50-75 characters for readability?
12. Line Height: Proper spacing (1.5-1.8 for body text)?

**Spacing & Rhythm**
13. White Space: Breathing room, not cramped?
14. Vertical Rhythm: Consistent spacing throughout?
15. Grid System: Proper alignment and structure?
16. Padding & Margins: Consistent spacing units?

🎯 **INTERACTION & UX DESIGN**

**User Flow**
17. Task Completion: Clear path to user goals?
18. Progressive Disclosure: Info revealed at right time?
19. Error Prevention: Guard rails and confirmations?
20. Feedback Loops: Clear system responses?

**Component Design**
21. Buttons: Clear, accessible, properly sized?
22. Forms: Labels, validation, helpful errors?
23. Navigation: Intuitive, discoverable, consistent?
24. Cards/Modules: Proper information density?

📱 **RESPONSIVE & MODERN**
25. Mobile-First: Works on small screens?
26. Touch Targets: 44x44px minimum?
27. Responsive Images: Proper sizing and formats?
28. Modern Patterns: Following current trends?

💎 **BRAND & POLISH**
29. Personality: Does it match brand voice?
30. Delight Factors: Micro-interactions, animations?
31. Professional Polish: Attention to detail?
32. Competitive Analysis: How vs. industry leaders?

🏆 **DESIGN SCORES**
- Visual Design: 1-10
- User Experience: 1-10  
- Brand Alignment: 1-10
- Innovation: 1-10
- Overall Design Quality: 1-10

📋 **DETAILED FEEDBACK**
**What's Exceptional:** (3 strengths)
**What Needs Work:** (5 specific improvements)
**Quick Wins:** (3 easy high-impact changes)
**Long-term Vision:** (Strategic design direction)

Provide professional designer-level critique.""",

            "automation_discovery": """AUTOMATION OPPORTUNITY ANALYSIS:

🤖 **WORKFLOW AUTOMATION DISCOVERY**

**Repetitive Tasks Detected**
1. Manual Data Entry: Copy-paste, form filling, repetitive typing
2. File Operations: Organizing, renaming, moving files
3. Data Processing: Excel operations, calculations, formatting
4. Email Tasks: Sending similar emails, forwarding, organizing
5. Web Actions: Login sequences, form submissions, data extraction

**Click Pattern Analysis**
6. Repeated Navigation: Same menu clicks, button sequences
7. Multi-step Processes: Tasks with predictable steps
8. Scheduled Actions: Tasks done at specific times/intervals
9. Conditional Logic: If-then patterns in user behavior
10. Data Collection: Gathering info from multiple sources

🎯 **AUTOMATION POTENTIAL**

**High Priority (Easy & High Impact)**
- Task: [Specific repetitive task]
- Time Saved: [Estimate per execution]
- Frequency: [How often performed]
- Complexity: Low/Medium/High
- ROI: Hours saved per month

**Medium Priority (Moderate Effort)**
[Same structure as above]

**Low Priority (Complex or Infrequent)**
[Same structure as above]

🔧 **AUTOMATION SOLUTIONS**

For each task provide:
1. **Solution Type**: Macro, script, tool, integration
2. **Implementation**: Step-by-step how to automate
3. **Tools Needed**: Software, APIs, scripts required
4. **Effort Estimate**: Hours to setup
5. **Maintenance**: Ongoing needs
6. **Risk Assessment**: What could break

💡 **SMART SUGGESTIONS**
- Keyboard Shortcuts: Shortcuts user should learn
- Browser Extensions: Tools that could help
- Scripts to Create: Custom automation scripts
- Integrations: Connect tools together (Zapier, IFTTT)
- AI Assistance: Where AI could help

📊 **AUTOMATION METRICS**
- Total Time Saved: Hours per week/month
- Tasks Identified: Count of automatable tasks
- Quick Wins: Tasks to automate first
- Long-term Projects: Complex automations worth building

Provide specific, actionable automation strategies."""
        }
        
        base_prompt = prompts.get(mode, prompts["comprehensive"])
        
        json_instruction = """

**IMPORTANT: Respond with BOTH detailed analysis AND structured JSON.**

First provide your detailed analysis, then end with a JSON block:

```json
{
    "scores": {
        "productivity": 0-10 (if applicable),
        "performance": 0-10 (if applicable),
        "security": 0-10 (if applicable),
        "ux_quality": 0-10 (if applicable),
        "accessibility": 0-10 (if applicable),
        "code_quality": 0-10 (if applicable),
        "design_quality": 0-10 (if applicable)
    },
    "issues": [
        {
            "type": "error|warning|security|performance|ux|accessibility",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "description": "Brief description",
            "location": "Where it's found",
            "impact": "Impact description"
        }
    ],
    "recommendations": [
        {
            "priority": "HIGH|MEDIUM|LOW",
            "action": "What to do",
            "benefit": "Expected improvement",
            "effort": "LOW|MEDIUM|HIGH"
        }
    ],
    "predictions": {
        "next_action": "Predicted user action",
        "confidence": 0-100,
        "time_estimate_minutes": 0-1000
    },
    "automation_opportunities": [
        {
            "task": "Task description",
            "time_saved_minutes": 0-1000,
            "complexity": "LOW|MEDIUM|HIGH",
            "roi": "HIGH|MEDIUM|LOW"
        }
    ]
}
```

Only include fields relevant to the analysis mode."""
        
        prompt = base_prompt + json_instruction
        
        print("   🤖 AI analyzing with advanced intelligence...")
        analysis = self._analyze_with_gemini(screenshot_path, prompt)
        
        structured_data = self._extract_structured_data(analysis)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "analysis": analysis,
            "structured_data": structured_data,
            "screenshot": screenshot_path
        }
        self.activity_log.append(log_entry)
        
        self._update_analytics_structured(mode, structured_data)
        self._learn_patterns(mode, analysis)
        
        return {
            "success": True,
            "mode": mode,
            "analysis": analysis,
            "structured_data": structured_data,
            "screenshot": screenshot_path,
            "timestamp": datetime.now().isoformat(),
            "analytics_updated": True
        }
    
    def smart_object_detection(self, objects_to_find: List[str]) -> Dict:
        """
        Advanced object detection - find specific UI elements, text, buttons, etc.
        
        Args:
            objects_to_find: List of objects to locate (e.g., ["Login button", "Error message", "Profile picture"])
        """
        print(f"\n🔍 Smart Object Detection for: {', '.join(objects_to_find)}")
        screenshot_path = self.gui.screenshot("object_detection")
        
        if not screenshot_path:
            return self._cloud_unavailable_message()
        
        prompt = f"""ADVANCED OBJECT DETECTION TASK:

Find and analyze these specific objects/elements:
{chr(10).join(f'{i+1}. {obj}' for i, obj in enumerate(objects_to_find))}

For EACH object provide:
**Object: [Name]**
- Found: YES / NO
- Location: Exact position (top-left, center, bottom-right, etc.)
- Coordinates: Approximate x,y if possible
- Description: What it looks like, color, size, text
- State: Active/inactive, visible/hidden, enabled/disabled
- Context: What's around it, related elements
- Confidence: 1-10 (how sure you are)

**Interactions Possible:**
- What can user do with this element?
- What happens when clicked/used?

**Accessibility:**
- Is it keyboard accessible?
- Does it have proper labels?
- Color contrast sufficient?

If an object is NOT found, suggest:
- Similar elements that ARE visible
- Where user should look instead
- Why it might not be visible (permissions, state, etc.)"""
        
        analysis = self._analyze_with_gemini(screenshot_path, prompt)
        
        return {
            "success": True,
            "objects_searched": objects_to_find,
            "analysis": analysis,
            "screenshot": screenshot_path
        }
    
    def continuous_monitoring(self, duration_minutes: int = 30, 
                            check_interval: int = 30,
                            triggers: Optional[Dict] = None) -> Dict:
        """
        Continuous AI monitoring with intelligent triggers
        
        Args:
            duration_minutes: How long to monitor
            check_interval: Seconds between checks
            triggers: Dict of conditions to watch for
                {
                    "errors": True,  # Alert on errors
                    "security": True,  # Alert on security issues
                    "productivity_drop": 3,  # Alert if score drops below 3
                    "specific_text": "error",  # Alert if text appears
                    "performance_issues": True
                }
        """
        if triggers is None:
            triggers = {
                "errors": True,
                "security": True,
                "productivity_drop": 4
            }
        
        print(f"\n👁️ Starting Continuous Monitoring")
        print(f"   ⏱️  Duration: {duration_minutes} minutes")
        print(f"   🔄 Check interval: {check_interval} seconds")
        print(f"   🎯 Triggers: {', '.join(f'{k}={v}' for k, v in triggers.items())}")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        iteration = 0
        alerts_triggered = []
        
        while datetime.now() < end_time:
            iteration += 1
            print(f"\n   📸 Check {iteration} at {datetime.now().strftime('%H:%M:%S')}")
            
            result = self.advanced_screen_analysis("comprehensive")
            
            if result["success"]:
                structured_data = result.get("structured_data", {})
                analysis = result["analysis"]
                
                if triggers.get("errors") and structured_data:
                    issues = structured_data.get("issues", [])
                    error_issues = [i for i in issues if i.get("type") in ["error", "warning"]]
                    
                    if error_issues:
                        critical_errors = [e for e in error_issues if e.get("severity") == "CRITICAL"]
                        high_errors = [e for e in error_issues if e.get("severity") == "HIGH"]
                        
                        if critical_errors or high_errors:
                            for error in (critical_errors + high_errors):
                                alert = {
                                    "type": "ERROR_DETECTED",
                                    "time": datetime.now().isoformat(),
                                    "severity": error.get("severity", "MEDIUM"),
                                    "details": error.get("description", "Error detected"),
                                    "location": error.get("location", ""),
                                    "screenshot": result["screenshot"]
                                }
                                alerts_triggered.append(alert)
                                self.alerts.append(alert)
                                print(f"   🚨 ALERT: {error.get('severity')} error - {error.get('description', '')[:50]}")
                
                if triggers.get("security") and structured_data:
                    issues = structured_data.get("issues", [])
                    security_issues = [i for i in issues if i.get("type") == "security"]
                    scores = structured_data.get("scores", {})
                    sec_score = scores.get("security", 10)
                    
                    if security_issues or sec_score < 5:
                        for issue in security_issues:
                            alert = {
                                "type": "SECURITY_CONCERN",
                                "time": datetime.now().isoformat(),
                                "severity": issue.get("severity", "MEDIUM"),
                                "details": issue.get("description", "Security concern detected"),
                                "screenshot": result["screenshot"]
                            }
                            alerts_triggered.append(alert)
                            self.alerts.append(alert)
                            print(f"   🛡️ ALERT: {issue.get('severity')} security - {issue.get('description', '')[:50]}")
                
                if triggers.get("productivity_drop") and isinstance(triggers["productivity_drop"], (int, float)) and structured_data:
                    scores = structured_data.get("scores", {})
                    prod_score = scores.get("productivity", 0)
                    
                    if prod_score > 0 and prod_score < triggers["productivity_drop"]:
                        alert = {
                            "type": "PRODUCTIVITY_DROP",
                            "time": datetime.now().isoformat(),
                            "score": prod_score,
                            "threshold": triggers["productivity_drop"],
                            "details": f"Productivity score {prod_score}/10 below threshold {triggers['productivity_drop']}",
                            "screenshot": result["screenshot"]
                        }
                        alerts_triggered.append(alert)
                        self.alerts.append(alert)
                        print(f"   📉 ALERT: Productivity drop (score: {prod_score}/10)!")
                
                if triggers.get("performance_issues") and structured_data:
                    issues = structured_data.get("issues", [])
                    perf_issues = [i for i in issues if i.get("type") == "performance"]
                    scores = structured_data.get("scores", {})
                    perf_score = scores.get("performance", 10)
                    
                    if perf_issues or perf_score < 5:
                        for issue in perf_issues:
                            alert = {
                                "type": "PERFORMANCE_ISSUE",
                                "time": datetime.now().isoformat(),
                                "severity": issue.get("severity", "MEDIUM"),
                                "details": issue.get("description", "Performance issue detected"),
                                "screenshot": result["screenshot"]
                            }
                            alerts_triggered.append(alert)
                            self.alerts.append(alert)
                            print(f"   ⚡ ALERT: Performance issue - {issue.get('description', '')[:50]}")
                
                if triggers.get("specific_text"):
                    analysis_lower = analysis.lower()
                    if triggers["specific_text"].lower() in analysis_lower:
                        alert = {
                            "type": "TEXT_FOUND",
                            "time": datetime.now().isoformat(),
                            "details": f"Found text: {triggers['specific_text']}",
                            "screenshot": result["screenshot"]
                        }
                        alerts_triggered.append(alert)
                        self.alerts.append(alert)
                        print(f"   📝 ALERT: Found '{triggers['specific_text']}'!")
            
            if datetime.now() < end_time:
                print(f"   ⏳ Next check in {check_interval}s...")
                time.sleep(check_interval)
        
        monitoring_duration = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": True,
            "duration": monitoring_duration,
            "checks_performed": iteration,
            "alerts": alerts_triggered,
            "alert_count": len(alerts_triggered),
            "summary": f"Monitored for {monitoring_duration/60:.1f} minutes with {len(alerts_triggered)} alerts"
        }
    
    def predictive_analysis(self) -> Dict:
        """
        Predict what user is likely to do next and suggest optimizations
        """
        print("\n🔮 Predictive Analysis")
        screenshot_path = self.gui.screenshot("predictive")
        
        if not screenshot_path:
            return self._cloud_unavailable_message()
        
        prompt = """PREDICTIVE INTELLIGENCE ANALYSIS:

Based on current screen state, predict and analyze:

🎯 **NEXT LIKELY ACTIONS**
1. What is the user most likely to do next? (3 predictions with probability)
2. What buttons/links will they probably click?
3. What information will they need next?
4. What problems might they encounter?

⏱️ **TIME PREDICTIONS**
5. How long will current task likely take?
6. When will they need a break?
7. Time-to-completion estimate for current work

🚀 **OPTIMIZATION SUGGESTIONS**
8. Keyboard shortcuts they should use instead
9. Faster ways to accomplish their current task
10. Tools or features they're not using but should
11. Workflow improvements for efficiency

🧠 **INTELLIGENT INSIGHTS**
12. Is there a better sequence of steps?
13. Are they working in the optimal application?
14. Should they batch this task with others?
15. Automation opportunities for current workflow

⚠️ **POTENTIAL ISSUES**
16. What errors might occur next?
17. What information is missing?
18. Blockers or bottlenecks ahead?
19. Risk assessment (1-10)

💡 **PROACTIVE RECOMMENDATIONS**
- Do this now: [Immediate action]
- Prepare for: [Upcoming need]
- Avoid this: [Potential mistake]
- Remember to: [Important reminder]

Be specific and actionable with confidence scores."""
        
        analysis = self._analyze_with_gemini(screenshot_path, prompt)
        
        return {
            "success": True,
            "predictions": analysis,
            "screenshot": screenshot_path,
            "timestamp": datetime.now().isoformat()
        }
    
    def advanced_comparison(self, mode: str = "changes") -> Dict:
        """
        Advanced multi-screenshot comparison and analysis
        
        Modes:
        - changes: Detect what changed
        - progression: Track task progression
        - deterioration: Find if things got worse
        - improvement: Validate improvements made
        """
        print(f"\n📊 Advanced Comparison - Mode: {mode}")
        print("   📸 Taking before snapshot...")
        
        screenshot1 = self.gui.screenshot("compare_before")
        if not screenshot1:
            return self._cloud_unavailable_message()
        
        print("   ⏳ Waiting 10 seconds for changes...")
        time.sleep(10)
        
        print("   📸 Taking after snapshot...")
        screenshot2 = self.gui.screenshot("compare_after")
        if not screenshot2:
            return self._cloud_unavailable_message()
        
        with open(screenshot1, "rb") as f1, open(screenshot2, "rb") as f2:
            img1_data = f1.read()
            img2_data = f2.read()
        
        prompts = {
            "changes": """DETAILED CHANGE ANALYSIS:

Compare these two screenshots and provide:

**What Changed:**
1. UI Elements: Added, removed, or modified elements
2. Content: Text changes, new information, removed data
3. Visual: Color changes, layout shifts, style updates
4. State: Application state changes, page navigation
5. Data: Numbers, values, counters that changed

**Change Assessment:**
- Type: UI / Content / Data / Navigation / State
- Magnitude: Minor / Moderate / Major / Critical
- Impact: How this affects user workflow
- Significance: Why this change matters

**Timeline Analysis:**
- Time elapsed: [estimate]
- User actions: What did user likely do?
- Workflow progress: Moving forward or backward?
- Task status: Started / In-progress / Completed / Blocked

**Recommendations:**
- Is this good progress?
- Should user continue this path?
- Any concerns or warnings?
- Next suggested actions""",

            "progression": """TASK PROGRESSION ANALYSIS:

Analyze progression between screenshots:

**Progress Indicators:**
1. Task Completion: % complete, progress bars, checkmarks
2. Data Processing: Records processed, items remaining
3. Workflow Stage: What phase of work (start/middle/end)?
4. Quality Metrics: Are things improving or degrading?

**Productivity Assessment:**
- Progress Rate: Fast / Moderate / Slow / Stalled
- Efficiency: Working optimally or inefficiently?
- Blockers: Any obstacles encountered?
- Focus: Stayed on task or got distracted?

**Predictions:**
- Time to completion: [estimate]
- Likely next milestone: [prediction]
- Potential issues: [warnings]
- Success probability: [percentage]

**Recommendations:**
What should user do to optimize progression?""",

            "deterioration": """DETERIORATION DETECTION:

Check if things got WORSE between screenshots:

**Problems That Appeared:**
1. New errors or warnings
2. Performance degradation
3. Visual glitches or bugs
4. Lost data or progress
5. Broken functionality

**Quality Metrics:**
- Did code quality decrease?
- Is UI/UX worse?
- More errors visible?
- Slower performance?
- Reduced usability?

**Root Cause Analysis:**
- What caused the deterioration?
- What action led to problems?
- Could this have been prevented?
- How to fix it?

**Severity Assessment:**
- Critical / High / Medium / Low
- Impact on user productivity
- Immediate actions needed

**Recovery Plan:**
Specific steps to fix issues and recover.""",

            "improvement": """IMPROVEMENT VALIDATION:

Validate if changes made things BETTER:

**Improvements Detected:**
1. UI/UX enhancements
2. Performance gains
3. Bugs fixed
4. Better organization
5. Increased clarity

**Quality Metrics:**
- Code quality: Improved / Same / Worse
- User experience: Better / Same / Worse  
- Performance: Faster / Same / Slower
- Design: Enhanced / Same / Degraded
- Functionality: More / Same / Less

**Quantifiable Gains:**
- Efficiency increase: [percentage]
- Error reduction: [count]
- Speed improvement: [metric]
- Usability gain: [score]

**Validation:**
✅ Changes that worked well
⚠️ Changes that need refinement
❌ Changes that should be reverted

**Recommendations:**
- Keep these changes: [list]
- Refine these: [list]
- Revert these: [list]
- Next improvements: [suggestions]"""
        }
        
        prompt = prompts.get(mode, prompts["changes"])
        
        print("   🤖 AI comparing screenshots...")
        
        try:
            client = get_client()
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text=f"Screenshot 1 (BEFORE):\n{prompt}"),
                            types.Part(inline_data=types.Blob(mime_type="image/png", data=img1_data)),
                            types.Part(text="Screenshot 2 (AFTER):"),
                            types.Part(inline_data=types.Blob(mime_type="image/png", data=img2_data))
                        ]
                    )
                ]
            )
            
            analysis = response.text or "Could not compare screenshots"
            
            return {
                "success": True,
                "mode": mode,
                "comparison": analysis,
                "before": screenshot1,
                "after": screenshot2
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Comparison failed: {str(e)}"
            }
    
    def security_scan(self) -> Dict:
        """Deep security vulnerability scan"""
        return self.advanced_screen_analysis("security")
    
    def performance_audit(self) -> Dict:
        """Performance and optimization audit"""
        return self.advanced_screen_analysis("performance")
    
    def ux_expert_review(self) -> Dict:
        """Professional UX/UI expert review"""
        return self.advanced_screen_analysis("ux_expert")
    
    def accessibility_audit(self) -> Dict:
        """Full accessibility compliance audit"""
        return self.advanced_screen_analysis("accessibility")
    
    def code_review(self) -> Dict:
        """Expert code review with refactoring suggestions"""
        return self.advanced_screen_analysis("code_review")
    
    def design_critique(self) -> Dict:
        """Professional design critique"""
        return self.advanced_screen_analysis("design_critique")
    
    def find_automation_opportunities(self) -> Dict:
        """Discover automation opportunities in current workflow"""
        return self.advanced_screen_analysis("automation_discovery")
    
    def intelligent_qa(self, question: str) -> Dict:
        """
        Ask intelligent questions about screen with context awareness
        """
        print(f"\n💭 Intelligent Q&A: '{question}'")
        screenshot_path = self.gui.screenshot("intelligent_qa")
        
        if not screenshot_path:
            return self._cloud_unavailable_message()
        
        prompt = f"""INTELLIGENT QUESTION ANSWERING:

Question: {question}

Provide a comprehensive, intelligent answer that includes:

📋 **Direct Answer:**
Clear, concise response to the question

🔍 **Context & Details:**
Additional relevant information and context

💡 **Insights:**
Deeper insights related to the question

🎯 **Actionable Information:**
What user can do with this information

⚠️ **Warnings/Considerations:**
Any caveats or things to be aware of

🔗 **Related Information:**
Other relevant details user might want to know

Be specific, accurate, and helpful. If you're not sure, say so and explain why."""
        
        analysis = self._analyze_with_gemini(screenshot_path, prompt)
        
        return {
            "success": True,
            "question": question,
            "answer": analysis,
            "screenshot": screenshot_path
        }
    
    def get_analytics_report(self) -> Dict:
        """
        Generate comprehensive analytics report
        """
        print("\n📊 Generating Analytics Report...")
        
        total_analyses = len(self.activity_log)
        total_alerts = len(self.alerts)
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║         ADVANCED SCREEN MONITOR ANALYTICS REPORT         ║
╚══════════════════════════════════════════════════════════╝

📊 OVERALL STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Analyses Performed: {total_analyses}
• Total Alerts Generated: {total_alerts}
• Monitoring Sessions: {len([a for a in self.activity_log if 'mode' in a])}
• Screenshots Captured: {len([a for a in self.activity_log if 'screenshot' in a])}

🎯 ANALYSIS BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        modes = {}
        for entry in self.activity_log:
            mode = entry.get('mode', entry.get('focus', 'unknown'))
            modes[mode] = modes.get(mode, 0) + 1
        
        for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
            report += f"• {mode.replace('_', ' ').title()}: {count}\n"
        
        prod_scores = self.analytics.get("productivity_scores", [])
        if prod_scores:
            avg_prod = sum(s["score"] for s in prod_scores) / len(prod_scores)
            report += f"\n📈 PRODUCTIVITY INSIGHTS\n"
            report += "━" * 60 + "\n"
            report += f"• Productivity Checks: {len(prod_scores)}\n"
            report += f"• Average Productivity Score: {avg_prod:.1f}/10\n"
            recent = prod_scores[-5:]
            report += f"• Recent Scores: {', '.join(str(s['score']) for s in recent)}\n"
        
        perf_metrics = self.analytics.get("performance_metrics", [])
        if perf_metrics:
            avg_perf = sum(m["score"] for m in perf_metrics) / len(perf_metrics)
            report += f"\n⚡ PERFORMANCE INSIGHTS\n"
            report += "━" * 60 + "\n"
            report += f"• Performance Checks: {len(perf_metrics)}\n"
            report += f"• Average Performance Score: {avg_perf:.1f}/10\n"
        
        errors = self.analytics.get("errors_detected", [])
        if errors:
            critical = len([e for e in errors if e.get("severity") == "CRITICAL"])
            high = len([e for e in errors if e.get("severity") == "HIGH"])
            medium = len([e for e in errors if e.get("severity") == "MEDIUM"])
            low = len([e for e in errors if e.get("severity") == "LOW"])
            
            report += f"\n⚠️  ERROR TRACKING\n"
            report += "━" * 60 + "\n"
            report += f"• Total Errors Detected: {len(errors)}\n"
            if critical: report += f"• CRITICAL: {critical}\n"
            if high: report += f"• HIGH: {high}\n"
            if medium: report += f"• MEDIUM: {medium}\n"
            if low: report += f"• LOW: {low}\n"
        
        security_issues = self.analytics.get("security_issues", [])
        if security_issues:
            critical_sec = len([s for s in security_issues if s.get("severity") == "CRITICAL"])
            high_sec = len([s for s in security_issues if s.get("severity") == "HIGH"])
            
            report += f"\n🛡️  SECURITY TRACKING\n"
            report += "━" * 60 + "\n"
            report += f"• Total Security Issues: {len(security_issues)}\n"
            if critical_sec: report += f"• CRITICAL: {critical_sec}\n"
            if high_sec: report += f"• HIGH: {high_sec}\n"
            report += f"• Most Recent: {security_issues[-1].get('description', 'N/A')[:50]}...\n" if security_issues else ""
        
        if self.alerts:
            report += f"\n🚨 RECENT ALERTS\n"
            report += "━" * 60 + "\n"
            for alert in self.alerts[-5:]:
                severity = alert.get('severity', '')
                severity_str = f"[{severity}] " if severity else ""
                report += f"• {severity_str}[{alert.get('type', 'ALERT')}] {alert.get('details', 'No details')[:50]}\n"
                report += f"  Time: {alert.get('time', 'Unknown')}\n"
        
        if self.patterns:
            report += f"\n🧠 PATTERN LEARNING\n"
            report += "━" * 60 + "\n"
            report += f"• Patterns Tracked: {len(self.patterns)} time periods\n"
            for pattern_key in list(self.patterns.keys())[-3:]:
                pattern = self.patterns[pattern_key]
                report += f"• {pattern_key}: {len(pattern['modes_used'])} analyses, {pattern['error_frequency']} errors\n"
        
        report += f"\n✨ SYSTEM STATUS\n"
        report += "━" * 60 + "\n"
        report += f"• Monitor Active: {'Yes' if self.monitoring else 'No'}\n"
        report += f"• Last Screenshot: {self.last_screenshot or 'None'}\n"
        report += f"• Learning Data Points: {sum(d['usage_count'] for d in self.learning_data.values()) if self.learning_data else 0}\n"
        
        return {
            "success": True,
            "report": report,
            "total_analyses": total_analyses,
            "total_alerts": total_alerts,
            "modes": modes,
            "recent_alerts": self.alerts[-5:] if self.alerts else []
        }
    
    def export_activity_log(self, filename: str = "screen_monitor_log.json") -> Dict:
        """Export activity log to JSON file"""
        try:
            filepath = os.path.join("screenshots", filename)
            os.makedirs("screenshots", exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump({
                    "export_time": datetime.now().isoformat(),
                    "total_entries": len(self.activity_log),
                    "activity_log": self.activity_log,
                    "alerts": self.alerts,
                    "analytics": self.analytics
                }, f, indent=2)
            
            return {
                "success": True,
                "message": f"Activity log exported to {filepath}",
                "filepath": filepath,
                "entries": len(self.activity_log)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to export: {str(e)}"
            }
    
    def clear_all_data(self) -> Dict:
        """Clear all monitoring data"""
        self.activity_log = []
        self.alerts = []
        self.patterns = {}
        self.learning_data = {}
        self.analytics = {
            "productivity_scores": [],
            "errors_detected": [],
            "security_issues": [],
            "performance_metrics": []
        }
        
        return {
            "success": True,
            "message": "All monitoring data cleared"
        }
    
    def _extract_structured_data(self, analysis: str) -> Dict:
        """Extract structured JSON data from analysis response"""
        try:
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', analysis, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            json_match = re.search(r'\{[\s\S]*"scores"[\s\S]*\}', analysis)
            if json_match:
                return json.loads(json_match.group(0))
            
            return {}
        except Exception as e:
            print(f"   ⚠️  Could not extract structured data: {e}")
            return {}
    
    def _update_analytics_structured(self, mode: str, structured_data: Dict):
        """Update analytics using structured data"""
        if not structured_data:
            return
        
        timestamp = datetime.now().isoformat()
        
        scores = structured_data.get("scores", {})
        for score_type, score_value in scores.items():
            if isinstance(score_value, (int, float)) and score_value > 0:
                if score_type == "productivity":
                    self.analytics["productivity_scores"].append({
                        "score": score_value,
                        "timestamp": timestamp,
                        "mode": mode
                    })
                elif score_type == "performance":
                    self.analytics["performance_metrics"].append({
                        "score": score_value,
                        "timestamp": timestamp,
                        "mode": mode
                    })
        
        issues = structured_data.get("issues", [])
        for issue in issues:
            if issue.get("type") in ["error", "warning"]:
                self.analytics["errors_detected"].append({
                    "severity": issue.get("severity", "MEDIUM"),
                    "type": issue.get("type"),
                    "description": issue.get("description", ""),
                    "timestamp": timestamp,
                    "mode": mode
                })
            
            if issue.get("type") == "security" or "security" in issue.get("description", "").lower():
                self.analytics["security_issues"].append({
                    "severity": issue.get("severity", "MEDIUM"),
                    "description": issue.get("description", ""),
                    "location": issue.get("location", ""),
                    "timestamp": timestamp,
                    "mode": mode
                })
    
    def _extract_error_details(self, analysis: str) -> str:
        """Extract error details from analysis"""
        lines = analysis.split('\n')
        error_lines = [line for line in lines if any(
            keyword in line.lower() for keyword in ['error', 'warning', 'exception', 'failed', 'bug']
        )]
        return '\n'.join(error_lines[:3]) if error_lines else "Error detected in analysis"
    
    def _extract_security_details(self, analysis: str) -> str:
        """Extract security details from analysis"""
        lines = analysis.split('\n')
        security_lines = [line for line in lines if any(
            keyword in line.lower() for keyword in ['security', 'vulnerability', 'password', 'credential', 'exposed', 'sensitive']
        )]
        return '\n'.join(security_lines[:3]) if security_lines else "Security concern detected in analysis"
    
    def _extract_performance_details(self, analysis: str) -> str:
        """Extract performance details from analysis"""
        lines = analysis.split('\n')
        perf_lines = [line for line in lines if any(
            keyword in line.lower() for keyword in ['slow', 'performance', 'bottleneck', 'lag', 'delay', 'loading']
        )]
        return '\n'.join(perf_lines[:3]) if perf_lines else "Performance issue detected in analysis"
    
    def _update_analytics(self, mode: str, analysis: str):
        """Update analytics based on analysis results"""
        analysis_lower = analysis.lower()
        
        if mode == "comprehensive" or mode == "productivity":
            import re
            score_match = re.search(r'(?:productivity|efficiency).*?(\d+)(?:/10|out of 10)', analysis_lower)
            if score_match:
                score = int(score_match.group(1))
                self.analytics["productivity_scores"].append({
                    "score": score,
                    "timestamp": datetime.now().isoformat()
                })
        
        if "error" in analysis_lower or "warning" in analysis_lower:
            self.analytics["errors_detected"].append({
                "mode": mode,
                "timestamp": datetime.now().isoformat(),
                "summary": analysis[:200]
            })
        
        if mode == "security" or "security" in analysis_lower or "vulnerability" in analysis_lower:
            severity = "UNKNOWN"
            if "critical" in analysis_lower:
                severity = "CRITICAL"
            elif "high" in analysis_lower:
                severity = "HIGH"
            elif "medium" in analysis_lower:
                severity = "MEDIUM"
            elif "low" in analysis_lower:
                severity = "LOW"
            
            self.analytics["security_issues"].append({
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
                "summary": analysis[:200]
            })
        
        if mode == "performance":
            import re
            score_match = re.search(r'performance.*?score.*?(\d+)(?:/10|out of 10)', analysis_lower)
            if score_match:
                score = int(score_match.group(1))
                self.analytics["performance_metrics"].append({
                    "score": score,
                    "timestamp": datetime.now().isoformat()
                })
    
    def _learn_patterns(self, mode: str, analysis: str):
        """Learn patterns from analysis results"""
        hour = datetime.now().hour
        day = datetime.now().strftime("%A")
        
        pattern_key = f"{day}_{hour}"
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = {
                "modes_used": [],
                "common_activities": [],
                "error_frequency": 0,
                "productivity_avg": 0
            }
        
        self.patterns[pattern_key]["modes_used"].append(mode)
        
        analysis_lower = analysis.lower()
        if "error" in analysis_lower or "warning" in analysis_lower:
            self.patterns[pattern_key]["error_frequency"] += 1
        
        if mode not in self.learning_data:
            self.learning_data[mode] = {
                "usage_count": 0,
                "common_findings": [],
                "avg_analysis_length": 0
            }
        
        self.learning_data[mode]["usage_count"] += 1
        self.learning_data[mode]["avg_analysis_length"] = (
            (self.learning_data[mode]["avg_analysis_length"] * (self.learning_data[mode]["usage_count"] - 1) + len(analysis)) 
            / self.learning_data[mode]["usage_count"]
        )
    
    def _analyze_with_gemini(self, image_path: str, prompt: str) -> str:
        """Internal method to analyze screenshot with Gemini"""
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            client = get_client()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text=prompt),
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="image/png",
                                    data=image_data
                                )
                            )
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=4096
                )
            )
            
            return response.text or "Could not analyze image"
        
        except FileNotFoundError:
            return f"Error: Screenshot file '{image_path}' not found"
        except Exception as e:
            return f"Error analyzing screenshot: {str(e)}"
    
    def _cloud_unavailable_message(self) -> Dict:
        """Return cloud unavailable message"""
        return {
            "success": False,
            "message": "❌ Screenshot feature not available in cloud environment.\n\n💡 To use Advanced AI Screen Monitoring features, download and run this locally on your computer.\n\nThis powerful system can:\n🧠 Perform deep AI analysis\n🔍 Detect objects and UI elements\n🛡️ Scan for security issues\n⚡ Monitor performance\n🎨 Review UX/UI design\n♿ Check accessibility\n🤖 Find automation opportunities"
        }


def create_advanced_smart_screen_monitor():
    """Factory function to create advanced smart screen monitor"""
    return AdvancedSmartScreenMonitor()


if __name__ == "__main__":
    print("🚀 Advanced Smart Screen Monitor - Most Powerful Version")
    print("=" * 60)
    
    monitor = create_advanced_smart_screen_monitor()
    
    print("\n✨ Available Features:")
    print("• advanced_screen_analysis(mode) - Comprehensive AI analysis")
    print("• smart_object_detection(objects) - Find specific UI elements")
    print("• continuous_monitoring() - Real-time monitoring with triggers")
    print("• predictive_analysis() - Predict next actions")
    print("• advanced_comparison(mode) - Compare screenshots")
    print("• security_scan() - Deep security audit")
    print("• performance_audit() - Performance analysis")
    print("• ux_expert_review() - Professional UX review")
    print("• accessibility_audit() - Accessibility compliance")
    print("• code_review() - Expert code review")
    print("• design_critique() - Professional design critique")
    print("• find_automation_opportunities() - Discover automations")
    print("• intelligent_qa(question) - Ask anything about screen")
    print("• get_analytics_report() - View analytics")
    print("• export_activity_log() - Export all data")
