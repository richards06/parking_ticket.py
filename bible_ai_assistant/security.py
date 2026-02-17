"""
Security module for input/output sanitization and prompt injection protection
"""
import re
from typing import Optional
from config import MAX_INPUT_LENGTH


class SecurityManager:
    """Handles input validation, sanitization, and prompt injection detection"""
    
    # Patterns that indicate prompt injection attempts
    INJECTION_PATTERNS = [
        r'ignore\s+(?:previous\s+)?instructions?',
        r'forget\s+(?:previous|your)\s+instructions?',
        r'system\s+prompt',
        r'jailbreak',
        r'bypass\s+(?:the\s+)?rules?',
        r'override\s+(?:your\s+)?(?:instructions|rules)',
        r'you\s+are\s+no\s+longer',
        r'pretend\s+(?:you\s+are|to\s+be)',
        r'act\s+as\s+(?:a\s+)?(?:hacker|administrator)',
        r'developer\s+mode',
        r'hidden\s+instructions?',
        r'secret\s+mode',
    ]
    
    # Dangerous output keywords - be specific to avoid false positives
    DANGEROUS_OUTPUT_KEYWORDS = [
        'api_key', 'apikey', 'password', 'secret', 'token',
        'delete', 'drop', 'truncate', 'rm -rf',
        'credit card', 'ssn', 'social security'
    ]
    
    @staticmethod
    def sanitize_input(user_input: str) -> Optional[str]:
        """
        Sanitize and validate user input
        Returns sanitized input or None if dangerous
        """
        if not user_input:
            return None
        
        # Check length
        if len(user_input) > MAX_INPUT_LENGTH:
            return None
        
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in user_input if ord(char) >= 32 or char in '\n\t')
        
        # Check for injection patterns
        for pattern in SecurityManager.INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return None
        
        # Limit suspicious characters
        if sanitized.count('{') > 3 or sanitized.count('}') > 3:
            return None
        
        return sanitized.strip()
    
    @staticmethod
    def filter_response(response: str) -> str:
        """
        Filter LLM response to prevent leaking sensitive information
        Look for PATTERNS of information leakage, not just words
        """
        if not response:
            return "I'm unable to provide a response at this time."
        
        # Check for dangerous patterns (not just keywords that appear in scripture)
        # Pattern: actual credential exposure like "api_key=sk-..." or "password: ..."
        dangerous_patterns = [
            r'api[_-]?key\s*[=:]\s*[a-zA-Z0-9_\-]{20,}',  # API key with value
            r'password\s*[=:]\s*\S+',  # Password with value
            r'token\s*[=:]\s*[a-zA-Z0-9_\-]{20,}',  # Token with value
            r'secret\s*[=:]\s*[a-zA-Z0-9_\-]{20,}',  # Secret with value
            r'credit.?card\s*[=:]\s*\d{13,19}',  # Credit card number
            r'ssn\s*[=:]\s*\d{3}-\d{2}-\d{4}',  # SSN pattern
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return "I can only provide Bible-based information and guidance."
        
        return response
    
    @staticmethod
    def validate_scripture_reference(reference: str) -> bool:
        """
        Validate that a scripture reference follows proper format
        Examples: John 3:16, Genesis 1:1-5, Psalm 23
        """
        pattern = r'^[A-Za-z\s0-9:.-]+$'
        return bool(re.match(pattern, reference)) and len(reference) < 50
