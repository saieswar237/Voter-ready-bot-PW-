import unittest
from bot_logic import VoterBot

class MockAPIHandler:
    """
    Mock API Handler that returns predefined intents based on the test case.
    """
    def __init__(self):
        self.next_response = {}

    def set_next_response(self, response: dict):
        self.next_response = response

    def analyze_intent(self, user_input: str, context: str) -> dict:
        return self.next_response

class TestVoterBotLogic(unittest.TestCase):
    def setUp(self):
        self.api = MockAPIHandler()
        self.bot = VoterBot(self.api)

    def test_initial_greeting(self):
        response = self.bot.run_step()
        self.assertEqual(self.bot.state, "READINESS_CHECK")
        self.assertIn("Welcome to the Voter-Ready Bot", response)

    def test_branch_a_no_epic_first_time(self):
        # 1. Initial
        self.bot.run_step()
        
        # 2. User says No to EPIC
        self.api.set_next_response({"has_epic": False, "confidence": 0.99})
        response = self.bot.run_step("I don't have one")
        self.assertEqual(self.bot.state, "DOCUMENT_ASSISTANT")
        self.assertIn("first-time voter", response)

        # 3. User says First Time
        self.api.set_next_response({"status": "first_time"})
        response = self.bot.run_step("first time")
        self.assertEqual(self.bot.state, "END")
        self.assertIn("Form 6", response)

    def test_branch_a_no_epic_address_change(self):
        self.bot.run_step()
        
        self.api.set_next_response({"has_epic": False, "confidence": 0.99})
        self.bot.run_step("no")

        self.api.set_next_response({"status": "address_change"})
        response = self.bot.run_step("I moved to a new city")
        self.assertEqual(self.bot.state, "END")
        self.assertIn("Form 8", response)

    def test_branch_b_has_epic(self):
        self.bot.run_step()
        
        self.api.set_next_response({"has_epic": True, "confidence": 0.99})
        response = self.bot.run_step("Yes I have my voter id")
        
        self.assertEqual(self.bot.state, "END")
        self.assertIn("step-by-step walkthrough", response)
        self.assertIn("First Polling Officer", response)

if __name__ == '__main__':
    unittest.main()
