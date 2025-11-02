import json
import os
import re
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from typing import Dict, List, Any

# AI feature imports
try:
    from modules.ai_features.vision_ai import create_multimodal_ai, MultiModalInput
except ImportError:
    create_multimodal_ai = None
    MultiModalInput = None

try:
    from modules.intelligence.contextual_memory_enhanced import create_contextual_memory_enhanced
except ImportError:
    create_contextual_memory_enhanced = None

try:
    from modules.intelligence.correction_learning import create_correction_learning
except ImportError:
    create_correction_learning = None

try:
    from modules.intelligence.predictive_actions_engine import create_predictive_actions_engine
except ImportError:
    create_predictive_actions_engine = None

class AdvancedAIAutomation:
    def __init__(self):
        self.macros_file = "ai_macros.json"
        self.workflows_file = "visual_workflows.json"
        self.observed_patterns_file = "observed_patterns.json"
        self.macros = self.load_macros()
        self.workflows = self.load_workflows()
        self.observed_patterns = self.load_observed_patterns()

    def load_macros(self):
        """Load AI-generated macros"""
        if os.path.exists(self.macros_file):
            try:
                with open(self.macros_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_macros(self):
        """Save macros"""
        try:
            with open(self.macros_file, 'w') as f:
                json.dump(self.macros, f, indent=2)
        except Exception as e:
            print(f"Error saving macros: {e}")

    def load_workflows(self):
        """Load visual workflows"""
        if os.path.exists(self.workflows_file):
            try:
                with open(self.workflows_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_workflows(self):
        try:
            with open(self.workflows_file, 'w') as f:
                json.dump(self.workflows, f, indent=2)
        except Exception as e:
            print(f"Error saving workflows: {e}")

    def load_observed_patterns(self):
        if os.path.exists(self.observed_patterns_file):
            try:
                with open(self.observed_patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_observed_patterns(self):
        try:
            with open(self.observed_patterns_file, 'w') as f:
                json.dump(self.observed_patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving observed patterns: {e}")

    def summarize_email(self, email_content: str):
        lines = email_content.split('\n')

        summary = []

        for line in lines:
            line = line.strip()
            if line and len(line) > 20:
                if any(keyword in line.lower() for keyword in ['important', 'deadline', 'urgent', 'action required']):
                    summary.append(f"🔴 {line[:100]}")
                elif any(keyword in line.lower() for keyword in ['meeting', 'schedule', 'time']):
                    summary.append(f"📅 {line[:100]}")
                elif line.startswith('>') or line.startswith('On '):
                    continue
                else:
                    if len(summary) < 5:
                        summary.append(f"• {line[:100]}")

        output = "\n📧 EMAIL SUMMARY\n" + "="*60 + "\n"
        output += "\n".join(summary[:10])
        output += "\n" + "="*60 + "\n"

        return output

    def generate_document(self, doc_type: str, topic: str, details: Dict = None):
        if details is None:
            details = {}

        document = f"\n{'='*60}\n"

        if doc_type == "report":
            document += f"📄 REPORT: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            document += "Executive Summary:\n"
            document += f"This report covers {topic}.\n\n"
            document += "Key Findings:\n"
            document += "1. Finding one\n"
            document += "2. Finding two\n"
            document += "3. Finding three\n\n"
            document += "Recommendations:\n"
            document += "- Recommendation one\n"
            document += "- Recommendation two\n\n"

        elif doc_type == "meeting_summary":
            document += f"📝 MEETING SUMMARY: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            document += f"Attendees: {details.get('attendees', 'N/A')}\n\n"
            document += "Discussion Points:\n"
            document += "- Point 1\n"
            document += "- Point 2\n"
            document += "- Point 3\n\n"
            document += "Action Items:\n"
            document += "- [ ] Task 1\n"
            document += "- [ ] Task 2\n"
            document += "- [ ] Task 3\n\n"
            document += "Next Steps:\n"
            document += "Follow up on action items by [date]\n\n"

        elif doc_type == "notes":
            document += f"📓 NOTES: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            document += "Key Points:\n"
            document += "• Point 1\n"
            document += "• Point 2\n"
            document += "• Point 3\n\n"
            document += "Additional Information:\n"
            document += f"{details.get('content', 'Add your notes here...')}\n\n"

        document += f"{'='*60}\n"

        filename = f"{doc_type}_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            with open(filename, 'w') as f:
                f.write(document)
            return {"success": True, "message": f"Document created: {filename}", "content": document}
        except Exception as e:
            return {"success": False, "message": f"Error creating document: {e}", "content": document}

    def review_code(self, code: str, language: str = "python"):
        review = f"\n🔍 CODE REVIEW ({language.upper()})\n"
        review += "="*60 + "\n\n"

        lines = code.split('\n')

        review += "Issues Found:\n\n"

        if language.lower() == "python":
            if not any('def ' in line for line in lines):
                review += "⚠️ No functions detected - consider organizing code into functions\n"

            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 79]
            if long_lines:
                review += f"⚠️ Lines exceed 79 characters: {long_lines}\n"

            if 'import' in code and 'import *' in code:
                review += "🔴 Avoid wildcard imports (import *)\n"

        elif language.lower() == "javascript":
            if 'var ' in code:
                review += "⚠️ Consider using 'let' or 'const' instead of 'var'\n"

            if '==' in code:
                review += "⚠️ Consider using strict equality (===) instead of ==\n"

        review += "\nSuggestions:\n"
        review += "• Add docstrings/comments for complex logic\n"
        review += "• Consider error handling for edge cases\n"
        review += "• Use meaningful variable names\n"
        review += "• Keep functions focused on single responsibility\n"

        review += "\n" + "="*60 + "\n"

        return review

    def build_workflow(self, workflow_name: str, steps: List[Dict]):
        workflow = {
            "name": workflow_name,
            "created": datetime.now().isoformat(),
            "steps": steps,
            "enabled": True
        }

        self.workflows.append(workflow)
        self.save_workflows()

        return {"success": True, "message": f"Workflow '{workflow_name}' created with {len(steps)} steps"}

    def list_workflows(self):
        if not self.workflows:
            return "No workflows created yet."

        output = "\n" + "="*60 + "\n"
        output += "🔄 VISUAL WORKFLOWS\n"
        output += "="*60 + "\n\n"

        for i, workflow in enumerate(self.workflows, 1):
            status = "✅ Enabled" if workflow.get("enabled", True) else "❌ Disabled"
            output += f"{i}. {workflow['name']} - {status}\n"
            output += f"   Steps: {len(workflow.get('steps', []))}\n"
            output += f"   Created: {workflow.get('created', 'Unknown')}\n\n"

        output += "="*60 + "\n"
        return output

    def suggest_macro(self, repeated_actions: List[str]):
        if len(repeated_actions) < 3:
            return {"success": False, "message": "Need at least 3 repeated actions to suggest a macro"}

        macro_name = f"macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        macro = {
            "name": macro_name,
            "actions": repeated_actions,
            "frequency": len(repeated_actions),
            "suggested_at": datetime.now().isoformat(),
            "status": "suggested"
        }

        self.macros.append(macro)
        self.save_macros()

        return {
            "success": True,
            "message": f"Detected repeated pattern! Suggested macro: {macro_name}",
            "actions": repeated_actions,
            "suggestion": "Would you like to automate this sequence?"
        }

    def get_ai_connector_status(self):
        return {
            "success": True,
            "message": "AI App Connector ready",
            "supported_apps": ["Notion", "Google Calendar", "Trello", "Slack", "Discord"],
            "info": "Describe any integration in natural language to create it"
        }


def create_advanced_ai_automation():
    return AdvancedAIAutomation()


class AdvancedAIIntegration:
    def __init__(self, gui_instance):
        self.gui = gui_instance

        # Initialize Multi-Modal AI
        if create_multimodal_ai:
            try:
                self.multimodal_ai = create_multimodal_ai()
                print("✅ Multi-Modal AI initialized")
            except Exception as e:
                self.multimodal_ai = None
                print(f"⚠️ Multi-Modal AI initialization failed: {e}")
        else:
            self.multimodal_ai = None
            print("⚠️ Multi-Modal AI module not available")

        # Initialize Contextual Memory
        if create_contextual_memory_enhanced:
            try:
                self.contextual_memory = create_contextual_memory_enhanced()
                print("✅ Contextual Memory initialized")
            except Exception as e:
                self.contextual_memory = None
                print(f"⚠️ Contextual Memory initialization failed: {e}")
        else:
            self.contextual_memory = None
            print("⚠️ Contextual Memory module not available")

        # Initialize Correction Learning
        if create_correction_learning:
            try:
                self.correction_learning = create_correction_learning()
                print("✅ Correction Learning initialized")
            except Exception as e:
                self.correction_learning = None
                print(f"⚠️ Correction Learning initialization failed: {e}")
        else:
            self.correction_learning = None
            print("⚠️ Correction Learning module not available")

        # Initialize Predictive Engine
        if create_predictive_actions_engine:
            try:
                self.predictive_engine = create_predictive_actions_engine()
                print("✅ Predictive Engine initialized")
            except Exception as e:
                self.predictive_engine = None
                print(f"⚠️ Predictive Engine initialization failed: {e}")
        else:
            self.predictive_engine = None
            print("⚠️ Predictive Engine module not available")

    def append_output(self, text: str, tag: str = "info"):
        if not hasattr(self.gui, 'advanced_ai_output'):
            return

        self.gui.advanced_ai_output.config(state='normal')
        self.gui.advanced_ai_output.insert(tk.END, text, tag)
        self.gui.advanced_ai_output.see(tk.END)
        self.gui.advanced_ai_output.config(state='disabled')

    def analyze_screen(self):
        if not self.multimodal_ai:
            self.append_output("❌ Multi-Modal AI not available\n", "error")
            return

        self.append_output("\n🧠 Analyzing current screen...\n", "info")

        try:
            result = self.multimodal_ai.capture_and_analyze(
                text_or_voice="Analyze what's on my screen",
                is_voice=False,
                take_screenshot=True
            )

            if result.get("success"):
                response = self.multimodal_ai.get_context_aware_response(
                    MultiModalInput(
                        text="Analyze what's on my screen",
                        screenshot_path=result.get("screenshot_path")
                    )
                )
                self.append_output(f"{response}\n\n", "success")
            else:
                self.append_output(f"❌ Analysis failed: {result.get('message')}\n", "error")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def voice_vision_analysis(self):
        """Combined voice and vision analysis"""
        self.append_output("\n🎤👁️ Voice + Vision feature coming soon!\n", "info")
        self.append_output("This will combine voice commands with screen analysis.\n", "info")

    def mm_statistics(self):
        if not self.multimodal_ai:
            self.append_output("❌ Multi-Modal AI not available\n", "error")
            return

        self.append_output("\n📊 Multi-Modal AI Statistics\n", "info")

        try:
            stats = self.multimodal_ai.get_statistics()
            self.append_output(f"Total Interactions: {stats['total_interactions']}\n", "success")
            self.append_output(f"Modalities Used:\n", "info")
            for mod, count in stats['modalities_used'].items():
                self.append_output(f"  - {mod}: {count}\n", "success")
            self.append_output(f"Vision Usage: {stats['vision_usage_rate']:.1f}%\n", "success")
            self.append_output(f"Voice Usage: {stats['voice_usage_rate']:.1f}%\n\n", "success")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def remember_something(self):
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return

        content = simpledialog.askstring("Remember Something", "What should I remember?")
        if not content:
            return

        category = simpledialog.askstring("Category", "Category (general/preference/fact/pattern):", initialvalue="general")

        try:
            mem_id = self.contextual_memory.remember(content, category or "general", importance=0.7)
            self.append_output(f"\n📝 Remembered: {content}\n", "success")
            self.append_output(f"Category: {category}, ID: {mem_id[:8]}\n\n", "info")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def recall_memories(self):
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return

        query = simpledialog.askstring("Recall Memories", "Search for (leave empty for recent memories):")

        try:
            memories = self.contextual_memory.recall(query=query, limit=10)

            self.append_output(f"\n🔍 Found {len(memories)} memories\n\n", "info")

            for i, mem in enumerate(memories, 1):
                self.append_output(f"{i}. {mem.content}\n", "success")
                self.append_output(f"   Category: {mem.category}, Importance: {mem.importance:.2f}\n", "info")
                self.append_output(f"   Accessed: {mem.access_count} times\n\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def update_preferences(self):
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return

        pref_key = simpledialog.askstring("Preference Key", "Preference key (e.g., communication_style):")
        if not pref_key:
            return

        pref_value = simpledialog.askstring("Preference Value", f"Value for {pref_key}:")
        if not pref_value:
            return

        try:
            self.contextual_memory.update_preference(pref_key, pref_value)
            self.append_output(f"\n⚙️ Updated preference: {pref_key} = {pref_value}\n\n", "success")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def memory_statistics(self):
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return

        try:
            stats = self.contextual_memory.get_statistics()

            self.append_output("\n📊 Memory System Statistics\n\n", "info")
            self.append_output(f"Total Memories: {stats['total_memories']}\n", "success")
            self.append_output(f"Avg Importance: {stats['avg_importance']:.2f}\n", "success")
            self.append_output(f"Session Interactions: {stats['session_interactions']}\n", "success")
            self.append_output(f"Session Duration: {stats['session_duration_minutes']:.1f} minutes\n", "success")

            if stats['memories_by_category']:
                self.append_output(f"\nMemories by Category:\n", "info")
                for cat, count in stats['memories_by_category'].items():
                    self.append_output(f"  - {cat}: {count}\n", "success")

            self.append_output("\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def record_correction(self):
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return

        original = simpledialog.askstring("Original Response", "What was the original (incorrect) response?")
        if not original:
            return

        corrected = simpledialog.askstring("Corrected Response", "What should it have been?")
        if not corrected:
            return

        corr_type = simpledialog.askstring("Correction Type", "Type (command/response/action/general):", initialvalue="general")

        try:
            corr_id = self.correction_learning.record_correction(
                original_response=original,
                corrected_response=corrected,
                correction_type=corr_type or "general"
            )

            self.append_output(f"\n✏️ Correction Recorded\n", "success")
            self.append_output(f"ID: {corr_id}\n", "info")
            self.append_output(f"Type: {corr_type}\n\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def learning_report(self):
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return

        try:
            report = self.correction_learning.get_learning_report()

            self.append_output("\n📈 Learning Report\n\n", "info")

            if report.get('status'):
                self.append_output(f"{report['status']}\n\n", "warning")
                return

            self.append_output(f"Total Corrections: {report['total_corrections_all_time']}\n", "success")
            self.append_output(f"Recent (30 days): {report['recent_corrections_30_days']}\n", "success")
            self.append_output(f"Learning Velocity: {report['learning_velocity']}/day\n", "success")
            self.append_output(f"Improvement Rate: {report['improvement_rate']}%\n", "success")
            self.append_output(f"Patterns Learned: {report['patterns_learned']}\n", "success")

            if report.get('most_corrected_areas'):
                self.append_output(f"\nMost Corrected Areas:\n", "warning")
                for area in report['most_corrected_areas'][:5]:
                    self.append_output(f"  - {area['area']}: {area['count']} corrections\n", "warning")

            self.append_output("\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def apply_learning(self):
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return

        proposed = simpledialog.askstring("Proposed Response", "Enter a proposed response to improve:")
        if not proposed:
            return

        try:
            result = self.correction_learning.apply_learning(proposed)

            self.append_output("\n🎯 Learning Applied\n\n", "info")
            self.append_output(f"Corrections Applied: {result['corrections_applied']}\n", "success")

            if result['corrections_applied'] > 0:
                self.append_output(f"Improved Response:\n{result['improved_response']}\n\n", "success")
                self.append_output(f"Notes: {result['learning_notes']}\n\n", "info")
            else:
                self.append_output("No applicable corrections found.\n\n", "warning")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def get_predictions(self):
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return

        try:
            predictions = self.predictive_engine.predict_next_actions(max_predictions=5)

            self.append_output("\n🔮 Predicted Next Actions\n\n", "prediction")

            if not predictions:
                self.append_output("No predictions available yet. Use the system more to build patterns!\n\n", "info")
                return

            for i, pred in enumerate(predictions, 1):
                confidence_emoji = "🔴" if pred.confidence > 0.7 else "🟡" if pred.confidence > 0.4 else "🟢"
                self.append_output(f"{i}. {confidence_emoji} {pred.action}\n", "prediction")
                self.append_output(f"   Confidence: {pred.confidence*100:.0f}%\n", "info")
                self.append_output(f"   Reason: {pred.reasoning}\n\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def proactive_suggestions(self):
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return

        try:
            suggestions = self.predictive_engine.get_proactive_suggestions()

            self.append_output("\n💡 Proactive Suggestions\n\n", "prediction")

            if not suggestions:
                self.append_output("No suggestions at this time.\n\n", "info")
                return

            for i, sug in enumerate(suggestions, 1):
                self.append_output(f"{i}. {sug['emoji']} {sug['action']}\n", "prediction")
                self.append_output(f"   {sug['reason']} ({sug['confidence']}% confidence)\n\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def prediction_accuracy(self):
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return

        try:
            metrics = self.predictive_engine.get_accuracy_metrics()
            stats = self.predictive_engine.get_statistics()

            self.append_output("\n📊 Prediction Accuracy Metrics\n\n", "info")

            self.append_output(f"Total Predictions: {metrics['total_predictions']}\n", "success")
            self.append_output(f"Correct Predictions: {metrics['correct_predictions']}\n", "success")
            self.append_output(f"Accuracy: {metrics['accuracy']}%\n\n", "success")

            self.append_output(f"Actions Recorded: {stats['total_actions_recorded']}\n", "info")
            self.append_output(f"Unique Actions: {stats['unique_actions']}\n", "info")
            self.append_output(f"Sequences Learned: {stats['sequences_learned']}\n", "info")
            self.append_output(f"Time Patterns: {stats['time_patterns']}\n", "info")
            self.append_output(f"Context Patterns: {stats['context_patterns']}\n\n", "info")

        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")

    def clear_output(self):
        if hasattr(self.gui, 'advanced_ai_output'):
            self.gui.advanced_ai_output.config(state='normal')
            self.gui.advanced_ai_output.delete(1.0, tk.END)
            self.gui.advanced_ai_output.config(state='disabled')


def create_advanced_ai_integration(gui_instance):
    """Factory function"""
    return AdvancedAIIntegration(gui_instance)

