from unittest import TestCase

import balance


class PayloadTestDouble:
    def __init__(self, content = "Lorem|Ipsum|"):
        self.text = content

    def render(self):
        return self.text
    
    def __str__(self):
        return self.render()


class TestRecord(TestCase):
    def setUp(self):
        self.payload = PayloadTestDouble()

    def test_record_created_when_params_supplied(self):
        order = 1
        record = balance.Record(order, self.payload)
        self.assertIsInstance(record, balance.Record)
    
    def test_record_rejects_large_row_numbers(self):
        order = 100_000
        with self.assertRaises(ValueError):
            balance.Record(order, self.payload)
    
    def test_record_checksum_calculates_correctly_in_standard_case(self):
        order = 85
        record = balance.Record(order, self.payload)
        self.assertEqual(1638, record.checksum)

    def test_record_raises_error_for_empty_payload(self):
        order = 85
        with self.assertRaises(ValueError):
            balance.Record(order, "")

class TestPosition(TestCase):
    pass
    # TODO: make some test cases for Position