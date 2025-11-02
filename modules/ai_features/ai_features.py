import os
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class AIFeatures:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

        self.conversation_history_file = "ai_conversations.json"
        self.conversation_history = self.load_conversation_history()

    def load_conversation_history(self) -> dict:
        if os.path.exists(self.conversation_history_file):
            try:
                with open(self.conversation_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_conversation_history(self):
        try:
            with open(self.conversation_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving conversation history: {e}")

    def get_client(self):
        if self.client is None:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not set")
            self.client = genai.Client(api_key=self.api_key)
        return self.client

    def conversational_ai(self, message: str, context: str = "general") -> str:
        try:
            client = self.get_client()

            if context not in self.conversation_history:
                self.conversation_history[context] = []

            self.conversation_history[context].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })

            history_context = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in self.conversation_history[context][-5:]
            ])

            prompt = f"""You are a helpful, friendly AI assistant. Respond naturally to the user's message.

Previous conversation:
{history_context}

User: {message}

Provide a helpful, conversational response:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            reply = response.text

            self.conversation_history[context].append({
                "role": "assistant",
                "content": reply,
                "timestamp": datetime.now().isoformat()
            })

            self.save_conversation_history()

            return reply

        except Exception as e:
            return f"Error in conversational AI: {str(e)}"

    def customer_service_bot(self, query: str, company_context: str = "") -> str:
        try:
            client = self.get_client()

            prompt = f"""You are a professional customer service representative.

Company Context: {company_context if company_context else "General customer service"}

Customer Query: {query}

Provide a helpful, professional, and empathetic response addressing the customer's concern:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in customer service bot: {str(e)}"

    def educational_assistant(self, topic: str, question: str, level: str = "intermediate") -> str:
        try:
            client = self.get_client()

            prompt = f"""You are an educational assistant helping students learn.

Topic: {topic}
Learning Level: {level}
Student Question: {question}

Provide a clear, educational explanation with examples. Break down complex concepts into simple terms:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in educational assistant: {str(e)}"

    def domain_expert(self, domain: str, question: str) -> str:
        """
        Domain Expert - Specialized knowledge in specific fields
        """
        try:
            client = self.get_client()

            prompt = f"""You are an expert in {domain}. Provide detailed, accurate information based on deep domain knowledge.

Question: {question}

Provide an expert-level response with specific details, facts, and insights:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in domain expert: {str(e)}"

    def story_writer(self, prompt: str, genre: str = "general", length: str = "medium") -> str:
        try:
            client = self.get_client()

            length_guide = {
                "short": "Write a brief story (200-300 words)",
                "medium": "Write a story (500-800 words)",
                "long": "Write a detailed story (1000-1500 words)"
            }

            instruction = f"""You are a creative story writer.

Genre: {genre}
Story Prompt: {prompt}

{length_guide.get(length, length_guide['medium'])}

Write an engaging, well-structured story:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=instruction
            )

            return response.text

        except Exception as e:
            return f"Error in story writer: {str(e)}"

    def content_creator(self, topic: str, content_type: str = "blog post", tone: str = "professional") -> str:
        try:
            client = self.get_client()

            prompt = f"""You are a skilled content creator.

Content Type: {content_type}
Topic: {topic}
Tone: {tone}

Create engaging, high-quality content for the specified type and tone:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in content creator: {str(e)}"

    def article_generator(self, title: str, keywords: Optional[List[str]] = None, word_count: int = 800) -> str:
        """
        Article Generator - Generate full articles
        """
        try:
            client = self.get_client()

            keywords_str = ", ".join(keywords) if keywords else "relevant keywords"

            prompt = f"""You are a professional article writer.

Article Title: {title}
Target Keywords: {keywords_str}
Target Word Count: {word_count} words

Write a well-researched, informative article with proper structure (introduction, body, conclusion):"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in article generator: {str(e)}"

    def copywriting_assistant(self, product: str, goal: str = "persuade") -> str:
        try:
            client = self.get_client()

            prompt = f"""You are an expert copywriter.

Product/Service: {product}
Goal: {goal}

