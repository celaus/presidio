from unittest import TestCase

from assertions import assert_result
from analyzer.predefined_recognizers import DomainRecognizer

domain_recognizer = DomainRecognizer()
entities = ["DOMAIN_NAME"]


class TestDomainRecognizer(TestCase):

    def test_invalid_domain(self):
        domain = 'microsoft.'
        results = domain_recognizer.analyze(domain, entities)

        assert not results

    def test_invalid_domain_with_exact_context(self):
        domain = 'microsoft.'
        context = 'my domain is '
        results = domain_recognizer.analyze(context + domain, entities)

        assert not results

    def test_valid_domain(self):
        domain = 'microsoft.com'
        results = domain_recognizer.analyze(domain, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 13, 1.0)

    def test_valid_domains_lemma_text(self):
        domain1 = 'microsoft.com'
        domain2 = '192.168.0.1'
        results = domain_recognizer.analyze(
            'my domains: {} {}'.format(domain1, domain2), entities)

        assert len(results) == 2
        assert_result(results[0], entities[0], 12, 25, 1.0)
        assert_result(results[1], entities[0], 26, 33, 0)
