"""
Web Tools Launcher
Launches and manages the In-One-Box Streamlit web app
Provides seamless integration with desktop automation
"""

import subprocess
import webbrowser
import time
import os
import platform
import psutil
import requests
from threading import Thread

class WebToolsLauncher:
    def __init__(self):
        self.streamlit_port = 8501
        self.process = None
        self.base_url = f"http://localhost:{self.streamlit_port}"
        
    def is_port_in_use(self, port):
        """Check if a port is already in use"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port and conn.status == 'LISTEN':
                    return True
        except (psutil.AccessDenied, PermissionError):
            # If we can't check ports, assume it's available
            pass
        return False
    
    def is_app_running(self):
        """Check if the Streamlit app is running"""
        try:
            response = requests.get(self.base_url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def launch_web_app(self):
        """Launch the In-One-Box Streamlit web app"""
        if self.is_app_running():
            return {
                "success": True,
                "message": "✅ Web Tools app is already running!",
                "url": self.base_url
            }
        
        try:
            # Check if app.py exists (In-One-Box main file)
            if not os.path.exists("app.py"):
                return {
                    "success": False,
                    "message": "❌ Web tools app not found.\n💡 Clone the In-One-Box repository to this directory:\n   git clone https://github.com/VATSALVARSHNEY108/In-One-Box-.git\n   Then move the files to the current directory."
                }
            
            # Launch Streamlit app in background
            # Redirect stdout/stderr to DEVNULL to prevent pipe deadlock
            if platform.system() == "Windows":
                self.process = subprocess.Popen(
                    ["streamlit", "run", "app.py", "--server.port", str(self.streamlit_port)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    ["streamlit", "run", "app.py", "--server.port", str(self.streamlit_port)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Wait for app to start
            print("  🚀 Starting web tools app...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.is_app_running():
                    print(f"  ✅ App started successfully!")
                    return {
                        "success": True,
                        "message": "✅ Web Tools app launched successfully!",
                        "url": self.base_url
                    }
            
            return {
                "success": False,
                "message": "⚠️ App started but not responding. Please check manually."
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "message": "❌ Streamlit not installed. Run: pip install streamlit"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error launching app: {str(e)}"
            }
    
    def open_web_tool(self, category, tool_name=None):
        """
        Open a specific tool category or tool in the web app
        
        Args:
            category: Tool category (e.g., "Text Tools", "Image Tools")
            tool_name: Specific tool name (optional)
        """
        # Launch app if not running
        if not self.is_app_running():
            result = self.launch_web_app()
            if not result["success"]:
                return result
            time.sleep(2)  # Give it a moment to fully load
        
        # Open browser to the app
        webbrowser.open(self.base_url)
        
        message = f"🌐 Opening {category}"
        if tool_name:
            message += f" - {tool_name}"
        
        return {
            "success": True,
            "message": f"{message}\n💡 Select the tool in your browser!",
            "url": self.base_url
        }
    
    def stop_web_app(self):
        """Stop the Streamlit web app"""
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5)
                return {
                    "success": True,
                    "message": "✅ Web Tools app stopped successfully!"
                }
            else:
                return {
                    "success": True,
                    "message": "⚠️ No app process found to stop."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error stopping app: {str(e)}"
            }
    
    def get_status(self):
        """Get the current status of the web app"""
        if self.is_app_running():
            return {
                "success": True,
                "message": f"✅ Web Tools app is running\n🌐 URL: {self.base_url}",
                "running": True,
                "url": self.base_url
            }
        else:
            return {
                "success": True,
                "message": "⚠️ Web Tools app is not running",
                "running": False
            }
    
    def list_available_tools(self):
        """List all available tool categories"""
        categories = {
            "🤖 AI Tools": [
                "Text Generation", "Image Analysis", "Content Creation", 
                "Language Translation", "Chatbot", "Code Helper"
            ],
            "🎵 Audio/Video Tools": [
                "Audio Converter", "Video Editor", "Format Converter",
                "Audio Trimmer", "Video Compressor"
            ],
            "💻 Coding Tools": [
                "Code Formatter", "Syntax Highlighter", "Minifier",
                "Regex Tester", "API Tester", "JSON Validator"
            ],
            "🌈 Color Tools": [
                "Color Picker", "Palette Generator", "Gradient Maker",
                "Color Converter", "Contrast Checker"
            ],
            "🎨 CSS Tools": [
                "CSS Generator", "Box Shadow", "Border Radius",
                "Flexbox Generator", "Grid Generator"
            ],
            "📊 Data Tools": [
                "CSV Converter", "JSON Editor", "XML Parser",
                "Data Validator", "SQL Formatter"
            ],
            "📁 File Tools": [
                "Format Converter", "File Compressor", "Bulk Renamer",
                "Duplicate Finder", "File Encryption"
            ],
            "🖼️ Image Tools": [
                "Image Converter", "Resizer", "Compressor",
                "Watermark", "Filter Effects", "Background Remover"
            ],
            "🧮 Science/Math Tools": [
                "Calculator", "Unit Converter", "Equation Solver",
                "Statistics Calculator", "Graph Plotter"
            ],
            "🔒 Security/Privacy Tools": [
                "Password Generator", "Hash Generator", "Encryptor",
                "Security Scanner", "VPN Checker"
            ],
            "📱 Social Media Tools": [
                "Post Scheduler", "Analytics", "Hashtag Generator",
                "Caption Creator", "Link Shortener"
            ],
            "📈 SEO/Marketing Tools": [
                "Keyword Research", "Meta Tag Generator", "Sitemap Creator",
                "Backlink Checker", "Domain Analyzer"
            ],
            "📝 Text Tools": [
                "Case Converter", "Word Counter", "Base64 Encoder",
                "Hash Generator", "QR Code Generator", "Lorem Ipsum"
            ],
            "🌐 Web Developer Tools": [
                "HTML Formatter", "CSS Minifier", "JavaScript Beautifier",
                "SEO Analyzer", "Performance Tester"
            ],
            "📰 News & Events Tools": [
                "News Aggregator", "RSS Reader", "Event Calendar",
                "Weather Forecast"
            ]
        }
        
        output = "\n" + "="*60 + "\n"
        output += "🛠️ AVAILABLE WEB TOOLS (500+ TOOLS)\n"
        output += "="*60 + "\n\n"
        
        for category, tools in categories.items():
            output += f"{category}\n"
            for tool in tools[:5]:  # Show first 5 tools
                output += f"  • {tool}\n"
            if len(tools) > 5:
                output += f"  • ...and {len(tools) - 5} more\n"
            output += "\n"
        
        output += "="*60 + "\n"
        output += "💡 Use commands like:\n"
        output += "   • 'open text tools'\n"
        output += "   • 'launch QR code generator'\n"
        output += "   • 'open image converter'\n"
        output += "="*60 + "\n"
        
        return {
            "success": True,
            "message": output,
            "categories": list(categories.keys())
        }

def create_web_tools_launcher():
    """Factory function to create WebToolsLauncher instance"""
    return WebToolsLauncher()
