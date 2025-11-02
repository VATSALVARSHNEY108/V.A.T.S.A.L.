"""
Translation Service Module
Provides text translation between multiple languages
"""

import requests
import json

class TranslationService:
    def __init__(self):
        self.languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'nl': 'Dutch', 'pl': 'Polish', 'tr': 'Turkish', 'vi': 'Vietnamese',
            'th': 'Thai', 'id': 'Indonesian', 'sv': 'Swedish', 'da': 'Danish',
            'no': 'Norwegian', 'fi': 'Finnish', 'cs': 'Czech', 'el': 'Greek',
            'he': 'Hebrew', 'ro': 'Romanian', 'uk': 'Ukrainian', 'bg': 'Bulgarian'
        }
        
        self.common_phrases = {
            'hello': {'es': 'hola', 'fr': 'bonjour', 'de': 'hallo', 'it': 'ciao'},
            'goodbye': {'es': 'adiós', 'fr': 'au revoir', 'de': 'auf wiedersehen', 'it': 'arrivederci'},
            'thank you': {'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'it': 'grazie'},
            'please': {'es': 'por favor', 'fr': "s'il vous plaît", 'de': 'bitte', 'it': 'per favore'},
            'yes': {'es': 'sí', 'fr': 'oui', 'de': 'ja', 'it': 'sì'},
            'no': {'es': 'no', 'fr': 'non', 'de': 'nein', 'it': 'no'}
        }
    
    def translate(self, text, target_lang='es', source_lang='auto'):
        """Translate text to target language using free API"""
        try:
            if text.lower() in self.common_phrases:
                return self._translate_common_phrase(text.lower(), target_lang)
            
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                translation = ''.join([item[0] for item in result[0] if item[0]])
                
                source_name = self.languages.get(source_lang, source_lang)
                target_name = self.languages.get(target_lang, target_lang)
                
                return self._format_translation(text, translation, source_name, target_name)
            else:
                return f"Translation failed. Please check language codes."
                
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def detect_language(self, text):
        """Detect the language of given text"""
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'auto',
                'tl': 'en',
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                detected_lang = result[2] if len(result) > 2 else 'unknown'
                lang_name = self.languages.get(detected_lang, detected_lang)
                
                return f"🔍 Detected Language: {lang_name} ({detected_lang})"
            else:
                return "Could not detect language."
                
        except Exception as e:
            return f"Detection error: {str(e)}"
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        output = f"\n{'='*50}\n"
        output += "🌐 SUPPORTED LANGUAGES\n"
        output += f"{'='*50}\n\n"
        
        for code, name in sorted(self.languages.items(), key=lambda x: x[1]):
            output += f"  {code.upper()}: {name}\n"
        
        output += f"\n{'='*50}\n"
        output += f"Total: {len(self.languages)} languages\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _translate_common_phrase(self, phrase, target_lang):
        """Quick translation for common phrases"""
        if phrase in self.common_phrases and target_lang in self.common_phrases[phrase]:
            translation = self.common_phrases[phrase][target_lang]
            target_name = self.languages.get(target_lang, target_lang)
            
            return self._format_translation(phrase, translation, "English", target_name)
        else:
            return self.translate(phrase, target_lang)
    
    def _format_translation(self, original, translated, source, target):
        """Format translation output beautifully"""
        output = f"\n{'='*50}\n"
        output += f"🌐 TRANSLATION\n"
        output += f"{'='*50}\n\n"
        output += f"📝 Original ({source}):\n   {original}\n\n"
        output += f"✅ Translated ({target}):\n   {translated}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def translate_file(self, file_path, target_lang='es'):
        """Translate text from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.translate(text, target_lang)
            
        except Exception as e:
            return f"File translation error: {str(e)}"

if __name__ == "__main__":
    service = TranslationService()
    
    print("Testing Translation Service...")
    print(service.translate("Hello, how are you?", "es"))
    print(service.translate("I love programming", "fr"))
    print(service.detect_language("Bonjour, comment allez-vous?"))
    print(service.get_supported_languages())
