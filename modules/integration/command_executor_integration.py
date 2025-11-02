"""
Command Executor Integration with Self-Operating Computer
Enables natural language commands to automatically trigger self-operating mode when appropriate
"""

import os
from typing import Dict, Any, Optional, Callable

try:
    from self_operating_integrations import SelfOperatingIntegrationHub, SmartTaskRouter
    from self_operating_coordinator import TaskCoordinator
except ImportError:
    SelfOperatingIntegrationHub = None
    SmartTaskRouter = None
    TaskCoordinator = None


class EnhancedCommandExecutor:
    """
    Enhanced command executor that intelligently routes commands
    to self-operating mode or traditional execution
    
    Features:
    - Analyzes command complexity and type
    - Routes visual/navigation tasks to self-operating mode
    - Routes structured commands to traditional execution
    - Learns from execution patterns
    - Provides unified interface for all commands
    """
    
    def __init__(self, base_executor: Optional[Any] = None):
        """
        Initialize enhanced command executor
        
        Args:
            base_executor: Original CommandExecutor instance
        """
        self.base_executor = base_executor
        
        # Initialize self-operating components
        self.integration_hub = None
        self.task_router = None
        self.coordinator = None
        
        if SelfOperatingIntegrationHub and SmartTaskRouter and TaskCoordinator:
            try:
                self.integration_hub = SelfOperatingIntegrationHub()
                self.task_router = SmartTaskRouter(self.integration_hub)
                self.coordinator = TaskCoordinator(self.integration_hub)
                print("✅ Enhanced Command Executor initialized with self-operating support")
            except Exception as e:
                print(f"⚠️ Self-operating components not available: {e}")
        
        # Execution mode settings
        self.auto_self_operating = False  # Auto-route to self-operating when appropriate
        self.prefer_self_operating = False  # Prefer self-operating over traditional
        
        # Statistics
        self.total_commands = 0
        self.self_operating_commands = 0
        self.traditional_commands = 0
    
    def execute(self, command_dict: dict) -> dict:
        """
        Execute command dict (wraps base executor's execute method)
        This maintains compatibility with existing code while adding smart routing
        
        Args:
            command_dict: Command dictionary from Gemini parser
            
        Returns:
            Execution result dict
        """
        # Extract command description for analysis
        command_desc = command_dict.get("description", "")
        
        # If auto mode is enabled and we have a description, analyze it
        if self.auto_self_operating and command_desc and self.should_use_self_operating(command_desc):
            # Convert to natural language and use self-operating
            self.total_commands += 1
            self.self_operating_commands += 1
            
            print(f"🎮 Auto-routing to self-operating mode: {command_desc}")
            
            try:
                result = self.coordinator.execute_goal(command_desc)
                
                if result.get("success", False):
                    return {
                        "success": True,
                        "message": f"✅ Self-operating mode completed task:\n{result.get('goal', '')}\n\nSteps completed: {result.get('completed_steps', 0)}/{result.get('total_steps', 0)}\nDuration: {result.get('duration_seconds', 0)}s"
                    }
                else:
                    # Fall back to traditional
                    print("⚠️ Self-operating failed, falling back to traditional execution")
                    return self._execute_traditional_dict(command_dict)
            except Exception as e:
                print(f"❌ Self-operating error: {e}, falling back to traditional")
                return self._execute_traditional_dict(command_dict)
        else:
            # Use traditional execution
            return self._execute_traditional_dict(command_dict)
    
    def _execute_traditional_dict(self, command_dict: dict) -> dict:
        """Execute command dict using base executor"""
        self.total_commands += 1
        self.traditional_commands += 1
        
        if self.base_executor:
            return self.base_executor.execute(command_dict)
        else:
            return {
                "success": False,
                "message": "Base executor not available"
            }
    
    def should_use_self_operating(self, command: str) -> bool:
        """
        Determine if command should use self-operating mode
        
        Args:
            command: User command
            
        Returns:
            True if self-operating is recommended
        """
        if not self.task_router:
            return False
        
        # Use task router's analysis
        return self.task_router.should_use_self_operating(command)
    
    def execute_command(self, command: str, force_mode: Optional[str] = None, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Execute command with intelligent routing
        
        Args:
            command: User command
            force_mode: Force execution mode ('self_operating' or 'traditional')
            progress_callback: Optional progress callback
            
        Returns:
            Execution result
        """
        self.total_commands += 1
        
        # Determine execution mode
        if force_mode == "self_operating":
            use_self_operating = True
        elif force_mode == "traditional":
            use_self_operating = False
        elif self.prefer_self_operating:
            use_self_operating = True
        elif self.auto_self_operating:
            use_self_operating = self.should_use_self_operating(command)
        else:
            use_self_operating = False
        
        print(f"\n{'='*60}")
        print(f"📝 Command: {command}")
        print(f"🔧 Execution Mode: {'Self-Operating' if use_self_operating else 'Traditional'}")
        print(f"{'='*60}")
        
        # Execute based on mode
        if use_self_operating and self.coordinator:
            self.self_operating_commands += 1
            return self._execute_with_self_operating(command, progress_callback)
        else:
            self.traditional_commands += 1
            return self._execute_traditional(command)
    
    def _execute_with_self_operating(self, command: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Execute command using self-operating mode"""
        print("🎮 Using Self-Operating Mode...")
        
        try:
            result = self.coordinator.execute_goal(command, progress_callback)
            
            return {
                "success": result.get("success", False),
                "mode": "self_operating",
                "output": result,
                "command": command
            }
        except Exception as e:
            print(f"❌ Self-operating execution failed: {e}")
            print("🔄 Falling back to traditional execution...")
            return self._execute_traditional(command)
    
    def _execute_traditional(self, command: str) -> Dict[str, Any]:
        """Execute command using traditional method"""
        print("⚙️ Using Traditional Execution...")
        
        if self.base_executor:
            try:
                # Use base executor's execute method
                result = self.base_executor.execute(command)
                return {
                    "success": True,
                    "mode": "traditional",
                    "output": result,
                    "command": command
                }
            except Exception as e:
                return {
                    "success": False,
                    "mode": "traditional",
                    "output": None,
                    "error": str(e),
                    "command": command
                }
        else:
            return {
                "success": False,
                "mode": "traditional",
                "output": "Base executor not available",
                "command": command
            }
    
    def enable_auto_self_operating(self):
        """Enable automatic routing to self-operating mode"""
        self.auto_self_operating = True
        print("✅ Auto self-operating mode ENABLED")
        print("   Commands will be analyzed and routed to self-operating mode when appropriate")
    
    def disable_auto_self_operating(self):
        """Disable automatic routing to self-operating mode"""
        self.auto_self_operating = False
        print("❌ Auto self-operating mode DISABLED")
        print("   All commands will use traditional execution")
    
    def set_prefer_self_operating(self, prefer: bool):
        """
        Set preference for self-operating mode
        
        Args:
            prefer: True to prefer self-operating, False for traditional
        """
        self.prefer_self_operating = prefer
        if prefer:
            print("✅ Self-operating mode is now PREFERRED")
        else:
            print("⚙️ Traditional mode is now preferred")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            "total_commands": self.total_commands,
            "self_operating_commands": self.self_operating_commands,
            "traditional_commands": self.traditional_commands,
            "self_operating_percentage": round(
                (self.self_operating_commands / self.total_commands * 100) if self.total_commands > 0 else 0,
                1
            ),
            "auto_mode_enabled": self.auto_self_operating,
            "prefer_self_operating": self.prefer_self_operating
        }
    
    def print_statistics(self):
        """Print execution statistics"""
        stats = self.get_statistics()
        print("\n📊 Command Execution Statistics:")
        print(f"   Total Commands: {stats['total_commands']}")
        print(f"   Self-Operating: {stats['self_operating_commands']} ({stats['self_operating_percentage']}%)")
        print(f"   Traditional: {stats['traditional_commands']}")
        print(f"   Auto Mode: {'✅ Enabled' if stats['auto_mode_enabled'] else '❌ Disabled'}")
        print(f"   Preference: {'Self-Operating' if stats['prefer_self_operating'] else 'Traditional'}")


