import unittest
from other.email_templates import (
    family_friends_template_labelled,
    work_template_labelled,
    phishing_template_labelled
)

class TestEmailTemplates(unittest.TestCase):
    def test_family_friends_template(self):
        email = family_friends_template_labelled()
        self.assertEqual(email['category'], 'family_friends')
        self.assertFalse(email['features']['contains_suspicious_link'])
        self.assertFalse(email['features']['mismatched_display_name'])
        self.assertFalse(email['features']['urgent_language'])
        self.assertFalse(email['features']['suspicious_attachment'])

    def test_work_template(self):
        email = work_template_labelled()
        self.assertEqual(email['category'], 'work')
        self.assertFalse(email['features']['contains_suspicious_link'])
        self.assertFalse(email['features']['mismatched_display_name'])
        self.assertIsInstance(email['features']['urgent_language'], bool)
        self.assertFalse(email['features']['suspicious_attachment'])

    def test_phishing_template(self):
        email = phishing_template_labelled()
        self.assertEqual(email['category'], 'phishing')
        self.assertTrue(email['features']['contains_suspicious_link'])
        self.assertTrue(email['features']['mismatched_display_name'])
        self.assertIsInstance(email['features']['urgent_language'], bool)


if __name__ == '__main__':
    unittest.main()