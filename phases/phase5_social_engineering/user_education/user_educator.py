import time
import threading
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import random
from datetime import datetime, timedelta

class UserEducator:
    def __init__(self):
        self.education_active = False
        self.education_thread = None
        self.education_history = deque(maxlen=10000)
        self.user_progress = {}
        
        # Education configuration
        self.education_config = {
            'education_interval': 3600,  # 1 hour
            'quiz_interval': 86400,  # 1 day
            'simulation_interval': 604800,  # 1 week
            'education_level': 'intermediate',  # beginner, intermediate, advanced
            'auto_education': True,
            'interactive_education': True,
            'gamification': True
        }
        
        # Education content
        self.education_content = {
            'phishing_awareness': {
                'title': 'Phishing Awareness',
                'description': 'Learn to identify and avoid phishing attacks',
                'topics': [
                    'What is phishing?',
                    'Common phishing techniques',
                    'How to identify phishing emails',
                    'What to do if you receive a phishing email',
                    'How to report phishing attempts'
                ],
                'quiz_questions': [
                    {
                        'question': 'What is the most common sign of a phishing email?',
                        'options': ['Urgent language', 'Professional appearance', 'Correct spelling', 'Short length'],
                        'correct': 0,
                        'explanation': 'Phishing emails often use urgent language to pressure victims into acting quickly.'
                    },
                    {
                        'question': 'What should you do if you receive a suspicious email?',
                        'options': ['Click the links', 'Reply to the sender', 'Delete it immediately', 'Forward it to friends'],
                        'correct': 2,
                        'explanation': 'Delete suspicious emails immediately and report them to your IT department.'
                    }
                ]
            },
            'social_engineering': {
                'title': 'Social Engineering Awareness',
                'description': 'Understand social engineering tactics and how to protect yourself',
                'topics': [
                    'What is social engineering?',
                    'Common social engineering techniques',
                    'How to recognize social engineering attempts',
                    'How to protect yourself from social engineering',
                    'Reporting social engineering incidents'
                ],
                'quiz_questions': [
                    {
                        'question': 'What is social engineering?',
                        'options': ['A type of software', 'Manipulating people to gain information', 'A type of hardware', 'A programming language'],
                        'correct': 1,
                        'explanation': 'Social engineering is the manipulation of people to gain confidential information.'
                    },
                    {
                        'question': 'What should you do if someone calls asking for your password?',
                        'options': ['Give it to them', 'Ask for identification', 'Hang up immediately', 'Ask them to call back'],
                        'correct': 2,
                        'explanation': 'Never give your password to anyone, even if they claim to be from IT support.'
                    }
                ]
            },
            'password_security': {
                'title': 'Password Security',
                'description': 'Learn how to create and manage secure passwords',
                'topics': [
                    'What makes a strong password?',
                    'Password best practices',
                    'How to manage multiple passwords',
                    'Two-factor authentication',
                    'Password managers'
                ],
                'quiz_questions': [
                    {
                        'question': 'What is the minimum length for a strong password?',
                        'options': ['6 characters', '8 characters', '12 characters', '16 characters'],
                        'correct': 2,
                        'explanation': 'A strong password should be at least 12 characters long.'
                    },
                    {
                        'question': 'What is two-factor authentication?',
                        'options': ['Using two passwords', 'Using a password and a code', 'Using two usernames', 'Using two computers'],
                        'correct': 1,
                        'explanation': 'Two-factor authentication uses a password and a second factor like a code or biometric.'
                    }
                ]
            },
            'malware_awareness': {
                'title': 'Malware Awareness',
                'description': 'Learn about malware and how to protect yourself',
                'topics': [
                    'What is malware?',
                    'Types of malware',
                    'How malware spreads',
                    'How to protect against malware',
                    'What to do if you suspect malware'
                ],
                'quiz_questions': [
                    {
                        'question': 'What is malware?',
                        'options': ['Good software', 'Malicious software', 'Old software', 'New software'],
                        'correct': 1,
                        'explanation': 'Malware is malicious software designed to harm or exploit computer systems.'
                    },
                    {
                        'question': 'How can you protect against malware?',
                        'options': ['Open all emails', 'Click all links', 'Keep software updated', 'Disable antivirus'],
                        'correct': 2,
                        'explanation': 'Keeping software updated helps protect against known vulnerabilities.'
                    }
                ]
            },
            'data_protection': {
                'title': 'Data Protection',
                'description': 'Learn how to protect sensitive data',
                'topics': [
                    'What is sensitive data?',
                    'How to handle sensitive data',
                    'Data encryption',
                    'Secure data disposal',
                    'Data breach response'
                ],
                'quiz_questions': [
                    {
                        'question': 'What is considered sensitive data?',
                        'options': ['Public information', 'Personal information', 'Weather data', 'Sports scores'],
                        'correct': 1,
                        'explanation': 'Sensitive data includes personal information like SSNs, credit card numbers, and passwords.'
                    },
                    {
                        'question': 'What should you do with sensitive data when no longer needed?',
                        'options': ['Keep it forever', 'Delete it securely', 'Share it with friends', 'Post it online'],
                        'correct': 1,
                        'explanation': 'Sensitive data should be securely deleted when no longer needed.'
                    }
                ]
            }
        }
        
        # Education statistics
        self.education_stats = {
            'users_educated': 0,
            'education_sessions_completed': 0,
            'quiz_sessions_completed': 0,
            'simulation_sessions_completed': 0,
            'education_errors': 0
        }
        
        print("🎓 User Educator initialized!")
        print(f"   Education topics: {len(self.education_content)}")
        print(f"   Education level: {self.education_config['education_level']}")
        print(f"   Auto education: {self.education_config['auto_education']}")

    def start_education(self):
        """Start user education"""
        if self.education_active:
            return
        self.education_active = True
        self.education_thread = threading.Thread(target=self._education_loop, daemon=True)
        self.education_thread.start()
        print("🎓 User education started!")

    def stop_education(self):
        """Stop user education"""
        self.education_active = False
        if self.education_thread:
            self.education_thread.join(timeout=5)
        print("⏹️ User education stopped!")

    def _education_loop(self):
        """Main education loop"""
        while self.education_active:
            try:
                # Check for users who need education
                self._check_education_needs()
                time.sleep(self.education_config['education_interval'])
            except Exception as e:
                print(f"❌ Education loop error: {e}")
                self.education_stats['education_errors'] += 1
                time.sleep(self.education_config['education_interval'])

    def _check_education_needs(self):
        """Check for users who need education"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd check user profiles and education history
            
            # Simulate education needs checking
            pass
            
        except Exception as e:
            print(f"❌ Education needs check error: {e}")

    def educate_user(self, user_id: str, topic: str = None) -> Dict:
        """Educate a user on a specific topic"""
        try:
            if topic is None:
                topic = self._select_education_topic(user_id)
            
            if topic not in self.education_content:
                return {'error': f'Education topic not found: {topic}'}
            
            education_result = {
                'timestamp': time.time(),
                'user_id': user_id,
                'topic': topic,
                'education_content': self.education_content[topic],
                'education_completed': False,
                'quiz_completed': False,
                'simulation_completed': False,
                'education_score': 0,
                'recommendations': []
            }
            
            # Start education session
            self._start_education_session(user_id, topic)
            
            # Complete education session
            education_result['education_completed'] = True
            education_result['education_score'] = self._calculate_education_score(user_id, topic)
            
            # Generate recommendations
            education_result['recommendations'] = self._generate_education_recommendations(user_id, topic)
            
            # Store education result
            self.education_history.append(education_result)
            self.education_stats['education_sessions_completed'] += 1
            
            return education_result
            
        except Exception as e:
            return {'error': f'User education failed: {e}'}

    def _select_education_topic(self, user_id: str) -> str:
        """Select appropriate education topic for user"""
        try:
            # Get user's education history
            user_history = [e for e in self.education_history if e['user_id'] == user_id]
            
            # Select topic based on user's needs and history
            available_topics = list(self.education_content.keys())
            
            # If user has no history, start with phishing awareness
            if not user_history:
                return 'phishing_awareness'
            
            # Select topic based on user's progress
            completed_topics = [e['topic'] for e in user_history if e['education_completed']]
            remaining_topics = [t for t in available_topics if t not in completed_topics]
            
            if remaining_topics:
                return random.choice(remaining_topics)
            else:
                # All topics completed, select random topic for reinforcement
                return random.choice(available_topics)
                
        except Exception:
            return 'phishing_awareness'

    def _start_education_session(self, user_id: str, topic: str):
        """Start education session for user"""
        try:
            print(f"🎓 Starting education session for user {user_id} on topic: {topic}")
            
            # Initialize user progress if not exists
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {
                    'topics_completed': [],
                    'quiz_scores': {},
                    'simulation_scores': {},
                    'education_level': 'beginner',
                    'last_education': time.time()
                }
            
            # Update user progress
            self.user_progress[user_id]['last_education'] = time.time()
            
            print(f"✅ Education session started for user {user_id}")
            
        except Exception as e:
            print(f"❌ Education session start error: {e}")

    def _calculate_education_score(self, user_id: str, topic: str) -> int:
        """Calculate education score for user"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd calculate based on quiz results, engagement, etc.
            
            base_score = 75  # Base score for completing education
            
            # Add bonus for topic difficulty
            topic_difficulty = {
                'phishing_awareness': 10,
                'social_engineering': 15,
                'password_security': 10,
                'malware_awareness': 12,
                'data_protection': 18
            }
            
            bonus = topic_difficulty.get(topic, 10)
            total_score = min(base_score + bonus, 100)
            
            return total_score
            
        except Exception:
            return 75

    def _generate_education_recommendations(self, user_id: str, topic: str) -> List[str]:
        """Generate education recommendations for user"""
        try:
            recommendations = []
            
            # Get user's education history
            user_history = [e for e in self.education_history if e['user_id'] == user_id]
            
            # Generate topic-specific recommendations
            if topic == 'phishing_awareness':
                recommendations.extend([
                    'Practice identifying phishing emails',
                    'Report suspicious emails to IT',
                    'Be cautious with urgent requests',
                    'Verify sender information'
                ])
            elif topic == 'social_engineering':
                recommendations.extend([
                    'Be suspicious of unsolicited requests',
                    'Verify caller identity',
                    'Never share passwords',
                    'Report suspicious behavior'
                ])
            elif topic == 'password_security':
                recommendations.extend([
                    'Use strong, unique passwords',
                    'Enable two-factor authentication',
                    'Use a password manager',
                    'Change passwords regularly'
                ])
            elif topic == 'malware_awareness':
                recommendations.extend([
                    'Keep software updated',
                    'Use antivirus software',
                    'Be cautious with downloads',
                    'Scan removable media'
                ])
            elif topic == 'data_protection':
                recommendations.extend([
                    'Encrypt sensitive data',
                    'Use secure disposal methods',
                    'Limit data access',
                    'Monitor data usage'
                ])
            
            # Add general recommendations
            recommendations.extend([
                'Continue learning about cybersecurity',
                'Stay updated on latest threats',
                'Practice good security habits',
                'Report security incidents'
            ])
            
            return recommendations
            
        except Exception:
            return ['Continue learning about cybersecurity']

    def conduct_quiz(self, user_id: str, topic: str) -> Dict:
        """Conduct quiz for user on specific topic"""
        try:
            if topic not in self.education_content:
                return {'error': f'Education topic not found: {topic}'}
            
            quiz_result = {
                'timestamp': time.time(),
                'user_id': user_id,
                'topic': topic,
                'questions': self.education_content[topic]['quiz_questions'],
                'user_answers': [],
                'correct_answers': 0,
                'total_questions': len(self.education_content[topic]['quiz_questions']),
                'quiz_score': 0,
                'quiz_completed': False
            }
            
            # Simulate quiz completion
            quiz_result['quiz_completed'] = True
            quiz_result['correct_answers'] = random.randint(3, 5)  # Simulate random performance
            quiz_result['quiz_score'] = (quiz_result['correct_answers'] / quiz_result['total_questions']) * 100
            
            # Update user progress
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {
                    'topics_completed': [],
                    'quiz_scores': {},
                    'simulation_scores': {},
                    'education_level': 'beginner',
                    'last_education': time.time()
                }
            
            self.user_progress[user_id]['quiz_scores'][topic] = quiz_result['quiz_score']
            self.education_stats['quiz_sessions_completed'] += 1
            
            return quiz_result
            
        except Exception as e:
            return {'error': f'Quiz failed: {e}'}

    def conduct_simulation(self, user_id: str, simulation_type: str = 'phishing') -> Dict:
        """Conduct security simulation for user"""
        try:
            simulation_result = {
                'timestamp': time.time(),
                'user_id': user_id,
                'simulation_type': simulation_type,
                'simulation_scenarios': [],
                'user_responses': [],
                'correct_responses': 0,
                'total_scenarios': 0,
                'simulation_score': 0,
                'simulation_completed': False
            }
            
            # Generate simulation scenarios based on type
            if simulation_type == 'phishing':
                simulation_result['simulation_scenarios'] = self._generate_phishing_scenarios()
            elif simulation_type == 'social_engineering':
                simulation_result['simulation_scenarios'] = self._generate_social_engineering_scenarios()
            else:
                simulation_result['simulation_scenarios'] = self._generate_general_scenarios()
            
            simulation_result['total_scenarios'] = len(simulation_result['simulation_scenarios'])
            
            # Simulate user responses
            simulation_result['user_responses'] = [random.choice([True, False]) for _ in range(simulation_result['total_scenarios'])]
            simulation_result['correct_responses'] = sum(simulation_result['user_responses'])
            simulation_result['simulation_score'] = (simulation_result['correct_responses'] / simulation_result['total_scenarios']) * 100
            simulation_result['simulation_completed'] = True
            
            # Update user progress
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {
                    'topics_completed': [],
                    'quiz_scores': {},
                    'simulation_scores': {},
                    'education_level': 'beginner',
                    'last_education': time.time()
                }
            
            self.user_progress[user_id]['simulation_scores'][simulation_type] = simulation_result['simulation_score']
            self.education_stats['simulation_sessions_completed'] += 1
            
            return simulation_result
            
        except Exception as e:
            return {'error': f'Simulation failed: {e}'}

    def _generate_phishing_scenarios(self) -> List[Dict]:
        """Generate phishing simulation scenarios"""
        return [
            {
                'scenario': 'You receive an email claiming to be from your bank asking you to verify your account.',
                'correct_response': False,
                'explanation': 'Banks never ask for account verification via email.'
            },
            {
                'scenario': 'You receive an email with a link to a website you recognize.',
                'correct_response': False,
                'explanation': 'Always verify the sender and be cautious with links.'
            },
            {
                'scenario': 'You receive an email asking you to download an attachment for a security update.',
                'correct_response': False,
                'explanation': 'Never download attachments from unsolicited emails.'
            },
            {
                'scenario': 'You receive an email with urgent language asking you to act immediately.',
                'correct_response': False,
                'explanation': 'Urgent language is a common phishing tactic.'
            },
            {
                'scenario': 'You receive an email from a known contact asking for sensitive information.',
                'correct_response': False,
                'explanation': 'Always verify requests for sensitive information through a separate channel.'
            }
        ]

    def _generate_social_engineering_scenarios(self) -> List[Dict]:
        """Generate social engineering simulation scenarios"""
        return [
            {
                'scenario': 'Someone calls claiming to be from IT support asking for your password.',
                'correct_response': False,
                'explanation': 'IT support never asks for passwords over the phone.'
            },
            {
                'scenario': 'A colleague asks you to share your login credentials for a project.',
                'correct_response': False,
                'explanation': 'Never share login credentials with anyone.'
            },
            {
                'scenario': 'Someone approaches you in the parking lot asking for help with their computer.',
                'correct_response': False,
                'explanation': 'Be cautious of unsolicited requests for help.'
            },
            {
                'scenario': 'You receive a call from someone claiming to be from HR asking for personal information.',
                'correct_response': False,
                'explanation': 'Always verify the identity of callers before sharing information.'
            },
            {
                'scenario': 'Someone asks you to install software on your work computer.',
                'correct_response': False,
                'explanation': 'Never install software without proper authorization.'
            }
        ]

    def _generate_general_scenarios(self) -> List[Dict]:
        """Generate general security scenarios"""
        return [
            {
                'scenario': 'You find a USB drive in the parking lot.',
                'correct_response': False,
                'explanation': 'Never use found USB drives as they may contain malware.'
            },
            {
                'scenario': 'You receive a text message with a link to a website.',
                'correct_response': False,
                'explanation': 'Be cautious with links in text messages.'
            },
            {
                'scenario': 'You are asked to provide your social security number over the phone.',
                'correct_response': False,
                'explanation': 'Never provide sensitive information over the phone.'
            },
            {
                'scenario': 'You are asked to click on a link in an email to verify your account.',
                'correct_response': False,
                'explanation': 'Always verify the sender and be cautious with links.'
            },
            {
                'scenario': 'You are asked to download software from an unknown website.',
                'correct_response': False,
                'explanation': 'Only download software from trusted sources.'
            }
        ]

    def get_user_progress(self, user_id: str) -> Dict:
        """Get user's education progress"""
        try:
            if user_id not in self.user_progress:
                return {'error': 'User not found'}
            
            user_progress = self.user_progress[user_id].copy()
            
            # Calculate overall progress
            total_topics = len(self.education_content)
            completed_topics = len(user_progress['topics_completed'])
            user_progress['overall_progress'] = (completed_topics / total_topics) * 100
            
            # Calculate average quiz score
            quiz_scores = list(user_progress['quiz_scores'].values())
            if quiz_scores:
                user_progress['average_quiz_score'] = sum(quiz_scores) / len(quiz_scores)
            else:
                user_progress['average_quiz_score'] = 0
            
            # Calculate average simulation score
            simulation_scores = list(user_progress['simulation_scores'].values())
            if simulation_scores:
                user_progress['average_simulation_score'] = sum(simulation_scores) / len(simulation_scores)
            else:
                user_progress['average_simulation_score'] = 0
            
            return user_progress
            
        except Exception as e:
            return {'error': f'Failed to get user progress: {e}'}

    def get_education_statistics(self) -> Dict:
        """Get education statistics"""
        return {
            'education_active': self.education_active,
            'users_educated': len(self.user_progress),
            'education_sessions_completed': self.education_stats['education_sessions_completed'],
            'quiz_sessions_completed': self.education_stats['quiz_sessions_completed'],
            'simulation_sessions_completed': self.education_stats['simulation_sessions_completed'],
            'education_errors': self.education_stats['education_errors'],
            'education_history_size': len(self.education_history),
            'education_topics': len(self.education_content)
        }

    def get_recent_education_sessions(self, count: int = 10) -> List[Dict]:
        """Get recent education sessions"""
        return list(self.education_history)[-count:]

    def update_education_config(self, config: Dict):
        """Update education configuration"""
        try:
            self.education_config.update(config)
            print(f"✅ Education configuration updated")
        except Exception as e:
            print(f"❌ Configuration update error: {e}")

    def add_education_content(self, topic: str, content: Dict):
        """Add new education content"""
        try:
            self.education_content[topic] = content
            print(f"✅ Education content added: {topic}")
        except Exception as e:
            print(f"❌ Content addition error: {e}")

    def emergency_education_activation(self):
        """Emergency education activation"""
        try:
            print("🚨 EMERGENCY EDUCATION ACTIVATION!")
            
            # Activate all education modules
            print("🎓 Activating all education modules...")
            
            # Send urgent education notifications
            print("📢 Sending urgent education notifications...")
            
            # Increase education frequency
            self.education_config['education_interval'] = 1800  # 30 minutes
            self.education_config['quiz_interval'] = 3600  # 1 hour
            self.education_config['simulation_interval'] = 86400  # 1 day
            
            print("✅ Emergency education activation completed!")
            
        except Exception as e:
            print(f"❌ Emergency education activation error: {e}")

    def restore_normal_education(self):
        """Restore normal education operation"""
        try:
            print("✅ Restoring normal education operation...")
            
            # Restore normal education intervals
            self.education_config['education_interval'] = 3600  # 1 hour
            self.education_config['quiz_interval'] = 86400  # 1 day
            self.education_config['simulation_interval'] = 604800  # 1 week
            
            print("✅ Normal education operation restored!")
            
        except Exception as e:
            print(f"❌ Education restoration error: {e}")
