from unittest import TestCase

from assertions import assert_result, assert_result_within_score_range
from analyzer.predefined_recognizers import SpacyRecognizer

NER_STRENGTH = 0.85
spacy_recognizer = SpacyRecognizer()
entities = ["PERSON", "DATE_TIME"]


class TestSpacyRecognizer(TestCase):

    # Test Name Entity
    # Bug #617 : Spacy Recognizer doesn't recognize Dan as PERSON even though
    # online spacy demo indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_person_first_name(self):
    #     name = 'Dan'
    #     results = spacy_recognizer.analyze(name, entities)

    #     assert len(results) == 1
    #     assert_result(results[0], entity[0], NER_STRENGTH)

    def test_person_first_name_with_context(self):
        name = 'Dan'
        context = 'my name is'
        results = spacy_recognizer.analyze(
            '{} {}'.format(context, name), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[0], 11, 14, NER_STRENGTH, 1)

    def test_person_full_name(self):
        name = 'Dan Tailor'
        results = spacy_recognizer.analyze(name, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 10, NER_STRENGTH)

    def test_person_full_name_with_context(self):
        name = 'John Oliver'
        context = ' is the funniest comedian'
        results = spacy_recognizer.analyze(
            '{} {}'.format(name, context), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[0], 0, 11, NER_STRENGTH, 1)

    def test_person_last_name(self):
        name = 'Tailor'
        results = spacy_recognizer.analyze(name, entities)

        assert not results

    # Bug #617 : Spacy Recognizer doesn't recognize Mr. Tailor as PERSON even
    # though online spacy visualizer indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_person_title_with_last_name(self):
    #     name = 'Mr. Tailor'
    #     results = spacy_recognizer.analyze(name, entities)

    #     assert len(results) == 1
    #     assert_result(results[0], entities[0], 0, 9, NER_STRENGTH)

    # Bug #617 : Spacy Recognizer doesn't recognize Mr. Tailor as PERSON even
    # though online spacy visualizer indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_person_title_with_last_name_with_context_and_time(self):
    #     name = 'Mr. Tailor'
    #     context = 'Good morning'
    #     results = spacy_recognizer.analyze(
    #       '{} {}'.format(context, name), entities)

    #     assert len(results) == 2
    #     assert_result_within_score_range(
    #       results[1], entities[1], 5, 12, NER_STRENGTH, 1)
    #     assert_result_within_score_range(
    #       results[0], entities[0], 17, 23, NER_STRENGTH, 1)

    def test_person_full_middle_name(self):
        name = 'Richard Milhous Nixon'
        results = spacy_recognizer.analyze(name, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 21, NER_STRENGTH)

    def test_person_full_name_with_middle_letter(self):
        name = 'Richard M. Nixon'
        results = spacy_recognizer.analyze(name, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 16, NER_STRENGTH)

    def test_person_full_name_complex(self):
        name = 'Richard (Ric) C. Henderson'
        results = spacy_recognizer.analyze(name, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 26, NER_STRENGTH)

    def test_person_last_name_is_also_a_date_expected_person_only(self):
        name = 'Dan May'
        results = spacy_recognizer.analyze(name, entities)

        assert len(results) == 1
        assert_result(results[0], entities[0], 0, 7, NER_STRENGTH, )

    # Bug #617 : Spacy Recognizer doesn't recognize Dan May as PERSON even
    # though online spacy demo indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    def test_person_last_name_is_a_date_with_context_expected_person(self):
        name = 'Dan May'
        context = "has a bank account"
        results = spacy_recognizer.analyze(
            '{} {}'.format(name, context), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[0], 0, 7, NER_STRENGTH, 1)

    # Bug #617 : Spacy Recognizer doesn't recognize Mr. May as PERSON even
    # though online spacy demo indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_person_title_and_last_name_is_also_a_date_expected_person(self):
    #     name = 'Mr. May'
    #     results = spacy_recognizer.analyze(name, entities)

    #     assert len(results) == 1
    #     assert_result(results[0], entities[0], 4, 7, NER_STRENGTH)

    # Bug #617 : Spacy Recognizer doesn't recognize Mr. May as PERSON even
    # though online spacy demo indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_person_title_and_last_name_is_a_date_with_context_expected_
    # person_only(self):
    #     name = 'Mr. May'
    #     context = "They call me"
    #     results = spacy_recognizer.analyze(
    # '{} {}'.format(context, name), entities)

    #     assert len(results) == 1
    #     assert_result_within_score_range(
    # results[0], entities[0], 17, 20, NER_STRENGTH, 1)

# Test DATE_TIME Entity
    def test_date_time_year(self):
        date = '1972'
        results = spacy_recognizer.analyze(date, entities)

        assert len(results) == 1
        assert_result(results[0], entities[1], 0, 4, NER_STRENGTH)

    def test_date_time_year_with_context(self):
        date = '1972'
        context = 'I bought my car in'
        results = spacy_recognizer.analyze(
            '{} {}'.format(context, date), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 19, 23, NER_STRENGTH, 1)

    # Bug #617 : Spacy Recognizer doesn't recognize May as DATE_TIME even
    # though online spacy demo indicates that it does
    # See http://textanalysisonline.com/spacy-named-entity-recognition-ner
    # def test_date_time_month(self):
    #     date = 'May'
    #     results = spacy_recognizer.analyze(date, entities)

    #     assert len(results) == 1
    #     assert_result_within_score_range(
    #       results[0], entities[1], 0, 3, NER_STRENGTH, 1)

    def test_date_time_month_with_context(self):
        date = 'May'
        context = 'I bought my car in'
        results = spacy_recognizer.analyze(
            '{} {}'.format(context, date), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 19, 22, NER_STRENGTH, 1)

    def test_date_time_day_in_month(self):
        date = 'May 1st'
        results = spacy_recognizer.analyze(date, entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 0, 7, NER_STRENGTH, 1)

    def test_date_time_day_in_month_with_context(self):
        date = 'May 1st'
        context = 'I bought my car on '
        results = spacy_recognizer.analyze(
            '{} {}'.format(context, date), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 19, 26, NER_STRENGTH, 1)

    def test_date_time_full_date(self):
        date = 'May 1st, 1977'
        results = spacy_recognizer.analyze(date, entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 0, 13, NER_STRENGTH, 1)

    def test_full_date_time_with_context(self):
        date = 'May 1st, 1977'
        context = 'I bought my car on'
        results = spacy_recognizer.analyze(
            '{} {}'.format(context, date), entities)

        assert len(results) == 1
        assert_result_within_score_range(
            results[0], entities[1], 19, 32, NER_STRENGTH, 1)