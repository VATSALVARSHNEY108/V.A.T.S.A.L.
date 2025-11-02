"""
💬 Communication Enhancements Module
Advanced AI-powered communication features for messages, emails, and collaboration

Features:
1. Voice Message Transcription - Convert audio to text
2. Smart Reply Suggestions - Generate 3 quick reply options
3. Email Priority Ranker - Sort emails by importance
4. Auto Follow-Up Reminder - Track unanswered messages
5. Meeting Notes Auto-Sender - Send meeting summaries
6. AI Chat Summarizer - Summarize long threads
7. Multi-Language Auto Reply - Reply in recipient's language
8. Voice-to-Task Converter - Convert speech to tasks/events
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from gemini_controller import get_client
from google.genai import types


class CommunicationEnhancements:
    """Advanced communication enhancement features"""
    
    def __init__(self):
        """Initialize communication enhancements"""
        self.follow_ups_file = "follow_up_reminders.json"
        self.priority_cache_file = "email_priorities.json"
        self.chat_summaries_file = "chat_summaries.json"
        
        self.follow_ups = self._load_json(self.follow_ups_file, [])
        self.email_priorities = self._load_json(self.priority_cache_file, {})
        self.chat_summaries = self._load_json(self.chat_summaries_file, [])
        
        print("💬 Communication Enhancements initialized")
        print("   ✅ 8 advanced features ready")
    
    def _load_json(self, filename: str, default: Any) -> Any:
        """Load JSON file with default fallback"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filename: str, data: Any):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving {filename}: {e}")
    
    def transcribe_voice_message(self, audio_file_path: str = None, audio_url: str = None) -> Dict:
        """
        Feature 1: Voice Message Transcription (Framework/Stub)
        Convert WhatsApp/Telegram audio messages to text
        
        NOTE: This is a framework implementation. To enable full transcription:
        - Integrate with Google Speech-to-Text API, OpenAI Whisper, or similar
        - Add audio file download capability for URLs
        - Implement audio format conversion if needed
        
        Args:
            audio_file_path: Path to local audio file
            audio_url: URL to audio file (for WhatsApp/Telegram)
        
        Returns:
            Dict with transcription text and metadata (currently placeholder)
        """
        try:
            if not audio_file_path and not audio_url:
                return {
                    "success": False,
                    "message": "Please provide either audio file path or URL"
                }
            
            source = audio_file_path if audio_file_path else audio_url
            
            print(f"🎤 Voice transcription framework called for: {source}")
            print(f"⚠️  NOTE: This is a framework implementation.")
            print(f"   To enable: Integrate speech-to-text API (Google/Whisper/etc)")
            
            transcription_text = f"""[Voice Transcription Framework]

Source: {source}

⚠️ FRAMEWORK IMPLEMENTATION
This feature requires integration with a speech-to-text service.

To enable full functionality:
1. Add API credentials for speech-to-text service (Google Cloud Speech-to-Text, OpenAI Whisper, etc.)
2. Install required audio processing libraries
3. Implement audio download for URL sources
4. Add audio format validation and conversion

Current status: Framework ready for integration
"""
            
            result = {
                "success": True,
                "transcription": transcription_text,
                "source": source,
                "timestamp": datetime.now().isoformat(),
                "duration": "N/A",
                "language": "N/A",
                "confidence": 0.0,
                "framework_mode": True,
                "note": "Framework implementation - requires speech-to-text API integration"
            }
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Transcription error: {str(e)}"
            }
    
    def generate_smart_replies(self, message_data: Dict, context: str = "professional") -> Dict:
        """
        Feature 2: Smart Reply Suggestions
        Generate 3 quick reply options for any message or email
        
        Args:
            message_data: Dict with 'from', 'subject', 'body', 'platform'
            context: Reply context - 'professional', 'casual', 'friendly'
        
        Returns:
            Dict with 3 suggested replies
        """
        try:
            client = get_client()
            
            sender = message_data.get("from", "Unknown")
            subject = message_data.get("subject", "")
            body = message_data.get("body", "")
            platform = message_data.get("platform", "email")
            
            prompt = f"""You are an AI communication assistant. Generate exactly 3 different reply options for this message.

**Message Details:**
From: {sender}
Subject: {subject}
Platform: {platform}

**Message Content:**
{body}

**Context:** {context}

**Instructions:**
Generate 3 distinct reply options:
1. Short & Quick (1-2 sentences) - Brief acknowledgment
2. Detailed & Thoughtful (3-4 sentences) - Comprehensive response
3. Action-Oriented (2-3 sentences) - Clear next steps

Format your response as:
OPTION 1:
[short reply text]

OPTION 2:
[detailed reply text]

OPTION 3:
[action-oriented reply text]

Keep replies appropriate for {platform} and {context} tone."""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=800
                )
            )
            
            reply_text = response.text.strip()
            
            replies = self._parse_reply_options(reply_text)
            
            return {
                "success": True,
                "message": f"✅ Generated {len(replies)} smart reply options",
                "replies": replies,
                "original_message": {
                    "from": sender,
                    "subject": subject,
                    "preview": body[:100]
                },
                "context": context,
                "platform": platform
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating smart replies: {str(e)}",
                "replies": []
            }
    
    def _parse_reply_options(self, reply_text: str) -> List[Dict]:
        """Parse AI response into 3 reply options"""
        replies = []
        
        lines = reply_text.split('\n')
        current_option = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('OPTION'):
                if current_option and current_text:
                    replies.append({
                        "type": current_option,
                        "text": '\n'.join(current_text).strip()
                    })
                    current_text = []
                
                if '1' in line:
                    current_option = "short_quick"
                elif '2' in line:
                    current_option = "detailed_thoughtful"
                elif '3' in line:
                    current_option = "action_oriented"
            elif line and current_option:
                current_text.append(line)
        
        if current_option and current_text:
            replies.append({
                "type": current_option,
                "text": '\n'.join(current_text).strip()
            })
        
        if len(replies) < 3:
            replies = [
                {"type": "short_quick", "text": "Thanks for your message! I'll look into this."},
                {"type": "detailed_thoughtful", "text": "Thank you for reaching out. I've received your message and will review the details carefully. I'll get back to you with a comprehensive response soon."},
                {"type": "action_oriented", "text": "Got it! I'll take care of this right away and update you once it's done."}
            ]
        
        return replies[:3]
    
    def rank_emails_by_priority(self, emails: List[Dict]) -> Dict:
        """
        Feature 3: Email Priority Ranker
        Sort emails by real importance, not just sender
        
        Args:
            emails: List of email dicts with 'from', 'subject', 'body'
        
        Returns:
            Dict with ranked emails and priority scores
        """
        try:
            if not emails:
                return {
                    "success": False,
                    "message": "No emails provided for ranking"
                }
            
            print(f"📊 Analyzing priority for {len(emails)} emails...")
            
            ranked_emails = []
            
            for email in emails:
                priority_score = self._calculate_priority_score(email)
                
                ranked_email = {
                    **email,
                    "priority_score": priority_score["score"],
                    "priority_level": priority_score["level"],
                    "priority_reasons": priority_score["reasons"],
                    "urgency_keywords": priority_score["urgency_keywords"]
                }
                
                ranked_emails.append(ranked_email)
            
            ranked_emails.sort(key=lambda x: x["priority_score"], reverse=True)
            
            self._save_json(self.priority_cache_file, {
                "last_ranked": datetime.now().isoformat(),
                "email_count": len(ranked_emails)
            })
            
            return {
                "success": True,
                "message": f"✅ Ranked {len(ranked_emails)} emails by priority",
                "ranked_emails": ranked_emails,
                "summary": {
                    "critical": len([e for e in ranked_emails if e["priority_level"] == "Critical"]),
                    "high": len([e for e in ranked_emails if e["priority_level"] == "High"]),
                    "medium": len([e for e in ranked_emails if e["priority_level"] == "Medium"]),
                    "low": len([e for e in ranked_emails if e["priority_level"] == "Low"])
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error ranking emails: {str(e)}"
            }
    
    def _calculate_priority_score(self, email: Dict) -> Dict:
        """Calculate priority score for an email (0-100)"""
        score = 50
        reasons = []
        urgency_keywords = []
        
        subject = (email.get("subject", "") or "").lower()
        body = (email.get("body", "") or "").lower()
        sender = (email.get("from", "") or "").lower()
        combined_text = f"{subject} {body}"
        
        critical_keywords = ["urgent", "asap", "emergency", "critical", "immediately", "deadline today"]
        high_priority_keywords = ["important", "deadline", "required", "action needed", "please review", "time-sensitive"]
        question_keywords = ["?", "question", "clarify", "help", "assistance"]
        
        for keyword in critical_keywords:
            if keyword in combined_text:
                score += 15
                urgency_keywords.append(keyword)
                reasons.append(f"Critical keyword: '{keyword}'")
        
        for keyword in high_priority_keywords:
            if keyword in combined_text:
                score += 10
                urgency_keywords.append(keyword)
                reasons.append(f"High priority keyword: '{keyword}'")
        
        for keyword in question_keywords:
            if keyword in combined_text:
                score += 5
                reasons.append(f"Contains question or request")
                break
        
        if any(domain in sender for domain in ["@company.com", "@organization.com", "boss", "manager", "ceo"]):
            score += 15
            reasons.append("From important sender")
        
        word_count = len(body.split())
        if word_count < 50:
            score += 5
            reasons.append("Brief message (likely quick question)")
        elif word_count > 500:
            score -= 5
            reasons.append("Very long message")
        
        if subject.startswith("re:") or subject.startswith("fwd:"):
            score += 5
            reasons.append("Reply or forward (ongoing conversation)")
        
        score = max(0, min(100, score))
        
        if score >= 80:
            level = "Critical"
        elif score >= 65:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"
        
        return {
            "score": round(score, 1),
            "level": level,
            "reasons": reasons,
            "urgency_keywords": urgency_keywords
        }
    
    def add_follow_up_reminder(self, message_data: Dict, remind_in_days: int = 3) -> Dict:
        """
        Feature 4: Auto Follow-Up Reminder
        Reminds you to follow up on unanswered messages
        
        Args:
            message_data: Dict with message details
            remind_in_days: Days until reminder (default 3)
        
        Returns:
            Dict with reminder confirmation
        """
        try:
            reminder = {
                "id": f"reminder_{len(self.follow_ups) + 1}",
                "message": {
                    "from": message_data.get("from", "Unknown"),
                    "subject": message_data.get("subject", ""),
                    "body_preview": message_data.get("body", "")[:200],
                    "platform": message_data.get("platform", "email"),
                    "received_at": message_data.get("timestamp", datetime.now().isoformat())
                },
                "remind_at": (datetime.now() + timedelta(days=remind_in_days)).isoformat(),
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            self.follow_ups.append(reminder)
            self._save_json(self.follow_ups_file, self.follow_ups)
            
            return {
                "success": True,
                "message": f"✅ Follow-up reminder set for {remind_in_days} days",
                "reminder": reminder,
                "remind_date": (datetime.now() + timedelta(days=remind_in_days)).strftime("%Y-%m-%d %H:%M")
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error setting reminder: {str(e)}"
            }
    
    def check_follow_up_reminders(self) -> Dict:
        """Check for pending follow-up reminders"""
        try:
            now = datetime.now()
            due_reminders = []
            
            for reminder in self.follow_ups:
                if reminder["status"] == "pending":
                    remind_at = datetime.fromisoformat(reminder["remind_at"])
                    if remind_at <= now:
                        due_reminders.append(reminder)
            
            return {
                "success": True,
                "due_reminders": due_reminders,
                "total_pending": len([r for r in self.follow_ups if r["status"] == "pending"]),
                "message": f"📬 You have {len(due_reminders)} follow-up(s) due now"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error checking reminders: {str(e)}"
            }
    
    def mark_follow_up_complete(self, reminder_id: str) -> Dict:
        """Mark a follow-up reminder as complete"""
        try:
            for reminder in self.follow_ups:
                if reminder["id"] == reminder_id:
                    reminder["status"] = "completed"
                    reminder["completed_at"] = datetime.now().isoformat()
                    self._save_json(self.follow_ups_file, self.follow_ups)
                    return {
                        "success": True,
                        "message": "✅ Follow-up marked as complete"
                    }
            
            return {
                "success": False,
                "message": "Reminder not found"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    def send_meeting_notes(self, meeting_data: Dict, recipients: List[str]) -> Dict:
        """
        Feature 5: Meeting Notes Auto-Sender
        Automatically send meeting summaries to participants
        
        Args:
            meeting_data: Dict with meeting details
            recipients: List of email addresses
        
        Returns:
            Dict with send status
        """
        try:
            meeting_title = meeting_data.get("title", "Meeting")
            summary = meeting_data.get("summary", "")
            key_points = meeting_data.get("key_points", [])
            action_items = meeting_data.get("action_items", [])
            date = meeting_data.get("date", datetime.now().strftime("%Y-%m-%d"))
            
            email_body = f"""
📋 Meeting Notes: {meeting_title}
Date: {date}

{'='*60}

📝 SUMMARY:
{summary}

💡 KEY POINTS:
"""
            
            for i, point in enumerate(key_points, 1):
                email_body += f"{i}. {point}\n"
            
            email_body += f"\n✅ ACTION ITEMS:\n"
            
            for i, item in enumerate(action_items, 1):
                email_body += f"{i}. {item}\n"
            
            email_body += f"\n{'='*60}\n"
            email_body += f"Auto-generated by VATSAL AI Assistant\n"
            
            print(f"📧 Sending meeting notes to {len(recipients)} recipient(s)...")
            
            try:
                from email_sender import EmailSender
                email_sender = EmailSender()
                
                results = []
                for recipient in recipients:
                    result = email_sender.send_simple_email(
                        to=recipient,
                        subject=f"Meeting Notes: {meeting_title} - {date}",
                        message=email_body
                    )
                    results.append(result)
                
                successful = len([r for r in results if r.get("success")])
                
                return {
                    "success": successful > 0,
                    "message": f"✅ Meeting notes sent to {successful}/{len(recipients)} recipients",
                    "recipients": recipients,
                    "email_preview": email_body[:300]
                }
            
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Email sending not configured: {str(e)}",
                    "email_preview": email_body
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending meeting notes: {str(e)}"
            }
    
    def summarize_chat_thread(self, messages: List[Dict], platform: str = "Slack") -> Dict:
        """
        Feature 6: AI Chat Summarizer
        Summarize Slack/Discord/Teams threads
        
        Args:
            messages: List of message dicts with 'sender', 'text', 'timestamp'
            platform: Platform name (Slack, Discord, Teams)
        
        Returns:
            Dict with summary and key insights
        """
        try:
            if not messages:
                return {
                    "success": False,
                    "message": "No messages to summarize"
                }
            
            client = get_client()
            
            thread_text = ""
            for msg in messages:
                sender = msg.get("sender", "Unknown")
                text = msg.get("text", "")
                timestamp = msg.get("timestamp", "")
                thread_text += f"[{timestamp}] {sender}: {text}\n"
            
            prompt = f"""You are an AI assistant summarizing a {platform} chat thread.

**Thread Messages ({len(messages)} messages):**
{thread_text}

**Instructions:**
Create a comprehensive summary with:

1. **Main Topic**: What is this conversation about? (1-2 sentences)

2. **Key Decisions**: List any decisions made or conclusions reached

3. **Action Items**: List any tasks or action items mentioned

4. **Participants**: Who are the key contributors?

5. **Important Links/Resources**: Any URLs, files, or resources mentioned

6. **Next Steps**: What should happen next based on this conversation?

Format your response clearly with these sections."""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=1000
                )
            )
            
            summary = response.text.strip()
            
            summary_data = {
                "summary_id": f"summary_{len(self.chat_summaries) + 1}",
                "platform": platform,
                "message_count": len(messages),
                "summary": summary,
                "created_at": datetime.now().isoformat(),
                "thread_preview": thread_text[:200]
            }
            
            self.chat_summaries.append(summary_data)
            self._save_json(self.chat_summaries_file, self.chat_summaries)
            
            return {
                "success": True,
                "message": f"✅ Summarized {len(messages)} messages from {platform}",
                "summary": summary,
                "metadata": {
                    "platform": platform,
                    "message_count": len(messages),
                    "participants": len(set([msg.get("sender") for msg in messages]))
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error summarizing chat: {str(e)}"
            }
    
    def generate_multilingual_reply(self, message_data: Dict, detect_language: bool = True) -> Dict:
        """
        Feature 7: Multi-Language Auto Reply
        AI replies in the recipient's language
        
        Args:
            message_data: Dict with message details
            detect_language: Whether to auto-detect recipient's language
        
        Returns:
            Dict with reply in detected language
        """
        try:
            from translation_service import TranslationService
            translator = TranslationService()
            
            body = message_data.get("body", "")
            sender = message_data.get("from", "Unknown")
            
            detected_lang = "en"
            if detect_language and body:
                detection_result = translator.detect_language(body)
                
                if "(" in detection_result and ")" in detection_result:
                    detected_lang = detection_result.split("(")[1].split(")")[0]
            
            client = get_client()
            
            prompt = f"""Generate a professional reply to this message in {detected_lang} language.

**Original Message:**
{body}

**Instructions:**
- Write the reply in {detected_lang}
- Keep it professional and helpful
- Address the main points
- Keep it concise (2-3 sentences)

Generate ONLY the reply text in {detected_lang}."""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=400
                )
            )
            
            reply_text = response.text.strip()
            
            return {
                "success": True,
                "message": f"✅ Generated reply in {detected_lang}",
                "reply": reply_text,
                "detected_language": detected_lang,
                "original_message": body[:200],
                "sender": sender
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating multilingual reply: {str(e)}"
            }
    
    def convert_voice_to_task(self, voice_text: str, add_to_calendar: bool = True) -> Dict:
        """
        Feature 8: Voice-to-Task Converter
        Convert spoken messages into tasks or calendar events
        
        Args:
            voice_text: Transcribed voice message text
            add_to_calendar: Whether to add to calendar (if event detected)
        
        Returns:
            Dict with extracted task/event details
        """
        try:
            client = get_client()
            
            prompt = f"""You are an AI assistant that converts voice messages into actionable tasks or calendar events.

**Voice Message:**
"{voice_text}"

**Instructions:**
Analyze this voice message and determine if it's a:
1. TASK - Something to do (no specific date/time)
2. EVENT - Meeting, appointment, or scheduled activity (has date/time)

Extract:
- Type: task or event
- Title: Clear, concise title
- Description: Full details
- Priority: low, medium, high, urgent
- Due date/time: (if mentioned, format: YYYY-MM-DD HH:MM)
- Category: work, personal, meeting, reminder, etc.
- Action items: List of specific things to do

Format your response as JSON:
{{
  "type": "task" or "event",
  "title": "...",
  "description": "...",
  "priority": "...",
  "datetime": "YYYY-MM-DD HH:MM" or null,
  "category": "...",
  "action_items": ["...", "..."]
}}"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=500
                )
            )
            
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            try:
                extracted = json.loads(result_text)
            except:
                extracted = {
                    "type": "task",
                    "title": "Voice Task",
                    "description": voice_text,
                    "priority": "medium",
                    "datetime": None,
                    "category": "general",
                    "action_items": [voice_text]
                }
            
            if extracted.get("type") == "event" and add_to_calendar and extracted.get("datetime"):
                try:
                    from calendar_manager import CalendarManager
                    calendar = CalendarManager()
                    
                    event_datetime = extracted.get("datetime", "")
                    if event_datetime:
                        calendar.add_event(
                            title=extracted.get("title", "Voice Event"),
                            date=event_datetime.split()[0],
                            time=event_datetime.split()[1] if len(event_datetime.split()) > 1 else "09:00",
                            description=extracted.get("description", "")
                        )
                        extracted["added_to_calendar"] = True
                except:
                    extracted["added_to_calendar"] = False
            
            return {
                "success": True,
                "message": f"✅ Converted voice to {extracted.get('type', 'task')}",
                "extracted": extracted,
                "voice_text": voice_text
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error converting voice to task: {str(e)}"
            }
    
    def get_feature_summary(self) -> str:
        """Get summary of all communication enhancement features"""
        output = "\n" + "="*70 + "\n"
        output += "💬 COMMUNICATION ENHANCEMENTS - FEATURE SUMMARY\n"
        output += "="*70 + "\n\n"
        
        features = [
            ("1. Voice Message Transcription", "Convert WhatsApp/Telegram audio to text"),
            ("2. Smart Reply Suggestions", "Generate 3 quick reply options"),
            ("3. Email Priority Ranker", "Sort emails by real importance"),
            ("4. Auto Follow-Up Reminder", "Track unanswered messages"),
            ("5. Meeting Notes Auto-Sender", "Send meeting summaries automatically"),
            ("6. AI Chat Summarizer", "Summarize Slack/Discord/Teams threads"),
            ("7. Multi-Language Auto Reply", "Reply in recipient's language"),
            ("8. Voice-to-Task Converter", "Convert speech to tasks/events")
        ]
        
        for name, description in features:
            output += f"✅ {name}\n"
            output += f"   {description}\n\n"
        
        output += "="*70 + "\n"
        output += f"📊 Statistics:\n"
        output += f"   Follow-ups pending: {len([r for r in self.follow_ups if r['status'] == 'pending'])}\n"
        output += f"   Chat summaries saved: {len(self.chat_summaries)}\n"
        output += "="*70 + "\n"
        
        return output


def create_communication_enhancements():
    """Factory function to create CommunicationEnhancements instance"""
    return CommunicationEnhancements()
