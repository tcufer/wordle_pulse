from unittest import expectedFailure
import pytest
import json
from src.tweet_parser import TweetParser


class TestClass():

    def test_default_text(self):
        default_text = "Wordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩"
        tweet_parser = TweetParser(default_text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result["attempts_count"] == 4

    def test_numericized_result_with_default_text(self):
        default_text = "Wordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩"
        tweet_parser = TweetParser(default_text)
        parsed_result = json.loads(tweet_parser.perform())
        expected_result = {
            "1": [0, 1, 0, 0, 2],
            "2": [2, 0, 1, 0, 2],
            "3": [2, 1, 1, 0, 2],
            "4": [2, 2, 2, 2, 2]
        }

        assert parsed_result["attempts"] == expected_result

    def test_with_text_before_and_after(self):
        text = "test test Wordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩test test"
        tweet_parser = TweetParser(text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result["attempts_count"] == 4
        assert parsed_result["wordle_id"] == "255"

    def test_wordle_title(self):
        text = "Wordle (ES) #30 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩"
        tweet_parser = TweetParser(text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result == {}

    def test_text_with_two_results_but_different(self):
        text = "Besedle 20 3/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟩🟩🟩🟩\nWordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩"
        tweet_parser = TweetParser(text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result["attempts_count"] == 4
        assert parsed_result["wordle_id"] == "255"

    def test_text_with_two_results_but_different_2(self):
        text = "Wordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩🟩🟩🟩\nBesedle 20 3/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟩🟩🟩🟩"
        tweet_parser = TweetParser(text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result["attempts_count"] == 4
        assert parsed_result["wordle_id"] == "255"

    def test_text_with_included_other_emojis(self):
        text = "Wordle 255 4/6\n\n⬛🟨⬛⬛🟩\n🟩⬛🟨⬛🟩\n🟩🟨🟨⬛🟩\n🟩🟩💩🟩🟩"
        tweet_parser = TweetParser(text)
        parsed_result = json.loads(tweet_parser.perform())

        assert parsed_result == {}
