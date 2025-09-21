"""
Enhanced Input Validation Engine
Advanced input validation with comprehensive sanitization
"""
import re
import html
import urllib.parse
import json
import base64
import hashlib
from typing import Dict, List, Optional, Any, Union
import email.utils
import ipaddress

class EnhancedInputValidator:
    """Enhanced Input Validation with Advanced Sanitization"""
    
    def __init__(self):
        self.validation_rules = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[\d\s\-\(\)]{10,}$',
            'url': r'^https?://[^\s/$.?#].[^\s]*$',
            'ip_address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'username': r'^[a-zA-Z0-9_]{3,20}$',
            'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            'credit_card': r'^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$',
            'ssn': r'^\d{3}-\d{2}-\d{4}$',
            'zip_code': r'^\d{5}(-\d{4})?$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'time': r'^\d{2}:\d{2}:\d{2}$',
            'datetime': r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        }
        
        self.dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'data:text/html',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',
            r'<link[^>]*>',
            r'<meta[^>]*>',
            r'<style[^>]*>.*?</style>',
            r'expression\s*\(',
            r'url\s*\(',
            r'@import',
            r'\.\./',
            r'\.\.\\',
            r'%2e%2e%2f',
            r'%2e%2e%5c',
            r'\.\.%2f',
            r'\.\.%5c',
            r'\.\.%252f',
            r'\.\.%255c',
            r'[;&\|`$]',
            r'(\bcat\b|\bls\b|\bdir\b|\btype\b|\bmore\b|\bless\b|\bhead\b|\btail\b)',
            r'(\bwhoami\b|\bid\b|\buname\b|\bhostname\b)',
            r'(\bping\b|\bnslookup\b|\bdig\b|\btraceroute\b)',
            r'(\bwget\b|\bcurl\b|\bfetch\b|\bdownload\b)',
            r'(\brm\b|\bdel\b|\bremove\b|\bdelete\b)',
            r'(\bmkdir\b|\bmd\b|\bcreate\b|\bnew\b)',
            r'(\bchmod\b|\bchown\b|\battrib\b|\bpermissions\b)',
            r"('|(\\')|(;)|(--)|(/\*)|(\*/)|(\bunion\b)|(\bselect\b)|(\binsert\b)|(\bupdate\b)|(\bdelete\b)|(\bdrop\b)|(\bcreate\b)|(\balter\b))",
            r"(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+",
            r"(\bUNION\b|\bSELECT\b).*(\bFROM\b|\bWHERE\b)",
            r"(\bINSERT\b|\bUPDATE\b|\bDELETE\b).*(\bINTO\b|\bSET\b|\bFROM\b)",
            r"(\bDROP\b|\bCREATE\b|\bALTER\b).*(\bTABLE\b|\bDATABASE\b|\bINDEX\b)",
            r"[\(\)=\*!&\|]",
            r"(\bcn\b|\bdc\b|\bou\b|\bobjectClass\b)",
            r"(\buserPassword\b|\bmail\b|\btelephoneNumber\b)",
            r"(\bdistinguishedName\b|\bcn\b|\bsn\b|\bgivenName\b)",
            r"<!DOCTYPE",
            r"<!ENTITY",
            r"<!\[CDATA\[",
            r"<\?xml",
            r"&\w+;"
        ]
        
        self.validation_stats = {
            'total_validations': 0,
            'passed_validations': 0,
            'failed_validations': 0,
            'sanitizations_performed': 0,
            'dangerous_patterns_detected': 0
        }
        
        print("🔍 Enhanced Input Validator initialized!")
        print(f"   Validation rules: {len(self.validation_rules)}")
        print(f"   Dangerous patterns: {len(self.dangerous_patterns)}")
    
    def validate_input(self, input_data: Any, input_type: str, rules: Dict = None) -> Dict:
        """Validate input data with comprehensive checks"""
        self.validation_stats['total_validations'] += 1
        
        validation_result = {
            'is_valid': True,
            'sanitized_value': input_data,
            'original_value': input_data,
            'validation_errors': [],
            'sanitization_applied': False,
            'threat_detected': False,
            'recommendations': []
        }
        
        # Convert input to string for validation
        if isinstance(input_data, (dict, list)):
            input_str = json.dumps(input_data)
        else:
            input_str = str(input_data)
        
        # Check for dangerous patterns
        threat_detection = self._detect_dangerous_patterns(input_str)
        if threat_detection['threat_detected']:
            validation_result['threat_detected'] = True
            validation_result['validation_errors'].extend(threat_detection['threats'])
            validation_result['recommendations'].extend(threat_detection['recommendations'])
            self.validation_stats['dangerous_patterns_detected'] += 1
        
        # Apply input type validation
        if input_type in self.validation_rules:
            type_validation = self._validate_by_type(input_str, input_type)
            if not type_validation['is_valid']:
                validation_result['is_valid'] = False
                validation_result['validation_errors'].extend(type_validation['errors'])
                validation_result['recommendations'].extend(type_validation['recommendations'])
        
        # Apply custom rules if provided
        if rules:
            custom_validation = self._validate_custom_rules(input_str, rules)
            if not custom_validation['is_valid']:
                validation_result['is_valid'] = False
                validation_result['validation_errors'].extend(custom_validation['errors'])
                validation_result['recommendations'].extend(custom_validation['recommendations'])
        
        # Sanitize input if needed
        if validation_result['threat_detected'] or not validation_result['is_valid']:
            sanitized = self._sanitize_input(input_str)
            if sanitized != input_str:
                validation_result['sanitized_value'] = sanitized
                validation_result['sanitization_applied'] = True
                validation_result['is_valid'] = True
                self.validation_stats['sanitizations_performed'] += 1
        
        # Update statistics
        if validation_result['is_valid']:
            self.validation_stats['passed_validations'] += 1
        else:
            self.validation_stats['failed_validations'] += 1
        
        return validation_result
    
    def _detect_dangerous_patterns(self, input_str: str) -> Dict:
        """Detect dangerous patterns in input"""
        threats = []
        recommendations = []
        
        for pattern in self.dangerous_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                threats.append(f"Dangerous pattern detected: {pattern}")
                recommendations.extend([
                    'BLOCK_INPUT',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_INPUT_SOURCE',
                    'IMPLEMENT_ADDITIONAL_VALIDATION'
                ])
        
        return {
            'threat_detected': len(threats) > 0,
            'threats': threats,
            'recommendations': recommendations
        }
    
    def _validate_by_type(self, input_str: str, input_type: str) -> Dict:
        """Validate input by specific type"""
        errors = []
        recommendations = []
        
        if input_type == 'email':
            if not re.match(self.validation_rules['email'], input_str):
                errors.append("Invalid email format")
                recommendations.append("Use valid email format: user@domain.com")
        
        elif input_type == 'phone':
            if not re.match(self.validation_rules['phone'], input_str):
                errors.append("Invalid phone number format")
                recommendations.append("Use valid phone format: +1234567890")
        
        elif input_type == 'url':
            if not re.match(self.validation_rules['url'], input_str):
                errors.append("Invalid URL format")
                recommendations.append("Use valid URL format: https://example.com")
        
        elif input_type == 'ip_address':
            try:
                ipaddress.ip_address(input_str)
            except ValueError:
                errors.append("Invalid IP address format")
                recommendations.append("Use valid IP format: 192.168.1.1")
        
        elif input_type == 'username':
            if not re.match(self.validation_rules['username'], input_str):
                errors.append("Invalid username format")
                recommendations.append("Use 3-20 characters, alphanumeric and underscore only")
        
        elif input_type == 'password':
            if not re.match(self.validation_rules['password'], input_str):
                errors.append("Weak password format")
                recommendations.append("Use 8+ characters with uppercase, lowercase, number, and special character")
        
        elif input_type == 'credit_card':
            if not re.match(self.validation_rules['credit_card'], input_str):
                errors.append("Invalid credit card format")
                recommendations.append("Use valid credit card format: 1234-5678-9012-3456")
        
        elif input_type == 'ssn':
            if not re.match(self.validation_rules['ssn'], input_str):
                errors.append("Invalid SSN format")
                recommendations.append("Use valid SSN format: 123-45-6789")
        
        elif input_type == 'zip_code':
            if not re.match(self.validation_rules['zip_code'], input_str):
                errors.append("Invalid ZIP code format")
                recommendations.append("Use valid ZIP format: 12345 or 12345-6789")
        
        elif input_type == 'date':
            if not re.match(self.validation_rules['date'], input_str):
                errors.append("Invalid date format")
                recommendations.append("Use valid date format: YYYY-MM-DD")
        
        elif input_type == 'time':
            if not re.match(self.validation_rules['time'], input_str):
                errors.append("Invalid time format")
                recommendations.append("Use valid time format: HH:MM:SS")
        
        elif input_type == 'datetime':
            if not re.match(self.validation_rules['datetime'], input_str):
                errors.append("Invalid datetime format")
                recommendations.append("Use valid datetime format: YYYY-MM-DD HH:MM:SS")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations
        }
    
    def _validate_custom_rules(self, input_str: str, rules: Dict) -> Dict:
        """Validate input against custom rules"""
        errors = []
        recommendations = []
        
        # Length validation
        if 'min_length' in rules and len(input_str) < rules['min_length']:
            errors.append(f"Input too short (minimum {rules['min_length']} characters)")
            recommendations.append(f"Increase input length to at least {rules['min_length']} characters")
        
        if 'max_length' in rules and len(input_str) > rules['max_length']:
            errors.append(f"Input too long (maximum {rules['max_length']} characters)")
            recommendations.append(f"Reduce input length to maximum {rules['max_length']} characters")
        
        # Character validation
        if 'allowed_chars' in rules:
            allowed_pattern = f"^[{rules['allowed_chars']}]+$"
            if not re.match(allowed_pattern, input_str):
                errors.append(f"Input contains disallowed characters")
                recommendations.append(f"Use only allowed characters: {rules['allowed_chars']}")
        
        if 'forbidden_chars' in rules:
            forbidden_pattern = f"[{rules['forbidden_chars']}]"
            if re.search(forbidden_pattern, input_str):
                errors.append(f"Input contains forbidden characters")
                recommendations.append(f"Remove forbidden characters: {rules['forbidden_chars']}")
        
        # Pattern validation
        if 'pattern' in rules:
            if not re.match(rules['pattern'], input_str):
                errors.append("Input does not match required pattern")
                recommendations.append("Modify input to match required pattern")
        
        # Value range validation
        if 'min_value' in rules and input_str.isdigit():
            if int(input_str) < rules['min_value']:
                errors.append(f"Value too small (minimum {rules['min_value']})")
                recommendations.append(f"Increase value to at least {rules['min_value']}")
        
        if 'max_value' in rules and input_str.isdigit():
            if int(input_str) > rules['max_value']:
                errors.append(f"Value too large (maximum {rules['max_value']})")
                recommendations.append(f"Reduce value to maximum {rules['max_value']}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations
        }
    
    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize input to remove dangerous content"""
        sanitized = input_str
        
        # HTML encoding
        sanitized = html.escape(sanitized, quote=True)
        
        # URL decoding
        sanitized = urllib.parse.unquote(sanitized)
        
        # Remove dangerous patterns
        for pattern in self.dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    def validate_json_input(self, json_data: Union[str, dict], schema: Dict = None) -> Dict:
        """Validate JSON input with optional schema"""
        validation_result = {
            'is_valid': True,
            'sanitized_value': json_data,
            'original_value': json_data,
            'validation_errors': [],
            'sanitization_applied': False,
            'threat_detected': False,
            'recommendations': []
        }
        
        try:
            # Parse JSON if string
            if isinstance(json_data, str):
                parsed_data = json.loads(json_data)
            else:
                parsed_data = json_data
            
            # Validate schema if provided
            if schema:
                schema_validation = self._validate_json_schema(parsed_data, schema)
                if not schema_validation['is_valid']:
                    validation_result['is_valid'] = False
                    validation_result['validation_errors'].extend(schema_validation['errors'])
                    validation_result['recommendations'].extend(schema_validation['recommendations'])
            
            # Check for dangerous patterns in JSON values
            threat_detection = self._detect_dangerous_patterns_in_json(parsed_data)
            if threat_detection['threat_detected']:
                validation_result['threat_detected'] = True
                validation_result['validation_errors'].extend(threat_detection['threats'])
                validation_result['recommendations'].extend(threat_detection['recommendations'])
            
            validation_result['sanitized_value'] = parsed_data
            
        except json.JSONDecodeError as e:
            validation_result['is_valid'] = False
            validation_result['validation_errors'].append(f"Invalid JSON format: {str(e)}")
            validation_result['recommendations'].append("Use valid JSON format")
        
        return validation_result
    
    def _validate_json_schema(self, data: Any, schema: Dict) -> Dict:
        """Validate JSON data against schema"""
        errors = []
        recommendations = []
        
        # Required fields validation
        if 'required' in schema:
            for field in schema['required']:
                if field not in data:
                    errors.append(f"Required field '{field}' is missing")
                    recommendations.append(f"Add required field '{field}'")
        
        # Field type validation
        if 'properties' in schema:
            for field, field_schema in schema['properties'].items():
                if field in data:
                    field_validation = self._validate_field_type(data[field], field_schema)
                    if not field_validation['is_valid']:
                        errors.extend([f"{field}: {error}" for error in field_validation['errors']])
                        recommendations.extend([f"{field}: {rec}" for rec in field_validation['recommendations']])
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations
        }
    
    def _validate_field_type(self, value: Any, field_schema: Dict) -> Dict:
        """Validate individual field against schema"""
        errors = []
        recommendations = []
        
        if 'type' in field_schema:
            expected_type = field_schema['type']
            if expected_type == 'string' and not isinstance(value, str):
                errors.append(f"Expected string, got {type(value).__name__}")
                recommendations.append("Convert to string type")
            elif expected_type == 'number' and not isinstance(value, (int, float)):
                errors.append(f"Expected number, got {type(value).__name__}")
                recommendations.append("Convert to number type")
            elif expected_type == 'boolean' and not isinstance(value, bool):
                errors.append(f"Expected boolean, got {type(value).__name__}")
                recommendations.append("Convert to boolean type")
            elif expected_type == 'array' and not isinstance(value, list):
                errors.append(f"Expected array, got {type(value).__name__}")
                recommendations.append("Convert to array type")
            elif expected_type == 'object' and not isinstance(value, dict):
                errors.append(f"Expected object, got {type(value).__name__}")
                recommendations.append("Convert to object type")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations
        }
    
    def _detect_dangerous_patterns_in_json(self, data: Any) -> Dict:
        """Detect dangerous patterns in JSON data"""
        threats = []
        recommendations = []
        
        def check_value(value):
            if isinstance(value, str):
                for pattern in self.dangerous_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        threats.append(f"Dangerous pattern in JSON: {pattern}")
                        recommendations.extend([
                            'BLOCK_JSON_INPUT',
                            'LOG_ATTEMPT',
                            'ALERT_SECURITY_TEAM',
                            'REVIEW_JSON_SOURCE',
                            'IMPLEMENT_JSON_VALIDATION'
                        ])
            elif isinstance(value, (dict, list)):
                if isinstance(value, dict):
                    for v in value.values():
                        check_value(v)
                elif isinstance(value, list):
                    for v in value:
                        check_value(v)
        
        check_value(data)
        
        return {
            'threat_detected': len(threats) > 0,
            'threats': threats,
            'recommendations': recommendations
        }
    
    def get_validation_statistics(self) -> Dict:
        """Get validation statistics"""
        return {
            'total_validations': self.validation_stats['total_validations'],
            'passed_validations': self.validation_stats['passed_validations'],
            'failed_validations': self.validation_stats['failed_validations'],
            'success_rate': (self.validation_stats['passed_validations'] / max(self.validation_stats['total_validations'], 1)) * 100,
            'sanitizations_performed': self.validation_stats['sanitizations_performed'],
            'dangerous_patterns_detected': self.validation_stats['dangerous_patterns_detected'],
            'validation_rules_count': len(self.validation_rules),
            'dangerous_patterns_count': len(self.dangerous_patterns)
        }
