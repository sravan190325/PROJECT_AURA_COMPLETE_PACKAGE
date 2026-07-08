"""
Claude Service for Project Aura.
Handles all interactions with Anthropic Claude API.
"""

import logging
import json
import os
import re
from typing import Dict, Any, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeService:
    """
    Service for interacting with Anthropic Claude API.
    Analyzes documents and extracts project information.
    Supports mock mode for testing when API quota is exhausted.
    """

    def __init__(self, api_key: str):
        """
        Initialize Claude Service.

        Args:
            api_key: Anthropic API key
        """
        self.use_mock = os.environ.get('USE_MOCK_CLAUDE', 'False').lower() == 'true'

        if not self.use_mock:
            self.client = Anthropic(api_key=api_key)
        else:
            self.client = None
            logger.info("Claude Service running in MOCK mode - no API calls will be made")

        self.model = "claude-3-5-sonnet-20241022"

    def analyze_project_documents(self, documents: list) -> Dict[str, Any]:
        """
        Analyze project documents using Claude to detect project type and extract information.

        Args:
            documents: List of document dictionaries with extracted content

        Returns:
            Dictionary with analysis results:
                - project_type: Detected project type
                - client_name: Extracted client name
                - scope: Project scope description
                - deliverables: List of deliverables
                - team_requirements: Required team composition
                - confidence: Confidence score of detection
                - extracted_fields: Raw extracted information
        """
        try:
            # Use mock data if in mock mode
            if self.use_mock:
                logger.info("Using mock Claude analysis (mock mode enabled)")
                result = self._get_mock_analysis(documents)
                return {
                    'success': True,
                    'analysis': result,
                    'error': None
                }

            # Prepare document content for analysis
            document_text = self._prepare_document_text(documents)

            # Create prompt for Claude
            prompt = self._create_analysis_prompt(document_text)

            # Call Claude API
            logger.info("Calling Claude API for document analysis")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse response
            response_text = message.content[0].text
            result = self._parse_analysis_response(response_text)

            logger.info(f"Analysis complete. Detected project type: {result.get('project_type')}")

            return {
                'success': True,
                'analysis': result,
                'error': None
            }

        except Exception as e:
            error_msg = f"Error analyzing documents with Claude: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'analysis': None,
                'error': error_msg
            }

    def clarify_project_information(self, analysis: Dict, user_input: Dict) -> Dict[str, Any]:
        """
        Clarify project information based on user input for missing fields.

        Args:
            analysis: Initial analysis from Claude
            user_input: User-provided clarifications

        Returns:
            Dictionary with complete project information
        """
        try:
            # Merge analysis with user input
            complete_info = {
                **analysis,
                'start_date': user_input.get('start_date'),
                'duration_weeks': user_input.get('duration'),
                'team_size': user_input.get('team_size'),
                'delivery_model': user_input.get('delivery_model')
            }

            # Use mock data if in mock mode
            if self.use_mock:
                logger.info("Using mock Claude clarification (mock mode enabled)")
                return {
                    'success': True,
                    'project_info': complete_info,
                    'error': None
                }

            # Validate and enhance the information
            prompt = self._create_clarification_prompt(analysis, user_input)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text
            enhanced_info = self._parse_clarification_response(response_text, complete_info)

            logger.info("Project information clarified successfully")

            return {
                'success': True,
                'project_info': enhanced_info,
                'error': None
            }

        except Exception as e:
            error_msg = f"Error clarifying project information: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'project_info': None,
                'error': error_msg
            }

    def _prepare_document_text(self, documents: list) -> str:
        """
        Prepare document text for Claude analysis.
        
        Args:
            documents: List of document dictionaries
        
        Returns:
            Formatted document text
        """
        doc_text = []
        
        for i, doc in enumerate(documents, 1):
            filename = doc.get('filename', 'Unknown')
            doc_type = doc.get('extension', 'unknown').upper()
            
            # Read from file if text is not in session
            content = doc.get('text', '')
            if not content and 'text_path' in doc and os.path.exists(doc['text_path']):
                try:
                    with open(doc['text_path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    logger.error(f"Failed to read text from {doc['text_path']}: {e}")
            content = content[:3000]  # Limit content length
            
            doc_text.append(f"""
--- Document {i}: {filename} ({doc_type}) ---
{content}
""")
        
        return '\n'.join(doc_text)

    def _create_analysis_prompt(self, document_text: str) -> str:
        """
        Create analysis prompt for Claude.
        
        Args:
            document_text: Extracted document text
        
        Returns:
            Formatted prompt for Claude
        """
        return f"""Analyze the following project documents and extract key information.

Documents:
{document_text}

Please analyze these documents and provide the following information in JSON format:

1. **project_type**: Identify the project type (Data Engineering, Data Analytics, Reporting/BI, GenAI, Cloud Migration, Application Development, Data Platform Modernization, or Other)
2. **client_name**: Extract the client or company name if mentioned
3. **scope**: Brief description of project scope
4. **deliverables**: List of key deliverables mentioned
5. **team_requirements**: Estimated team composition needed
6. **confidence**: Confidence level of this detection (0-100)
7. **missing_fields**: List of mandatory fields that are missing (e.g., "Start Date", "Duration", "Team Size", "Delivery Model")
8. **key_highlights**: Other important information extracted

Return ONLY valid JSON, no additional text. Example format:
{{
    "project_type": "Data Engineering",
    "client_name": "Company Name",
    "scope": "Build data pipeline...",
    "deliverables": ["Data Pipeline", "ETL Process"],
    "team_requirements": {{"PM": 1, "Data Engineer": 3, "QA": 1}},
    "confidence": 85,
    "missing_fields": ["Start Date", "Duration"],
    "key_highlights": ["Real-time processing", "Cloud-based"]
}}"""

    def _create_clarification_prompt(self, analysis: Dict, user_input: Dict) -> str:
        """
        Create clarification prompt for Claude.
        
        Args:
            analysis: Initial analysis results
            user_input: User-provided information
        
        Returns:
            Formatted prompt for Claude
        """
        return f"""Based on the project analysis and additional user information provided, 
please validate and enhance the project details.

Initial Analysis:
{json.dumps(analysis, indent=2)}

User Provided Information:
- Start Date: {user_input.get('start_date')}
- Duration: {user_input.get('duration')} weeks
- Team Size: {user_input.get('team_size')} people
- Delivery Model: {user_input.get('delivery_model')}

Please provide validation and any recommendations based on the project type and provided information.
Return JSON format with recommendations."""

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude's analysis response.
        
        Args:
            response_text: Raw response from Claude
        
        Returns:
            Parsed analysis dictionary
        """
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                logger.warning("Could not parse JSON from Claude response")
                return {
                    'project_type': 'Unknown',
                    'client_name': 'Not identified',
                    'scope': response_text[:200],
                    'deliverables': [],
                    'team_requirements': {},
                    'confidence': 0,
                    'missing_fields': ['Start Date', 'Duration', 'Team Size', 'Delivery Model'],
                    'raw_response': response_text
                }
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return {
                'project_type': 'Unknown',
                'confidence': 0,
                'error': 'Failed to parse response',
                'raw_response': response_text
            }

    def _parse_clarification_response(self, response_text: str, base_info: Dict) -> Dict[str, Any]:
        """
        Parse clarification response from Claude.

        Args:
            response_text: Raw response from Claude
            base_info: Base project information

        Returns:
            Enhanced project information dictionary
        """
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                enhancements = json.loads(json_str)
                return {**base_info, **enhancements}
            else:
                return base_info

        except json.JSONDecodeError:
            logger.warning("Could not parse clarification response as JSON")
            return base_info

    def _get_mock_analysis(self, documents: list) -> Dict[str, Any]:
        """
        Generate mock analysis data for testing (when API quota is exhausted).

        Args:
            documents: List of document dictionaries

        Returns:
            Mock analysis result
        """
        # Simulate analysis based on document content
        texts = []
        filenames = []
        for doc in documents:
            filenames.append(doc.get('filename', 'Uploaded Document'))
            content = doc.get('text', '')
            if not content and 'text_path' in doc and os.path.exists(doc['text_path']):
                try:
                    with open(doc['text_path'], 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    logger.error(f"Failed to read text from {doc['text_path']}: {e}")
            texts.append(content[:500])
        doc_text = '\n'.join(texts)
        cleaned_text = ' '.join(doc_text.split())

        # Detect project type based on keywords
        project_types = {
            'data engineer': ('Data Engineering', ['ETL Pipeline', 'Data Warehouse', 'Data Ingestion']),
            'ai': ('GenAI / AI Implementation', ['ML Model', 'AI Integration', 'LLM Implementation']),
            'cloud': ('Cloud Migration', ['AWS Migration', 'Infrastructure Setup', 'Cloud Architecture']),
            'analytics': ('Data Analytics', ['Dashboard', 'Analytics Platform', 'Reporting']),
            'bi': ('Reporting / BI', ['Business Intelligence', 'Reports', 'Dashboards']),
            'app': ('Application Development', ['Web App', 'Mobile App', 'API Development']),
            'platform': ('Data Platform Modernization', ['Platform Upgrade', 'Infrastructure Modernization', 'System Redesign']),
        }

        detected_type = 'Application Development'  # Default
        detected_deliverables = ['Application Delivery', 'Documentation', 'Testing']
        team_requirements = {'Project Manager': 1, 'Developer': 2, 'QA': 1}

        text_lower = doc_text.lower()
        for keyword, (ptype, deliverables) in project_types.items():
            if keyword in text_lower:
                detected_type = ptype
                detected_deliverables = deliverables
                break

        if 'mobile' in text_lower or 'android' in text_lower or 'ios' in text_lower:
            detected_type = 'Application Development'
            detected_deliverables = ['Mobile Application', 'Backend APIs', 'QA Test Report', 'Deployment Guide']
            team_requirements = {'Project Manager': 1, 'Mobile Developer': 2, 'Backend Developer': 1, 'QA': 1}
        elif detected_type == 'Data Engineering':
            team_requirements = {'Project Manager': 1, 'Data Engineer': 3, 'Data Architect': 1, 'QA': 1}
        elif detected_type == 'Data Analytics':
            team_requirements = {'Project Manager': 1, 'Data Analyst': 2, 'BI Developer': 1, 'QA': 1}
        elif detected_type == 'Cloud Migration':
            team_requirements = {'Project Manager': 1, 'Cloud Architect': 1, 'Cloud Engineer': 2, 'Security Engineer': 1, 'QA': 1}
        elif 'GenAI' in detected_type or detected_type == 'GenAI / AI Implementation':
            team_requirements = {'Project Manager': 1, 'AI Engineer': 2, 'Data Engineer': 1, 'QA': 1}

        client_name = self._extract_mock_field(
            cleaned_text,
            [
                r'(?:client|customer|company)\s*[:\-]\s*([A-Z][A-Za-z0-9 &,-]{2,60})',
                r'for\s+([A-Z][A-Za-z0-9 &,-]{2,60})'
            ],
            'Client from uploaded document'
        )
        project_name = self._extract_mock_field(
            cleaned_text,
            [
                r'(?:project|initiative|program)\s*(?:name)?\s*[:\-]\s*([A-Z][A-Za-z0-9 &,-]{3,80})',
                r'(?:SOW|Statement of Work)\s*(?:for)?\s*[:\-]?\s*([A-Z][A-Za-z0-9 &,-]{3,80})'
            ],
            os.path.splitext(filenames[0])[0] if filenames else f'{detected_type} Project'
        )
        scope = self._extract_mock_field(
            cleaned_text,
            [
                r'(?:scope|objective|overview)\s*[:\-]\s*([^.;]{30,260})',
                r'((?:build|develop|create|migrate|modernize|implement|deliver)\s+[^.;]{30,260})'
            ],
            cleaned_text[:260] if cleaned_text else 'Project scope will be refined from the uploaded document.'
        )

        return {
            'project_type': detected_type,
            'project_name': project_name,
            'client_name': client_name,
            'scope': scope,
            'deliverables': detected_deliverables,
            'team_requirements': team_requirements,
            'confidence': 75,
            'missing_fields': ['Start Date', 'Duration', 'Team Size', 'Delivery Model'],
            'key_highlights': [
                f'Analyzed uploaded file: {filenames[0] if filenames else "document"}',
                'Timeline and delivery model still need confirmation'
            ],
            'note': 'Mock analysis is enabled. Results are inferred from uploaded text without calling Claude.'
        }

    @staticmethod
    def _extract_mock_field(text: str, patterns: list, fallback: str) -> str:
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                value = ClaudeService._clean_mock_value(match.group(1))
                if value:
                    return value[:140]
        return fallback

    @staticmethod
    def _clean_mock_value(value: str) -> str:
        cleaned = value.strip(' -:.,')
        labels = [
            ' Client ',
            ' Scope ',
            ' Objective ',
            ' Overview ',
            ' Project Manager ',
            ' Deliverables ',
            ' Team ',
            ' Timeline ',
            ' Duration ',
            ' Start Date ',
        ]
        padded = f' {cleaned} '
        cut_points = [padded.find(label) for label in labels if padded.find(label) > 0]
        if cut_points:
            cleaned = padded[:min(cut_points)].strip()
        return cleaned.strip(' -:.,')