class CommandInterceptor:
    """
    Intercepts commands before execution and provides recommendations
    Useful for GUI integration to show users which mode will be used
    """
    
    def __init__(self, enhanced_executor: EnhancedCommandExecutor):
        """Initialize with enhanced executor"""
        self.executor = enhanced_executor
    
    def analyze_command(self, command: str) -> Dict[str, Any]:
        """
        Analyze command and provide execution recommendation
        
        Args:
            command: User command
            
        Returns:
            Analysis with recommendation
        """
        if not self.executor.integration_hub:
            return {
                "command": command,
                "recommended_mode": "traditional",
                "confidence": 1.0,
                "reasoning": "Self-operating not available"
            }
        
        # Get analysis from integration hub
        analysis = self.executor.integration_hub.analyze_task_complexity(command)
        
        # Determine recommended mode
        if analysis["recommended_module"] == "self_operating":
            recommended_mode = "self_operating"
            confidence = 0.8 if analysis["is_visual_navigation"] else 0.6
        else:
            recommended_mode = "traditional"
            confidence = 0.7
        
        return {
            "command": command,
            "recommended_mode": recommended_mode,
            "confidence": confidence,
            "reasoning": analysis.get("reasoning", ""),
            "complexity": analysis.get("complexity", "medium"),
            "full_analysis": analysis
        }
    
    def get_mode_description(self, mode: str) -> str:
        """Get human-readable description of execution mode"""
        descriptions = {
            "self_operating": "🎮 AI Vision Mode - AI will view your screen and perform actions autonomously",
            "traditional": "⚙️ Traditional Mode - Direct command execution with predefined actions",
            "hybrid": "🔀 Hybrid Mode - Combination of self-operating and traditional execution"
        }
        return descriptions.get(mode, "Unknown mode")


def create_enhanced_executor(base_executor: Optional[Any] = None) -> EnhancedCommandExecutor:
    """
    Create enhanced command executor
    
    Args:
        base_executor: Optional base CommandExecutor instance
        
    Returns:
        Enhanced executor
    """
    return EnhancedCommandExecutor(base_executor)


# Convenience function for simple command execution
def execute_smart_command(command: str, prefer_self_operating: bool = False) -> Dict[str, Any]:
    """
    Execute command with smart routing
    
    Args:
        command: Command to execute
        prefer_self_operating: Prefer self-operating mode
        
    Returns:
        Execution result
    """
    executor = EnhancedCommandExecutor()
    executor.auto_self_operating = True
    executor.prefer_self_operating = prefer_self_operating
    return executor.execute_command(command)


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Enhanced Command Executor with Self-Operating Integration")
    print("=" * 70)
    
    executor = EnhancedCommandExecutor()
    executor.enable_auto_self_operating()
    
    print("\n✅ Enhanced executor ready!")
    print("Use executor.execute_command(command) to execute commands with smart routing\n")
    
    # Example commands
    test_commands = [
        "open notepad",
        "navigate to google.com and search for AI",
        "show system info"
    ]
    
    print("📋 Example Command Analysis:")
    interceptor = CommandInterceptor(executor)
    for cmd in test_commands:
        analysis = interceptor.analyze_command(cmd)
        print(f"\n   Command: {cmd}")
        print(f"   → Mode: {analysis['recommended_mode']}")
        print(f"   → Reasoning: {analysis['reasoning']}")