Write compelling marketing copy that engages and converts. Include headlines, body copy, and call-to-action:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in copywriting assistant: {str(e)}"

    def technical_writer(self, topic: str, audience: str = "technical") -> str:
        try:
            client = self.get_client()

            prompt = f"""You are a technical writer creating clear, accurate documentation.

Topic: {topic}
Target Audience: {audience}

Write comprehensive technical documentation with clear explanations, examples, and proper structure:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in technical writer: {str(e)}"

    def text_translator(self, text: str, target_language: str, source_language: str = "auto") -> str:
        try:
            client = self.get_client()

            prompt = f"""Translate the following text to {target_language}.
{f'Source language: {source_language}' if source_language != 'auto' else 'Detect the source language automatically.'}

Text to translate:
{text}

Provide only the translation:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in text translator: {str(e)}"

    def sentiment_analysis(self, text: str) -> str:
        """
        Sentiment Analysis - Analyze emotional tone of text
        """
        try:
            client = self.get_client()

            prompt = f"""Analyze the sentiment of the following text and provide a detailed analysis.

Text: {text}

Provide:
1. Overall sentiment (positive/negative/neutral)
2. Sentiment score (-1.0 to 1.0)
3. Key emotions detected
4. Confidence level

Return the analysis in JSON format:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in sentiment analysis: {str(e)}"

    def text_summarizer(self, text: str, length: str = "medium") -> str:
        try:
            client = self.get_client()

            length_guide = {
                "brief": "1-2 sentences",
                "medium": "1 paragraph (3-5 sentences)",
                "detailed": "2-3 paragraphs with key points"
            }

            prompt = f"""Summarize the following text in {length_guide.get(length, length_guide['medium'])}.

Text:
{text}

