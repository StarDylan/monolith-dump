import unittest
from main import is_exact_subdomain_match

class TestExactSubdomainMatch(unittest.TestCase):

    def test_same_subdomain(self):
        self.assertTrue(is_exact_subdomain_match("https://blog.example.com", "https://blog.example.com"))
        self.assertTrue(is_exact_subdomain_match("https://blog.example.com", "https://blog.example.com/page"))

    def test_different_subdomains(self):
        self.assertFalse(is_exact_subdomain_match("https://blog.example.com", "https://cdn.example.com"))
        self.assertFalse(is_exact_subdomain_match("https://blog.example.com", "https://example.com"))
        self.assertFalse(is_exact_subdomain_match("https://blog.example.com", "https://shop.blog.example.com"))

    def test_same_domain_different_scheme(self):
        self.assertTrue(is_exact_subdomain_match("http://blog.example.com", "https://blog.example.com"))

    def test_case_insensitivity(self):
        self.assertTrue(is_exact_subdomain_match("https://Blog.Example.Com", "https://blog.example.com"))

    def test_query_and_fragment_ignored(self):
        self.assertTrue(is_exact_subdomain_match("https://blog.example.com", "https://blog.example.com/page?x=1#top"))

    def test_with_port(self):
        self.assertTrue(is_exact_subdomain_match("https://blog.example.com", "https://blog.example.com:443"))
        self.assertTrue(is_exact_subdomain_match("https://blog.example.com:443", "https://blog.example.com"))

    def test_invalid_urls(self):
        self.assertFalse(is_exact_subdomain_match("not-a-url", "https://blog.example.com"))
        self.assertFalse(is_exact_subdomain_match("https://blog.example.com", "also-not-a-url"))

if __name__ == "__main__":
    unittest.main()
