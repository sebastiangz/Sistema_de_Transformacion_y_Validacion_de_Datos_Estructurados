import unittest
from src.pipeline import ValidationPipeline
from src.parsers import parse_json, parse_csv, parse_xml, map_parser
from src.types import Success, Failure
from src.transforms import compose, uppercase_name
from src.validation import validate_user

class TestProject(unittest.TestCase):
    def setUp(self):
        self.user = {'name': '  Ana  López ', 'email': ' ANA@EXAMPLE.COM ', 'age': 23, 'tags': [' VIP ']}

    def test_success(self):
        result = ValidationPipeline().run(self.user)
        self.assertIsInstance(result, Success)
        self.assertEqual(result.value['name'], 'ANA LÓPEZ')
        self.assertEqual(result.value['email'], 'ana@example.com')
        self.assertEqual(result.value['tags'], ['vip'])

    def test_immutable(self):
        ValidationPipeline().run(self.user)
        self.assertEqual(self.user['name'], '  Ana  López ')

    def test_age_invalid(self):
        self.assertIsInstance(ValidationPipeline().run({**self.user, 'age': 15}), Failure)

    def test_email_invalid(self):
        self.assertIsInstance(validate_user({**self.user, 'email': 'no-es-correo'}), Failure)

    def test_missing(self):
        self.assertIsInstance(validate_user({'name': 'Ana'}), Failure)

    def test_json(self):
        self.assertIsInstance(parse_json('{"age":20}'), Success)
        self.assertIsInstance(parse_json('{mal}'), Failure)

    def test_csv(self):
        self.assertEqual(parse_csv('name,age\nAna,20').value[0]['name'], 'Ana')

    def test_xml(self):
        self.assertEqual(parse_xml('<user><name>Ana</name></user>').value['name'], 'Ana')

    def test_csv_coercion(self):
        result = ValidationPipeline().run({'name': 'Ana', 'email': 'ana@ejemplo.com', 'age': '20'})
        self.assertEqual(result.value['age'], 20)

    def test_many_errors(self):
        result = ValidationPipeline().run_many([self.user, {'name': 'Ana'}])
        self.assertIsInstance(result, Failure)
        self.assertIn('Registro 2', result.errors[0])

    def test_composition(self):
        f = compose(lambda x: x + 2, lambda x: x * 3)
        self.assertEqual(f(4), 14)

    def test_parser_combinator(self):
        parsed = map_parser(parse_json, lambda obj: obj['x'] * 2)('{"x":3}')
        self.assertEqual(parsed.value, 6)

    def test_railway(self):
        self.assertEqual(Failure(('error',)).map(lambda _: 1).errors, ('error',))

if __name__ == '__main__':
    unittest.main()