Summary:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in text summarizer: {str(e)}"

    def language_detector(self, text: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Identify the language of the following text. Provide the language name and ISO code.

Text: {text}

Response format: Language Name (ISO Code) - Confidence Level"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in language detector: {str(e)}"

    def content_moderator(self, text: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Analyze the following text for content moderation.

Text: {text}

Check for:
1. Inappropriate language
2. Hate speech
3. Violence
4. Sensitive topics
5. Overall safety rating

Provide a moderation report in JSON format:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in content moderator: {str(e)}"

    def image_description_generator(self, concept: str, style: str = "realistic") -> str:
        try:
            client = self.get_client()

            prompt = f"""Create a detailed prompt for AI image generation.

Concept: {concept}
Style: {style}

Generate a comprehensive, detailed description that an AI image generator could use. Include:
- Main subject
- Style and mood
- Lighting and atmosphere
- Colors and composition
- Artistic details

Image generation prompt:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in image description generator: {str(e)}"

    def style_transfer_description(self, content: str, style: str) -> str:
        """
        Style Transfer - Generate descriptions for style transfer
        """
        try:
            client = self.get_client()

            prompt = f"""Create a detailed description for applying style transfer.

Content: {content}
Target Style: {style}

Describe how the content should be transformed in the specified style:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in style transfer: {str(e)}"

    def analyze_data_patterns(self, data_description: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Analyze the following data for patterns.

Data Description: {data_description}

Identify:
1. Key patterns and trends
2. Anomalies or outliers
3. Correlations
4. Insights and recommendations

Provide detailed analysis:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in pattern recognition: {str(e)}"

    def trend_analysis(self, data_description: str, time_period: str = "") -> str:
        """
        Trend Analysis - Analyze trends over time
        """
        try:
            client = self.get_client()

            prompt = f"""Perform trend analysis on the following data.

Data: {data_description}
{f'Time Period: {time_period}' if time_period else ''}

Analyze:
1. Overall trend direction
2. Significant changes
3. Seasonal patterns
4. Future predictions
5. Key insights

Provide comprehensive trend analysis:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in trend analysis: {str(e)}"

    def predictive_modeling(self, scenario: str, variables: Optional[List[str]] = None) -> str:
        try:
            client = self.get_client()

            vars_str = ", ".join(variables) if variables else "relevant variables"

            prompt = f"""Create a predictive model for the following scenario.

Scenario: {scenario}
Key Variables: {vars_str}

Provide:
1. Prediction methodology
2. Expected outcomes
3. Confidence levels
4. Risk factors
5. Recommendations

Detailed prediction:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in predictive modeling: {str(e)}"

    def data_insights(self, data_description: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Extract actionable insights from the following data.

Data: {data_description}

Provide:
1. Key findings
2. Actionable recommendations
3. Business implications
4. Next steps

Generate comprehensive insights:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in data insights: {str(e)}"

    def statistical_analysis(self, data_description: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Perform statistical analysis on the following data.

Data: {data_description}

Provide:
1. Descriptive statistics
2. Distribution analysis
3. Correlation analysis
4. Statistical significance
5. Interpretation

Detailed statistical analysis:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in statistical analysis: {str(e)}"

    def image_recognition_guide(self, image_description: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Provide guidance for image recognition task.

Image Description: {image_description}

Describe:
1. Objects that should be recognized
2. Key features to look for
3. Recognition approach
4. Expected results

Image recognition guidance:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in image recognition: {str(e)}"

    def object_detection_guide(self, scenario: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Create an object detection strategy.

Scenario: {scenario}

Provide:
1. Objects to detect
2. Detection criteria
3. Bounding box specifications
4. Confidence thresholds
5. Implementation approach

Object detection guide:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in object detection: {str(e)}"

    def scene_analysis_guide(self, scene_type: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Provide scene analysis guidance.

Scene Type: {scene_type}

Describe:
1. Key elements in the scene
2. Spatial relationships
3. Context and setting
4. Important details
5. Analysis approach

Scene analysis guide:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in scene analysis: {str(e)}"

    def generate_speech_text(self, topic: str, duration_minutes: int = 5, tone: str = "professional") -> str:
        try:
            client = self.get_client()

            prompt = f"""Create a speech script for text-to-speech synthesis.

Topic: {topic}
Duration: {duration_minutes} minutes
Tone: {tone}

Generate a natural-sounding script with:
1. Clear pronunciation
2. Appropriate pacing
3. Natural pauses
4. Engaging delivery

Speech script:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in speech text generation: {str(e)}"

    def audio_analysis_guide(self, audio_type: str) -> str:
        try:
            client = self.get_client()

            prompt = f"""Provide audio analysis guidance.

Audio Type: {audio_type}

Describe:
1. Key features to analyze
2. Analysis metrics
3. Quality assessment criteria
4. Expected patterns
5. Interpretation methods

Audio analysis guide:"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"Error in audio analysis: {str(e)}"

    def format_converter(self, input_format: str, output_format: str, file_description: str = "") -> str:
        """Audio/Video Conversion - Format Converter"""
        try:
            client = self.get_client()
            prompt = f"""Provide guidance for converting media from {input_format} to {output_format}.

File Description: {file_description if file_description else 'Media file'}

Explain:
1. Recommended conversion tools
2. Quality settings
3. Conversion process
4. Potential issues and solutions

Conversion guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in format converter: {str(e)}"

    def codec_transformer(self, source_codec: str, target_codec: str) -> str:
        try:
            client = self.get_client()
            prompt = f"""Explain how to transform media from {source_codec} codec to {target_codec} codec.

Include:
1. Codec compatibility
2. Quality implications
3. Best practices
4. Tools and commands

Codec transformation guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in codec transformer: {str(e)}"

    def quality_adjuster(self, media_type: str, target_quality: str) -> str:
        """Audio/Video Conversion - Quality Adjuster"""
        try:
            client = self.get_client()
            prompt = f"""Guide for adjusting {media_type} quality to {target_quality}.

Provide:
1. Quality parameters (bitrate, resolution, etc.)
2. Recommended settings
3. File size impact
4. Best tools

Quality adjustment guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in quality adjuster: {str(e)}"

    def batch_converter(self, conversion_task: str, file_count: int = 1) -> str:
        """Audio/Video Conversion - Batch Converter"""
        try:
            client = self.get_client()
            prompt = f"""Provide a batch conversion strategy for: {conversion_task}

Number of files: {file_count}

Include:
1. Batch processing approach
2. Automation scripts
3. Progress monitoring
4. Error handling

Batch conversion guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in batch converter: {str(e)}"

    def resolution_changer(self, current_resolution: str, target_resolution: str) -> str:
        """Audio/Video Conversion - Resolution Changer"""
        try:
            client = self.get_client()
            prompt = f"""Guide for changing video resolution from {current_resolution} to {target_resolution}.

Cover:
1. Aspect ratio considerations
2. Scaling algorithms
3. Quality preservation
4. Command line examples

Resolution change guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in resolution changer: {str(e)}"

    def media_trimmer(self, media_type: str, trim_specification: str) -> str:
        try:
            client = self.get_client()
            prompt = f"""Provide trimming guidance for {media_type}.

Trim specification: {trim_specification}

Include:
1. Precise timing methods
2. Tools for trimming
3. Lossless vs lossy trimming
4. Best practices

Trimming guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in media trimmer: {str(e)}"

    def media_splitter(self, split_criteria: str) -> str:
        """Audio/Video Editing - Splitter"""
        try:
            client = self.get_client()
            prompt = f"""Guide for splitting media files.

Split criteria: {split_criteria}

Explain:
1. Splitting methods
2. Maintaining quality
3. File organization
4. Automation options

Splitting guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in media splitter: {str(e)}"

    def media_merger(self, merge_description: str) -> str:
        """Audio/Video Editing - Merger"""
        try:
            client = self.get_client()
            prompt = f"""Provide guidance for merging media files.

Merge task: {merge_description}

Cover:
1. Format compatibility
2. Transition handling
3. Quality preservation
4. Tools and commands

Merging guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in media merger: {str(e)}"

    def volume_adjuster(self, adjustment_type: str) -> str:
        """Audio/Video Editing - Volume Adjuster"""
        try:
            client = self.get_client()
            prompt = f"""Guide for audio volume adjustment.

Adjustment: {adjustment_type}

Include:
1. Volume normalization
2. Preventing distortion
3. Batch processing
4. Tools and techniques

Volume adjustment guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in volume adjuster: {str(e)}"

    def speed_controller(self, speed_change: str) -> str:
        """Audio/Video Editing - Speed Controller"""
        try:
            client = self.get_client()
            prompt = f"""Provide guidance for controlling playback speed.

Speed modification: {speed_change}

Explain:
1. Speed adjustment methods
2. Pitch preservation
3. Quality impact
4. Use cases and tools

Speed control guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in speed controller: {str(e)}"

    def size_optimizer(self, target_size: str, media_type: str) -> str:
        """Audio/Video Compression - Size Optimizer"""
        try:
            client = self.get_client()
            prompt = f"""Guide for optimizing {media_type} file size to {target_size}.

Include:
1. Compression strategies
2. Quality trade-offs
3. Recommended settings
4. Tools for optimization

Size optimization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in size optimizer: {str(e)}"

    def bitrate_adjuster(self, bitrate_target: str) -> str:
        """Audio/Video Compression - Bitrate Adjuster"""
        try:
            client = self.get_client()
            prompt = f"""Provide bitrate adjustment guidance.

Target bitrate: {bitrate_target}

Cover:
1. Bitrate selection
2. Quality implications
3. Variable vs constant bitrate
4. Best practices

Bitrate adjustment guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in bitrate adjuster: {str(e)}"

    def quality_compressor(self, compression_level: str) -> str:
        """Audio/Video Compression - Quality Compressor"""
        try:
            client = self.get_client()
            prompt = f"""Guide for quality-based compression.

Compression level: {compression_level}

Explain:
1. Compression algorithms
2. Quality metrics
3. Perceptual vs mathematical quality
4. Tools and settings

Quality compression guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in quality compressor: {str(e)}"

    def batch_compression(self, compression_task: str) -> str:
        """Audio/Video Compression - Batch Compression"""
        try:
            client = self.get_client()
            prompt = f"""Batch compression strategy.

Task: {compression_task}

Include:
1. Automated workflow
2. Consistent quality
3. Progress monitoring
4. Script examples

Batch compression guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in batch compression: {str(e)}"

    def format_specific_compression(self, format_name: str) -> str:
        try:
            client = self.get_client()
            prompt = f"""Format-specific compression guide for {format_name}.

Provide:
1. Format characteristics
2. Optimal compression settings
3. Codec recommendations
4. Best practices

Compression guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in format-specific compression: {str(e)}"

    def metadata_extractor(self, file_type: str) -> str:
        """Audio/Video Analysis - Metadata Extractor"""
        try:
            client = self.get_client()
            prompt = f"""Guide for extracting metadata from {file_type} files.

Cover:
1. Metadata types
2. Extraction tools
3. Parsing methods
4. Common metadata fields

Metadata extraction guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in metadata extractor: {str(e)}"

    def format_detector(self, detection_task: str) -> str:
        """Audio/Video Analysis - Format Detector"""
        try:
            client = self.get_client()
            prompt = f"""Format detection guidance.

Task: {detection_task}

Include:
1. Detection methods
2. File signature analysis
3. Container vs codec detection
4. Tools and commands

Format detection guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in format detector: {str(e)}"

    def quality_analyzer(self, analysis_type: str) -> str:
        """Audio/Video Analysis - Quality Analyzer"""
        try:
            client = self.get_client()
            prompt = f"""Quality analysis guidance.

Analysis type: {analysis_type}

Explain:
1. Quality metrics
2. Analysis tools
3. Interpretation of results
4. Objective vs subjective quality

Quality analysis guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in quality analyzer: {str(e)}"

    def duration_calculator(self, calculation_task: str) -> str:
        try:
            client = self.get_client()
            prompt = f"""Duration calculation guidance.

Task: {calculation_task}

Include:
1. Duration extraction methods
2. Frame-accurate timing
3. Batch duration calculation
4. Tools and scripts

Duration calculation guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in duration calculator: {str(e)}"

    def codec_identifier(self, identification_task: str) -> str:
        """Audio/Video Analysis - Codec Identifier"""
        try:
            client = self.get_client()
            prompt = f"""Codec identification guidance.

Task: {identification_task}

Cover:
1. Codec detection methods
2. Audio vs video codecs
3. Identification tools
4. Profile and level detection

Codec identification guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in codec identifier: {str(e)}"

    def stream_configuration(self, platform: str, stream_type: str) -> str:
        """Streaming Tools - Stream Configuration"""
        try:
            client = self.get_client()
            prompt = f"""Stream configuration for {platform}.

Stream type: {stream_type}

Provide:
1. Platform-specific settings
2. Encoder configuration
3. Network requirements
4. Best practices

Stream configuration guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in stream configuration: {str(e)}"

    def broadcast_settings(self, broadcast_type: str) -> str:
        """Streaming Tools - Broadcast Settings"""
        try:
            client = self.get_client()
            prompt = f"""Broadcast settings optimization.

Type: {broadcast_type}

Include:
1. Resolution and framerate
2. Bitrate recommendations
3. Audio settings
4. Latency optimization

Broadcast settings guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in broadcast settings: {str(e)}"

    def encoding_optimizer(self, encoding_scenario: str) -> str:
        """Streaming Tools - Encoding Optimizer"""
        try:
            client = self.get_client()
            prompt = f"""Encoding optimization for streaming.

Scenario: {encoding_scenario}

Cover:
1. Encoding presets
2. Hardware vs software encoding
3. Quality/performance balance
4. Multi-bitrate streaming

Encoding optimization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in encoding optimizer: {str(e)}"

    def quality_settings(self, target_quality: str, use_case: str = "") -> str:
        """Streaming Tools - Quality Settings"""
        try:
            client = self.get_client()
            prompt = f"""Quality settings for streaming.

Target: {target_quality}
{f'Use case: {use_case}' if use_case else ''}

Explain:
1. Quality parameters
2. Adaptive bitrate
3. Bandwidth optimization
4. Platform requirements

Quality settings guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in quality settings: {str(e)}"

    def platform_optimizer(self, platform_name: str) -> str:
        """Streaming Tools - Platform Optimizer"""
        try:
            client = self.get_client()
            prompt = f"""Platform-specific streaming optimization for {platform_name}.

Provide:
1. Platform requirements
2. Optimal encoder settings
3. Resolution/bitrate recommendations
4. Special considerations

Platform optimization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in platform optimizer: {str(e)}"

    def subtitle_editor(self, editing_task: str) -> str:
        """Subtitle Tools - Subtitle Editor"""
        try:
            client = self.get_client()
            prompt = f"""Subtitle editing guidance.

Task: {editing_task}

Include:
1. Subtitle formats
2. Editing tools
3. Timing adjustment
4. Text formatting

Subtitle editing guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in subtitle editor: {str(e)}"

    def timing_adjuster(self, adjustment_needed: str) -> str:
        """Subtitle Tools - Timing Adjuster"""
        try:
            client = self.get_client()
            prompt = f"""Subtitle timing adjustment.

Adjustment: {adjustment_needed}

Cover:
1. Timing correction methods
2. Synchronization techniques
3. Tools for adjustment
4. Batch timing fixes

Timing adjustment guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in timing adjuster: {str(e)}"

    def subtitle_format_converter(self, from_format: str, to_format: str) -> str:
        """Subtitle Tools - Format Converter"""
        try:
            client = self.get_client()
            prompt = f"""Convert subtitles from {from_format} to {to_format}.

Explain:
1. Format differences
2. Conversion process
3. Data preservation
4. Tools and scripts

Subtitle format conversion guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in subtitle format converter: {str(e)}"

    def subtitle_generator(self, generation_method: str) -> str:
        """Subtitle Tools - Subtitle Generator"""
        try:
            client = self.get_client()
            prompt = f"""Subtitle generation guidance.

Method: {generation_method}

Include:
1. Auto-generation options
2. Speech recognition integration
3. Manual creation tips
4. Quality improvement

Subtitle generation guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in subtitle generator: {str(e)}"

    def subtitle_synchronizer(self, sync_task: str) -> str:
        """Subtitle Tools - Synchronizer"""
        try:
            client = self.get_client()
            prompt = f"""Subtitle synchronization guidance.

Task: {sync_task}

Cover:
1. Sync detection
2. Automatic adjustment
3. Manual fine-tuning
4. Tools and techniques

Subtitle synchronization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in subtitle synchronizer: {str(e)}"

    def tag_editor(self, tag_operation: str) -> str:
        """Metadata Editors - Tag Editor"""
        try:
            client = self.get_client()
            prompt = f"""Tag editing guidance.

Operation: {tag_operation}

Include:
1. Tag types and standards
2. Editing tools
3. Batch operations
4. Best practices

Tag editing guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in tag editor: {str(e)}"

    def cover_art_manager(self, art_task: str) -> str:
        """Metadata Editors - Cover Art Manager"""
        try:
            client = self.get_client()
            prompt = f"""Cover art management.

Task: {art_task}

Cover:
1. Image format requirements
2. Embedding methods
3. Extraction and replacement
4. Tools and automation

Cover art management guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in cover art manager: {str(e)}"

    def information_extractor(self, extraction_target: str) -> str:
        """Metadata Editors - Information Extractor"""
        try:
            client = self.get_client()
            prompt = f"""Media information extraction.

Target: {extraction_target}

Explain:
1. Information types
2. Extraction methods
3. Parsing tools
4. Data organization

Information extraction guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in information extractor: {str(e)}"

    def metadata_batch_editor(self, batch_task: str) -> str:
        """Metadata Editors - Batch Editor"""
        try:
            client = self.get_client()
            prompt = f"""Batch metadata editing.

Task: {batch_task}

Include:
1. Batch processing workflow
2. Template application
3. Error handling
4. Automation scripts

Batch editing guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in batch editor: {str(e)}"

    def id3_editor(self, id3_operation: str) -> str:
        """Metadata Editors - ID3 Editor"""
        try:
            client = self.get_client()
            prompt = f"""ID3 tag editing guidance.

Operation: {id3_operation}

Cover:
1. ID3 versions
2. Tag fields
3. Editing tools
4. Best practices

ID3 editing guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in ID3 editor: {str(e)}"

    def noise_reduction(self, noise_type: str) -> str:
        """Audio Enhancement - Noise Reduction"""
        try:
            client = self.get_client()
            prompt = f"""Noise reduction for audio.

Noise type: {noise_type}

Provide:
1. Noise identification
2. Reduction techniques
3. Tools and plugins
4. Quality preservation

Noise reduction guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in noise reduction: {str(e)}"

    def audio_equalizer(self, eq_goal: str) -> str:
        """Audio Enhancement - Equalizer"""
        try:
            client = self.get_client()
            prompt = f"""Audio equalization guidance.

Goal: {eq_goal}

Include:
1. EQ fundamentals
2. Frequency adjustments
3. Tools and presets
4. Best practices

Equalization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in audio equalizer: {str(e)}"

    def audio_normalizer(self, normalization_type: str) -> str:
        """Audio Enhancement - Normalizer"""
        try:
            client = self.get_client()
            prompt = f"""Audio normalization guidance.

Type: {normalization_type}

Cover:
1. Normalization methods
2. Peak vs RMS normalization
3. Loudness standards
4. Tools and processes

Normalization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in audio normalizer: {str(e)}"

    def audio_amplifier(self, amplification_goal: str) -> str:
        """Audio Enhancement - Amplifier"""
        try:
            client = self.get_client()
            prompt = f"""Audio amplification guidance.

Goal: {amplification_goal}

Explain:
1. Safe amplification
2. Clipping prevention
3. Dynamic range
4. Tools and techniques

Amplification guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in audio amplifier: {str(e)}"

    def echo_remover(self, echo_scenario: str) -> str:
        """Audio Enhancement - Echo Remover"""
        try:
            client = self.get_client()
            prompt = f"""Echo removal guidance.

Scenario: {echo_scenario}

Include:
1. Echo detection
2. Removal techniques
3. Tools and plugins
4. Quality preservation

Echo removal guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in echo remover: {str(e)}"

    def video_stabilizer(self, stabilization_task: str) -> str:
        """Video Enhancement - Stabilizer"""
        try:
            client = self.get_client()
            prompt = f"""Video stabilization guidance.

Task: {stabilization_task}

Cover:
1. Stabilization algorithms
2. Crop considerations
3. Tools and software
4. Post-processing

Video stabilization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in video stabilizer: {str(e)}"

    def color_corrector(self, correction_goal: str) -> str:
        """Video Enhancement - Color Corrector"""
        try:
            client = self.get_client()
            prompt = f"""Color correction guidance.

Goal: {correction_goal}

Provide:
1. Color theory basics
2. Correction vs grading
3. Tools and workflows
4. LUT application

Color correction guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in color corrector: {str(e)}"

    def brightness_adjuster(self, adjustment_task: str) -> str:
        """Video Enhancement - Brightness Adjuster"""
        try:
            client = self.get_client()
            prompt = f"""Brightness adjustment guidance.

Task: {adjustment_task}

Include:
1. Brightness vs exposure
2. Histogram analysis
3. Tools and techniques
4. Maintaining detail

Brightness adjustment guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in brightness adjuster: {str(e)}"

    def contrast_enhancer(self, enhancement_goal: str) -> str:
        """Video Enhancement - Contrast Enhancer"""
        try:
            client = self.get_client()
            prompt = f"""Contrast enhancement guidance.

Goal: {enhancement_goal}

Explain:
1. Contrast principles
2. Dynamic range
3. Tools and filters
4. Avoiding artifacts

Contrast enhancement guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in contrast enhancer: {str(e)}"

    def frame_rate_converter(self, conversion_spec: str) -> str:
        """Video Enhancement - Frame Rate Converter"""
        try:
            client = self.get_client()
            prompt = f"""Frame rate conversion guidance.

Conversion: {conversion_spec}

Cover:
1. Frame rate basics
2. Interpolation methods
3. Motion smoothness
4. Tools and settings

Frame rate conversion guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in frame rate converter: {str(e)}"

    def playlist_creator(self, playlist_type: str) -> str:
        """Media Utilities - Playlist Creator"""
        try:
            client = self.get_client()
            prompt = f"""Playlist creation guidance.

Type: {playlist_type}

Include:
1. Playlist formats
2. Creation methods
3. Organization strategies
4. Tools and automation

Playlist creation guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in playlist creator: {str(e)}"

    def media_organizer(self, organization_task: str) -> str:
        """Media Utilities - Media Organizer"""
        try:
            client = self.get_client()
            prompt = f"""Media organization guidance.

Task: {organization_task}

Cover:
1. Folder structures
2. Naming conventions
3. Metadata-based organization
4. Automation scripts

Media organization guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in media organizer: {str(e)}"

    def media_batch_processor(self, processing_task: str) -> str:
        """Media Utilities - Batch Processor"""
        try:
            client = self.get_client()
            prompt = f"""Batch media processing guidance.

Task: {processing_task}

Provide:
1. Workflow design
2. Automation tools
3. Error handling
4. Progress monitoring

Batch processing guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in batch processor: {str(e)}"

    def media_file_renamer(self, renaming_pattern: str) -> str:
        """Media Utilities - File Renamer"""
        try:
            client = self.get_client()
            prompt = f"""Media file renaming guidance.

Pattern: {renaming_pattern}

Include:
1. Naming conventions
2. Pattern matching
3. Batch renaming
4. Tools and scripts

File renaming guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in file renamer: {str(e)}"

    def media_duplicate_finder(self, search_criteria: str) -> str:
        try:
            client = self.get_client()
            prompt = f"""Media duplicate finding guidance.

Criteria: {search_criteria}

Cover:
1. Detection methods
2. Comparison algorithms
3. Hash-based vs content-based
4. Tools and automation

Duplicate finding guide:"""
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return response.text
        except Exception as e:
            return f"Error in duplicate finder: {str(e)}"

    def list_ai_features(self) -> dict:
        return {
            "Chatbots": [
                "conversational_ai - General purpose conversational AI",
                "customer_service_bot - Customer support assistant",
                "educational_assistant - Learning and education help",
                "domain_expert - Specialized domain knowledge"
            ],
            "Text Generation": [
                "story_writer - Create creative stories",
                "content_creator - Generate various content types",
                "article_generator - Write full articles",
                "copywriting_assistant - Marketing copy creation",
                "technical_writer - Technical documentation"
            ],
            "Language Processing": [
                "text_translator - Translate between languages",
                "sentiment_analysis - Analyze emotional tone",
                "text_summarizer - Summarize long text",
                "language_detector - Identify language",
                "content_moderator - Content safety checking"
            ],
            "Image Generation": [
                "image_description_generator - AI art prompts",
                "style_transfer_description - Style transfer guidance"
            ],
            "Data Analysis": [
                "analyze_data_patterns - Pattern recognition",
                "trend_analysis - Analyze trends over time",
                "predictive_modeling - Make predictions",
                "data_insights - Extract actionable insights",
                "statistical_analysis - Statistical analysis"
            ],
            "Computer Vision": [
                "image_recognition_guide - Image recognition guidance",
                "object_detection_guide - Object detection strategies",
                "scene_analysis_guide - Scene understanding"
            ],
            "Voice & Audio": [
                "generate_speech_text - Speech synthesis scripts",
                "audio_analysis_guide - Audio analysis guidance"
            ],
            "Audio/Video Conversion": [
                "format_converter - Convert media formats",
                "codec_transformer - Transform codecs",
                "quality_adjuster - Adjust media quality",
                "batch_converter - Batch convert files",
                "resolution_changer - Change video resolution"
            ],
            "Audio/Video Editing": [
                "media_trimmer - Trim audio/video",
                "media_splitter - Split media files",
                "media_merger - Merge media files",
                "volume_adjuster - Adjust audio volume",
                "speed_controller - Control playback speed"
            ],
            "Audio/Video Compression": [
                "size_optimizer - Optimize file size",
                "bitrate_adjuster - Adjust bitrate",
                "quality_compressor - Quality-based compression",
                "batch_compression - Batch compress files",
                "format_specific_compression - Format-specific compression"
            ],
            "Audio/Video Analysis": [
                "metadata_extractor - Extract metadata",
                "format_detector - Detect file format",
                "quality_analyzer - Analyze media quality",
                "duration_calculator - Calculate duration",
                "codec_identifier - Identify codecs"
            ],
            "Streaming Tools": [
                "stream_configuration - Configure streaming",
                "broadcast_settings - Broadcast settings",
                "encoding_optimizer - Optimize encoding",
                "quality_settings - Quality settings for streaming",
                "platform_optimizer - Platform-specific optimization"
            ],
            "Subtitle Tools": [
                "subtitle_editor - Edit subtitles",
                "timing_adjuster - Adjust subtitle timing",
                "subtitle_format_converter - Convert subtitle formats",
                "subtitle_generator - Generate subtitles",
                "subtitle_synchronizer - Synchronize subtitles"
            ],
            "Metadata Editors": [
                "tag_editor - Edit media tags",
                "cover_art_manager - Manage cover art",
                "information_extractor - Extract file information",
                "metadata_batch_editor - Batch edit metadata",
                "id3_editor - Edit ID3 tags"
            ],
            "Audio Enhancement": [
                "noise_reduction - Reduce audio noise",
                "audio_equalizer - Equalize audio",
                "audio_normalizer - Normalize audio levels",
                "audio_amplifier - Amplify audio",
                "echo_remover - Remove echo from audio"
            ],
            "Video Enhancement": [
                "video_stabilizer - Stabilize shaky video",
                "color_corrector - Correct video colors",
                "brightness_adjuster - Adjust video brightness",
                "contrast_enhancer - Enhance video contrast",
                "frame_rate_converter - Convert frame rate"
            ],
            "Media Utilities": [
                "playlist_creator - Create playlists",
                "media_organizer - Organize media files",
                "media_batch_processor - Batch process media",
                "media_file_renamer - Rename media files",
                "media_duplicate_finder - Find duplicate media"
            ]
        }


def create_ai_features():
    """Factory function to create AIFeatures instance"""
    return AIFeatures()
