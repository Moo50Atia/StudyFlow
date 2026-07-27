"""
Unit & Integration Test Suite for KOS Kernel and KIE Components
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import unittest
from src.kos.core.config_runtime import ConfigurationRuntime
from src.kos.core.di_container import DependencyInjectionContainer
from src.kos.core.event_bus import EventBus, KOSEvent
from src.kos.security.tenant_isolation import TenantIsolationEngine, TenantIsolationError
from src.kos.security.permission_engine import PermissionEngine
from src.kie.search.query_analyzer import QueryAnalyzer
from src.kie.policy.confidence_engine import PolicyConfidenceEngine


class TestKOSKernel(unittest.TestCase):

    def test_config_runtime(self):
        config_rt = ConfigurationRuntime()
        self.assertEqual(config_rt.config.environment, "development")

    def test_di_container(self):
        container = DependencyInjectionContainer.get_instance()
        container.register_singleton(str, "test_instance")
        self.assertEqual(container.resolve(str), "test_instance")

    def test_event_bus(self):
        bus = EventBus()
        received = []
        bus.subscribe("TEST_EVENT", lambda e: received.append(e.payload))
        bus.publish(KOSEvent(event_id="e1", event_name="TEST_EVENT", payload={"data": 123}))
        self.assertEqual(len(received), 1)

    def test_tenant_isolation(self):
        self.assertTrue(TenantIsolationEngine.validate_access("t1", "t1", "res1"))
        with self.assertRaises(TenantIsolationError):
            TenantIsolationEngine.validate_access("t1", "t2", "res1")

    def test_query_analyzer(self):
        analyzer = QueryAnalyzer()
        intent = analyzer.classify_intent("What is Newton's Second Law?")
        self.assertEqual(intent, "INTENT_DEF")

    def test_confidence_engine(self):
        engine = PolicyConfidenceEngine()
        res = engine.evaluate_confidence([])
        self.assertEqual(res["confidence_band"], "UNSUPPORTED")
        self.assertTrue(res["should_abstain"])


if __name__ == "__main__":
    unittest.main()
