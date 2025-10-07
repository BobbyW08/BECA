"""
Autonomous Learning System for BECA
Runs in background, continuously learning without user prompts
"""
import threading
import time
import json
from datetime import datetime
from typing import List, Dict
import logging

from knowledge_system import knowledge_base, WebDocScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] BECA Learning: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('BECA-Learning')


class AutonomousLearner:
    """
    Background learning system that continuously improves BECA's knowledge
    """

    def __init__(self):
        self.learning_active = False
        self.learning_thread = None
        self.learned_count = 0

        # Curated learning curriculum - high-quality resources
        self.curriculum = [
            # Python Essentials
            {
                'url': 'https://docs.python.org/3/library/asyncio.html',
                'category': 'python',
                'priority': 0.9,
                'tags': ['python', 'async', 'concurrency']
            },
            {
                'url': 'https://docs.python.org/3/library/typing.html',
                'category': 'python',
                'priority': 0.8,
                'tags': ['python', 'typing', 'best-practices']
            },

            # Web Frameworks
            {
                'url': 'https://fastapi.tiangolo.com/',
                'category': 'web-framework',
                'priority': 0.9,
                'tags': ['fastapi', 'api', 'web']
            },
            {
                'url': 'https://flask.palletsprojects.com/',
                'category': 'web-framework',
                'priority': 0.7,
                'tags': ['flask', 'api', 'web']
            },

            # AI/ML Frameworks
            {
                'url': 'https://pytorch.org/docs/stable/index.html',
                'category': 'ai-ml',
                'priority': 0.9,
                'tags': ['pytorch', 'ml', 'deep-learning']
            },
            {
                'url': 'https://huggingface.co/docs/transformers/index',
                'category': 'ai-ml',
                'priority': 0.95,
                'tags': ['transformers', 'llm', 'nlp']
            },
            {
                'url': 'https://python.langchain.com/docs/get_started/introduction',
                'category': 'ai-framework',
                'priority': 0.9,
                'tags': ['langchain', 'llm', 'agents']
            },

            # AI Model Training
            {
                'url': 'https://huggingface.co/docs/transformers/training',
                'category': 'ai-training',
                'priority': 0.95,
                'tags': ['fine-tuning', 'training', 'ml']
            },
            {
                'url': 'https://huggingface.co/docs/peft/index',
                'category': 'ai-training',
                'priority': 0.9,
                'tags': ['lora', 'peft', 'fine-tuning']
            },

            # JavaScript/Frontend
            {
                'url': 'https://react.dev/learn',
                'category': 'frontend',
                'priority': 0.8,
                'tags': ['react', 'frontend', 'javascript']
            },
            {
                'url': 'https://nodejs.org/docs/latest/api/',
                'category': 'backend',
                'priority': 0.7,
                'tags': ['nodejs', 'javascript', 'backend']
            },

            # DevOps & Tools
            {
                'url': 'https://docs.docker.com/get-started/',
                'category': 'devops',
                'priority': 0.8,
                'tags': ['docker', 'containers', 'devops']
            },
            {
                'url': 'https://git-scm.com/doc',
                'category': 'version-control',
                'priority': 0.7,
                'tags': ['git', 'version-control']
            },

            # Testing
            {
                'url': 'https://docs.pytest.org/en/stable/',
                'category': 'testing',
                'priority': 0.8,
                'tags': ['pytest', 'testing', 'python']
            },

            # Databases
            {
                'url': 'https://www.postgresql.org/docs/',
                'category': 'database',
                'priority': 0.7,
                'tags': ['postgresql', 'database', 'sql']
            },
        ]

        # GitHub repos to clone and analyze
        self.repos_to_learn = [
            {
                'url': 'https://github.com/tiangolo/fastapi',
                'name': 'FastAPI',
                'priority': 0.9,
                'focus': 'Modern Python web framework architecture'
            },
            {
                'url': 'https://github.com/langchain-ai/langchain',
                'name': 'LangChain',
                'priority': 0.95,
                'focus': 'LLM application framework patterns'
            },
            {
                'url': 'https://github.com/huggingface/transformers',
                'name': 'Transformers',
                'priority': 0.9,
                'focus': 'ML model implementation patterns'
            },
        ]

    def start(self):
        """Start autonomous learning in background"""
        if self.learning_active:
            logger.info("Autonomous learning already active")
            return

        self.learning_active = True
        self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.learning_thread.start()
        logger.info("🚀 Autonomous learning system activated!")

    def stop(self):
        """Stop autonomous learning"""
        self.learning_active = False
        if self.learning_thread:
            self.learning_thread.join(timeout=5)
        logger.info("Autonomous learning system stopped")

    def _learning_loop(self):
        """Main learning loop that runs in background"""

        # Phase 1: Learn from curriculum (documentation)
        logger.info("📚 Phase 1: Learning from documentation curriculum...")
        self._learn_from_curriculum()

        # Phase 2: Check learning queue and process pending items
        logger.info("📖 Phase 2: Processing learning queue...")
        self._process_learning_queue()

        # Phase 3: Periodic knowledge refresh (runs continuously)
        logger.info("🔄 Phase 3: Entering continuous learning mode...")
        while self.learning_active:
            try:
                # Every hour, learn something new from the queue
                self._learn_next_queued_item()

                # Every 6 hours, refresh knowledge from high-priority sources
                if self.learned_count % 6 == 0:
                    self._refresh_knowledge()

                # Sleep for 1 hour between learning sessions
                time.sleep(3600)

            except Exception as e:
                logger.error(f"Error in learning loop: {e}")
                time.sleep(300)  # Sleep 5 minutes on error

    def _learn_from_curriculum(self):
        """Learn from the curated curriculum"""
        logger.info(f"📚 Starting curriculum learning ({len(self.curriculum)} resources)...")

        # Sort by priority
        sorted_curriculum = sorted(self.curriculum, key=lambda x: x['priority'], reverse=True)

        for i, item in enumerate(sorted_curriculum[:5], 1):  # Learn top 5 first
            if not self.learning_active:
                break

            try:
                logger.info(f"📖 [{i}/5] Learning from {item['url']}...")

                doc = WebDocScraper.fetch_and_parse(item['url'])

                if 'Failed to fetch' not in doc['content']:
                    knowledge_base.add_documentation(
                        source=item['url'].split('/')[2],
                        url=item['url'],
                        title=doc['title'],
                        content=doc['content'],
                        category=item['category'],
                        tags=item.get('tags', [])
                    )

                    # Also add to learning resources for reference
                    knowledge_base.add_learning_resource(
                        resource_type='documentation',
                        title=doc['title'],
                        url=item['url'],
                        topics=item.get('tags', []),
                        priority=item['priority']
                    )

                    logger.info(f"   ✅ Learned: {doc['title']}")
                    self.learned_count += 1
                else:
                    logger.warning(f"   ⚠️  Failed to fetch: {item['url']}")

                # Small delay between requests to be respectful
                time.sleep(2)

            except Exception as e:
                logger.error(f"   ❌ Error learning from {item['url']}: {e}")

        logger.info(f"✅ Curriculum learning complete! Learned from {self.learned_count} sources")

    def _process_learning_queue(self):
        """Process items in the learning queue"""
        try:
            queue = knowledge_base.get_learning_queue(limit=10, status='pending')

            if not queue:
                logger.info("📋 Learning queue is empty")
                return

            logger.info(f"📋 Processing {len(queue)} items from learning queue...")

            for i, item in enumerate(queue[:3], 1):  # Process top 3
                if not self.learning_active:
                    break

                try:
                    logger.info(f"📖 [{i}/3] Learning: {item['title']}...")

                    doc = WebDocScraper.fetch_and_parse(item['url'])

                    if 'Failed to fetch' not in doc['content']:
                        knowledge_base.add_documentation(
                            source=item['url'].split('/')[2],
                            url=item['url'],
                            title=doc['title'],
                            content=doc['content'],
                            category='learning-queue',
                            tags=item['topics']
                        )

                        # Mark as learned
                        knowledge_base.mark_resource_learned(item['id'])

                        logger.info(f"   ✅ Completed: {item['title']}")
                        self.learned_count += 1
                    else:
                        logger.warning(f"   ⚠️  Failed to fetch: {item['url']}")

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"   ❌ Error processing queue item: {e}")

        except Exception as e:
            logger.error(f"Error processing learning queue: {e}")

    def _learn_next_queued_item(self):
        """Learn from the next item in the queue"""
        try:
            queue = knowledge_base.get_learning_queue(limit=1, status='pending')

            if queue:
                item = queue[0]
                logger.info(f"🎓 Auto-learning: {item['title']}...")

                doc = WebDocScraper.fetch_and_parse(item['url'])

                if 'Failed to fetch' not in doc['content']:
                    knowledge_base.add_documentation(
                        source=item['url'].split('/')[2],
                        url=item['url'],
                        title=doc['title'],
                        content=doc['content'],
                        category='auto-learning',
                        tags=item['topics']
                    )

                    knowledge_base.mark_resource_learned(item['id'])
                    logger.info(f"   ✅ Auto-learned: {item['title']}")
                    self.learned_count += 1

        except Exception as e:
            logger.error(f"Error in auto-learning: {e}")

    def _refresh_knowledge(self):
        """Periodically refresh knowledge from high-priority sources"""
        logger.info("🔄 Refreshing high-priority knowledge...")

        high_priority = [item for item in self.curriculum if item['priority'] >= 0.9]

        for item in high_priority[:2]:  # Refresh top 2
            try:
                doc = WebDocScraper.fetch_and_parse(item['url'])

                if 'Failed to fetch' not in doc['content']:
                    # Update existing documentation
                    knowledge_base.add_documentation(
                        source=item['url'].split('/')[2],
                        url=item['url'],
                        title=doc['title'],
                        content=doc['content'],
                        category=item['category'],
                        tags=item.get('tags', [])
                    )

                    logger.info(f"   ✅ Refreshed: {doc['title']}")

                time.sleep(2)

            except Exception as e:
                logger.error(f"   ❌ Error refreshing: {e}")

    def get_stats(self) -> Dict:
        """Get learning statistics"""
        return {
            'active': self.learning_active,
            'total_learned': self.learned_count,
            'curriculum_size': len(self.curriculum),
            'repos_to_learn': len(self.repos_to_learn)
        }


# Global instance
autonomous_learner = AutonomousLearner()


def start_autonomous_learning():
    """Start the autonomous learning system"""
    autonomous_learner.start()


def stop_autonomous_learning():
    """Stop the autonomous learning system"""
    autonomous_learner.stop()


def get_learning_stats():
    """Get current learning statistics"""
    return autonomous_learner.get_stats()
