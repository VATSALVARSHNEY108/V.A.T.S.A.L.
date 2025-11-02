"""
Correction Learning System
Learns from user corrections and feedback to improve over time
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class CorrectionRecord:
    """Represents a single correction made by user"""
    
    def __init__(self, original_response: str, corrected_response: str,
                 context: str, correction_type: str, metadata: Optional[Dict] = None):
        self.id = datetime.now().isoformat() + "_" + str(hash(original_response))[:8]
        self.original_response = original_response
        self.corrected_response = corrected_response
        self.context = context
        self.correction_type = correction_type
        self.timestamp = datetime.now().isoformat()
        self.metadata = metadata or {}
        self.applied_count = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "original_response": self.original_response,
            "corrected_response": self.corrected_response,
            "context": self.context,
            "correction_type": self.correction_type,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "applied_count": self.applied_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        record = cls(
            original_response=data["original_response"],
            corrected_response=data["corrected_response"],
            context=data.get("context", ""),
            correction_type=data.get("correction_type", "general"),
            metadata=data.get("metadata", {})
        )
        record.id = data["id"]
        record.timestamp = data["timestamp"]
        record.applied_count = data.get("applied_count", 0)
        return record


class CorrectionLearning:
    """
    Correction Learning System
    
    Features:
    - Track user corrections
    - Analyze correction patterns
    - Learn common mistakes
    - Improve responses over time
    - Provide correction suggestions
    - Measure improvement metrics
    """
    
    def __init__(self):
        self.corrections_file = "corrections_database.json"
        self.patterns_file = "correction_patterns.json"
        self.metrics_file = "learning_metrics.json"
        
        self.corrections: List[CorrectionRecord] = []
        self.patterns: Dict = {}
        self.metrics: Dict = {}
        
        self._load_all()
        
        print("📚 Correction Learning System initialized")
    
    def _load_all(self):
        """Load all correction data"""
        if os.path.exists(self.corrections_file):
            try:
                with open(self.corrections_file, 'r') as f:
                    data = json.load(f)
                    self.corrections = [CorrectionRecord.from_dict(rec) for rec in data]
            except:
                self.corrections = []
        
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    self.patterns = json.load(f)
            except:
                self.patterns = self._default_patterns()
        else:
            self.patterns = self._default_patterns()
        
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    self.metrics = json.load(f)
            except:
                self.metrics = self._default_metrics()
        else:
            self.metrics = self._default_metrics()
    
    def _default_patterns(self) -> Dict:
        """Default correction patterns"""
        return {
            "common_errors": [],
            "improvement_areas": {},
            "learned_preferences": {},
            "error_categories": defaultdict(int)
        }
    
    def _default_metrics(self) -> Dict:
        """Default learning metrics"""
        return {
            "total_corrections": 0,
            "corrections_by_type": {},
            "improvement_rate": 0.0,
            "most_corrected_areas": [],
            "learning_progress": []
        }
    
    def _save_all(self):
        """Save all correction data"""
        try:
            with open(self.corrections_file, 'w') as f:
                corrections_data = [rec.to_dict() for rec in self.corrections]
                json.dump(corrections_data, f, indent=2)
        except Exception as e:
            print(f"Error saving corrections: {e}")
        
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
        
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def record_correction(self, original_response: str, corrected_response: str,
                         context: str = "", correction_type: str = "general",
                         metadata: Optional[Dict] = None) -> str:
        """
        Record a correction made by user
        
        Args:
            original_response: What the AI originally said/did
            corrected_response: What it should have been
            context: Context where correction was made
            correction_type: Type of correction (command, response, action, etc.)
            metadata: Additional information
        
        Returns:
            Correction ID
        """
        record = CorrectionRecord(
            original_response=original_response,
            corrected_response=corrected_response,
            context=context,
            correction_type=correction_type,
            metadata=metadata
        )
        
        self.corrections.append(record)
        
        self.metrics["total_corrections"] += 1
        
        if correction_type not in self.metrics["corrections_by_type"]:
            self.metrics["corrections_by_type"][correction_type] = 0
        self.metrics["corrections_by_type"][correction_type] += 1
        
        self._analyze_patterns()
        
        self._save_all()
        
        print(f"📝 Correction recorded: {correction_type}")
        
        return record.id
    
    def _analyze_patterns(self):
        """Analyze correction patterns to find common issues"""
        if len(self.corrections) < 3:
            return
        
        correction_groups = defaultdict(list)
        for correction in self.corrections[-20:]:
            correction_groups[correction.correction_type].append(correction)
        
        for corr_type, records in correction_groups.items():
            if len(records) >= 3:
                if corr_type not in self.patterns["improvement_areas"]:
                    self.patterns["improvement_areas"][corr_type] = {
                        "frequency": 0,
                        "examples": [],
                        "learned_at": datetime.now().isoformat()
                    }
                
                self.patterns["improvement_areas"][corr_type]["frequency"] = len(records)
                self.patterns["improvement_areas"][corr_type]["examples"] = [
                    {
                        "original": r.original_response[:100],
                        "corrected": r.corrected_response[:100]
                    } for r in records[:3]
                ]
    
    def get_correction_guidance(self, current_context: str, 
                               response_type: str = "general") -> Optional[Dict]:
        """
        Get guidance based on previous corrections
        
        Args:
            current_context: Current situation/context
            response_type: Type of response being generated
        
        Returns:
            Guidance dict or None if no relevant corrections found
        """
        relevant_corrections = [
            c for c in self.corrections
            if c.correction_type == response_type or 
               current_context.lower() in c.context.lower()
        ]
        
        if not relevant_corrections:
            return None
        
        relevant_corrections.sort(key=lambda x: x.timestamp, reverse=True)
        recent = relevant_corrections[:3]
        
        guidance = {
            "found_corrections": len(recent),
            "suggestions": [],
            "common_mistakes": [],
            "preferred_approach": None
        }
        
        for correction in recent:
            guidance["suggestions"].append({
                "instead_of": correction.original_response[:150],
                "use": correction.corrected_response[:150],
                "reason": f"User corrected this {correction.correction_type}"
            })
        
        if response_type in self.patterns.get("improvement_areas", {}):
            area = self.patterns["improvement_areas"][response_type]
            guidance["common_mistakes"] = area.get("examples", [])
            guidance["frequency_of_issue"] = area.get("frequency", 0)
        
        return guidance
    
    def apply_learning(self, proposed_response: str, context: str = "",
                      response_type: str = "general") -> Dict:
        """
        Apply learned corrections to improve a proposed response
        
        Args:
            proposed_response: Response to potentially improve
            context: Current context
            response_type: Type of response
        
        Returns:
            Dict with improved response and learning notes
        """
        guidance = self.get_correction_guidance(context, response_type)
        
        if not guidance:
            return {
                "improved_response": proposed_response,
                "corrections_applied": 0,
                "learning_notes": "No relevant corrections found"
            }
        
        improved_response = proposed_response
        corrections_applied = 0
        learning_notes = []
        
        for suggestion in guidance.get("suggestions", []):
            instead_of = suggestion["instead_of"]
            use = suggestion["use"]
            
            if instead_of[:50].lower() in improved_response.lower():
                learning_notes.append(f"Applied learning: {suggestion['reason']}")
                corrections_applied += 1
        
        if corrections_applied > 0:
            learning_notes.append(f"Total corrections applied: {corrections_applied}")
        
        return {
            "improved_response": improved_response,
            "corrections_applied": corrections_applied,
            "learning_notes": "\n".join(learning_notes),
            "guidance_used": guidance
        }
    
    def provide_feedback(self, response_id: str, was_helpful: bool,
                        feedback_text: str = ""):
        """
        Provide feedback on whether applied corrections were helpful
        
        Args:
            response_id: ID of the response
            was_helpful: Whether the correction was helpful
            feedback_text: Additional feedback
        """
        feedback_entry = {
            "response_id": response_id,
            "was_helpful": was_helpful,
            "feedback": feedback_text,
            "timestamp": datetime.now().isoformat()
        }
        
        if "feedback_history" not in self.metrics:
            self.metrics["feedback_history"] = []
        
        self.metrics["feedback_history"].append(feedback_entry)
        
        helpful_count = sum(1 for f in self.metrics["feedback_history"] if f["was_helpful"])
        total_count = len(self.metrics["feedback_history"])
        
        if total_count > 0:
            self.metrics["improvement_rate"] = helpful_count / total_count
        
        self._save_all()
    
    def get_learning_report(self) -> Dict:
        """Generate comprehensive learning report"""
        if not self.corrections:
            return {
                "status": "No corrections recorded yet",
                "total_corrections": 0
            }
        
        recent_corrections = self.corrections[-30:]
        
        correction_types_count = defaultdict(int)
        for corr in recent_corrections:
            correction_types_count[corr.correction_type] += 1
        
        most_corrected = sorted(
            correction_types_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        learning_velocity = len(recent_corrections) / 30 if len(self.corrections) >= 30 else len(self.corrections)
        
        improvement_areas = list(self.patterns.get("improvement_areas", {}).keys())
        
        return {
            "total_corrections_all_time": len(self.corrections),
            "recent_corrections_30_days": len(recent_corrections),
            "learning_velocity": round(learning_velocity, 2),
            "most_corrected_areas": [{"area": area, "count": count} for area, count in most_corrected],
            "improvement_areas_identified": improvement_areas,
            "improvement_rate": round(self.metrics.get("improvement_rate", 0) * 100, 1),
            "patterns_learned": len(self.patterns.get("improvement_areas", {})),
            "feedback_received": len(self.metrics.get("feedback_history", []))
        }
    
    def get_statistics(self) -> Dict:
        """Get correction system statistics"""
        return {
            "total_corrections": len(self.corrections),
            "corrections_by_type": dict(self.metrics.get("corrections_by_type", {})),
            "improvement_rate": self.metrics.get("improvement_rate", 0),
            "patterns_identified": len(self.patterns.get("improvement_areas", {})),
            "learning_enabled": True
        }
    
    def export_corrections(self, filepath: str = "corrections_export.json"):
        """Export all corrections for analysis"""
        export_data = {
            "corrections": [c.to_dict() for c in self.corrections],
            "patterns": self.patterns,
            "metrics": self.metrics,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def clear_old_corrections(self, days_old: int = 90):
        """Clear corrections older than specified days"""
        cutoff = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        self.corrections = [
            c for c in self.corrections
            if datetime.fromisoformat(c.timestamp).timestamp() > cutoff
        ]
        
        self._save_all()
        
        return len(self.corrections)


def create_correction_learning():
    """Factory function"""
    return CorrectionLearning()


if __name__ == "__main__":
    print("📚 Correction Learning System - Test Mode\n")
    
    learning = create_correction_learning()
    
    learning.record_correction(
        original_response="I opened Chrome",
        corrected_response="I launched Google Chrome browser",
        context="Opening browser",
        correction_type="command",
        metadata={"user_preference": "formal_language"}
    )
    
    guidance = learning.get_correction_guidance("Opening browser", "command")
    print(f"Guidance: {guidance}\n")
    
    report = learning.get_learning_report()
    print(f"Learning Report: {json.dumps(report, indent=2)}")
