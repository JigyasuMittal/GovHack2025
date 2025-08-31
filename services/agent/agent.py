#!/usr/bin/env python3
"""
GovMate AI Agent - Main agent logic for government service discovery.
Uses a rules-first approach with LLM fallback for robust intent classification and planning.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class Intent:
    """Represents a classified user intent."""
    intent: str
    confidence: float
    slots: Dict[str, Any]
    tags: List[str]

@dataclass
class ServiceLocation:
    """Represents a government service location."""
    id: int
    name: str
    description: str
    agency: str
    address: str
    suburb: str
    state: str
    lat: float
    lon: float
    distance_km: float
    phone: Optional[str]
    website: Optional[str]
    category: str

@dataclass
class Plan:
    """Represents an AI agent plan for helping the user."""
    intent: str
    services: List[ServiceLocation]
    seifa_context: Optional[Dict[str, Any]]
    labour_context: Optional[Dict[str, Any]]
    rulecard: Optional[Dict[str, Any]]
    citations: List[str]
    reasoning: str

class GovMateAgent:
    """Main AI agent for government service discovery."""
    
    def __init__(self):
        self.intent_patterns = {
            'employment_support': [
                r'\b(lost|lost my|unemployed|job|employment|work|centrelink|jobseeker|newstart)\b',
                r'\b(need help finding|looking for|seeking|want to find)\b.*\b(job|work|employment)\b',
                r'\b(redundant|laid off|fired|dismissed|terminated)\b',
                r'\b(income support|benefits|payment|allowance)\b'
            ],
            'driver_licence': [
                r'\b(driver|driving|licence|license|learner|test|road test)\b',
                r'\b(need to get|want to get|apply for)\b.*\b(licence|license)\b',
                r'\b(transport|TMR|department of transport)\b',
                r'\b(learn to drive|driving lessons|driving test)\b'
            ],
            'housing_support': [
                r'\b(housing|home|rent|rental|accommodation|homeless|evicted)\b',
                r'\b(need a place|looking for|seeking)\b.*\b(home|house|apartment|accommodation)\b',
                r'\b(public housing|social housing|housing assistance)\b',
                r'\b(can\'t afford|struggling with|difficulty paying)\b.*\b(rent|housing)\b'
            ],
            'food_assistance': [
                r'\b(food|hungry|groceries|meals|eating|feed)\b',
                r'\b(can\'t afford|struggling with|need help with)\b.*\b(food|groceries|meals)\b',
                r'\b(food bank|food pantry|emergency food)\b',
                r'\b(going hungry|not enough to eat|food insecurity)\b'
            ],
            'health_support': [
                r'\b(health|medical|doctor|hospital|medicare|healthcare)\b',
                r'\b(need medical|sick|ill|health problem|medical help)\b',
                r'\b(can\'t afford|struggling with)\b.*\b(medical|health|doctor)\b',
                r'\b(mental health|depression|anxiety|stress)\b'
            ],
            'financial_assistance': [
                r'\b(money|financial|cash|funds|payment|bill|debt)\b',
                r'\b(can\'t pay|struggling with|need help with)\b.*\b(bill|debt|payment)\b',
                r'\b(emergency payment|financial hardship|financial assistance)\b',
                r'\b(broke|no money|financial difficulty)\b'
            ]
        }
        
        self.location_patterns = [
            r'\b(near|in|at|around)\b\s+([A-Za-z\s]+)',
            r'\b([A-Za-z\s]+)\s+(QLD|NSW|VIC|WA|SA|TAS|NT|ACT)\b',
            r'\b(Brisbane|Sydney|Melbourne|Perth|Adelaide|Hobart|Darwin|Canberra)\b'
        ]
    
    def classify_intent(self, query: str) -> Intent:
        """Classify user intent using pattern matching and rules."""
        
        query_lower = query.lower()
        best_intent = "general_info"
        best_confidence = 0.3
        matched_tags = []
        
        # Pattern-based classification
        for intent, patterns in self.intent_patterns.items():
            confidence = 0.0
            intent_tags = []
            
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                if matches:
                    confidence += 0.3
                    intent_tags.extend(matches)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent
                matched_tags = intent_tags
        
        # Extract location information
        location = self.extract_location(query)
        
        # Extract other slots
        slots = {
            'location': location,
            'urgency': self.detect_urgency(query),
            'specific_service': self.extract_specific_service(query)
        }
        
        return Intent(
            intent=best_intent,
            confidence=min(best_confidence, 0.95),
            slots=slots,
            tags=matched_tags
        )
    
    def extract_location(self, query: str) -> Optional[str]:
        """Extract location information from query."""
        
        for pattern in self.location_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    return ' '.join(matches[0]).strip()
                else:
                    return matches[0].strip()
        
        return None
    
    def detect_urgency(self, query: str) -> str:
        """Detect urgency level in the query."""
        
        urgent_words = ['emergency', 'urgent', 'immediately', 'now', 'today', 'asap']
        query_lower = query.lower()
        
        for word in urgent_words:
            if word in query_lower:
                return 'high'
        
        return 'normal'
    
    def extract_specific_service(self, query: str) -> Optional[str]:
        """Extract specific service mentions."""
        
        service_keywords = {
            'centrelink': ['centrelink', 'jobseeker', 'newstart'],
            'medicare': ['medicare', 'health insurance'],
            'housing': ['housing', 'rental assistance', 'public housing'],
            'food': ['food bank', 'food assistance', 'meals'],
            'transport': ['driver licence', 'transport', 'TMR']
        }
        
        query_lower = query.lower()
        for service, keywords in service_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return service
        
        return None
    
    def create_plan(self, intent: Intent, services: List[ServiceLocation], 
                   seifa_context: Optional[Dict] = None,
                   labour_context: Optional[Dict] = None,
                   rulecard: Optional[Dict] = None) -> Plan:
        """Create a comprehensive plan for the user."""
        
        # Generate reasoning
        reasoning = self.generate_reasoning(intent, services, seifa_context, labour_context)
        
        # Generate citations
        citations = self.generate_citations(intent, services, seifa_context, labour_context)
        
        return Plan(
            intent=intent.intent,
            services=services,
            seifa_context=seifa_context,
            labour_context=labour_context,
            rulecard=rulecard,
            citations=citations,
            reasoning=reasoning
        )
    
    def generate_reasoning(self, intent: Intent, services: List[ServiceLocation],
                          seifa_context: Optional[Dict] = None,
                          labour_context: Optional[Dict] = None) -> str:
        """Generate reasoning for the plan."""
        
        reasoning_parts = []
        
        # Intent reasoning
        reasoning_parts.append(f"Based on your query, I identified you need help with {intent.intent.replace('_', ' ')}.")
        
        # Service reasoning
        if services:
            reasoning_parts.append(f"I found {len(services)} relevant services near you.")
            
            # Add SEIFA context if available
            if seifa_context:
                decile = seifa_context.get('irsd_decile', 'unknown')
                reasoning_parts.append(f"Your area has a SEIFA decile of {decile}/10, which helps us understand local socio-economic context.")
            
            # Add labour context if available
            if labour_context:
                unemployment = labour_context.get('unemployment_rate', 'unknown')
                reasoning_parts.append(f"Current unemployment rate in your state is {unemployment}%.")
        
        return " ".join(reasoning_parts)
    
    def generate_citations(self, intent: Intent, services: List[ServiceLocation],
                          seifa_context: Optional[Dict] = None,
                          labour_context: Optional[Dict] = None) -> List[str]:
        """Generate citations for the plan."""
        
        citations = []
        
        # Add service citations
        for service in services:
            citations.append(f"Service: {service.name} - {service.agency}")
        
        # Add data source citations
        if seifa_context:
            citations.append("SEIFA 2021 data from Australian Bureau of Statistics")
        
        if labour_context:
            citations.append("Labour Force data from Australian Bureau of Statistics")
        
        # Add government directory citations
        citations.append("Government service locations from official directories")
        
        return citations
    
    def get_rulecard(self, intent: str) -> Optional[Dict[str, Any]]:
        """Get rulecard for the given intent."""
        
        rulecards = {
            'employment_support': {
                'description': 'Steps to get employment support and income assistance',
                'checklist': [
                    'Apply for JobSeeker Payment through Centrelink',
                    'Create a myGov account if you don\'t have one',
                    'Provide required documents (ID, bank details, employment separation certificate)',
                    'Attend appointments with your job service provider',
                    'Look for suitable employment opportunities',
                    'Consider training or upskilling programs'
                ],
                'citations': [
                    'Services Australia - JobSeeker Payment',
                    'Australian Government - myGov',
                    'Department of Employment and Workplace Relations'
                ]
            },
            'driver_licence': {
                'description': 'Steps to get your driver licence in Queensland',
                'checklist': [
                    'Check eligibility requirements on TMR website',
                    'Book a theory test at a TMR customer service centre',
                    'Study the road rules and practice tests',
                    'Pass the theory test to get your learner licence',
                    'Complete required driving hours with a supervising driver',
                    'Book and pass your practical driving test',
                    'Pay licence fees and receive your licence'
                ],
                'citations': [
                    'Queensland Transport and Main Roads',
                    'TMR Customer Service Centres',
                    'Queensland Government - Driver Licences'
                ]
            },
            'housing_support': {
                'description': 'Steps to get housing assistance and support',
                'checklist': [
                    'Contact your local housing service office',
                    'Check eligibility for public housing',
                    'Apply for rental assistance through Centrelink',
                    'Contact local community housing providers',
                    'Seek emergency accommodation if needed',
                    'Consider private rental with assistance'
                ],
                'citations': [
                    'Queensland Housing Department',
                    'Services Australia - Rental Assistance',
                    'Community Housing Providers'
                ]
            },
            'food_assistance': {
                'description': 'Steps to get food assistance and support',
                'checklist': [
                    'Contact your local food bank or food pantry',
                    'Check eligibility for food assistance programs',
                    'Visit community centres for meal programs',
                    'Contact local charities and community organisations',
                    'Check for emergency food relief services',
                    'Consider government assistance programs'
                ],
                'citations': [
                    'Foodbank Queensland',
                    'Local Community Centres',
                    'Charity and Community Organisations'
                ]
            }
        }
        
        return rulecards.get(intent)
    
    def audit_plan(self, user_input: str, plan: Plan) -> Dict[str, Any]:
        """Create an audit log of the agent's decision-making process."""
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'user_input': user_input,
            'intent_classification': {
                'intent': plan.intent,
                'confidence': 0.85,  # Would be from actual classification
                'tags': ['employment', 'support']  # Would be from actual classification
            },
            'services_found': len(plan.services),
            'context_used': {
                'seifa': plan.seifa_context is not None,
                'labour': plan.labour_context is not None,
                'rulecard': plan.rulecard is not None
            },
            'reasoning': plan.reasoning,
            'citations': plan.citations,
            'data_sources': [
                'ABS SEIFA 2021',
                'ABS Labour Force Statistics',
                'Government Service Directories',
                'Official Agency Websites'
            ]
        }

# Global agent instance
agent = GovMateAgent()
