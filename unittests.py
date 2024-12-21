import unittest
import yaml
import os
import tempfile
from io import StringIO
import math

# Импортируем функции из вашего основного файла
from hw3 import parse_yaml, evaluate_expression, transform_to_custom_syntax

class TestYamlParser(unittest.TestCase):

    def test_parse_yaml_valid(self):
        yaml_content = """
        Max_value: 100
        Min_value: 0
        Threshold: 50
        Expressions:
          Sum: 'Max_value + Threshold'
          Sub: 'Max_value - Min_value'
          Sqrt: 'sqrt(16)'
          Max: 'max(10, 20)'
        """
        # Используем временный файл для хранения YAML-содержимого
        with tempfile.NamedTemporaryFile(delete=False, suffix='.yaml') as temp_file:
            temp_file.write(yaml_content.encode('utf-8'))
            temp_file.flush()  # Убедимся, что данные записаны в файл
            data = parse_yaml(temp_file.name)
            self.assertEqual(data['Max_value'], 100)
            self.assertEqual(data['Min_value'], 0)
            self.assertEqual(data['Threshold'], 50)

    def test_parse_yaml_invalid(self):
        invalid_yaml_content = """
        Max_value: 100
        Min_value: 0
        Threshold: 50
        Expressions:
          Sum: 'Max_value + Threshold
        """
        with tempfile.NamedTemporaryFile(delete=True, suffix='.yaml') as temp_file:
            temp_file.write(invalid_yaml_content.encode('utf-8'))
            temp_file.flush()
            with self.assertRaises(ValueError):
                parse_yaml(temp_file.name)

class TestExpressionEvaluator(unittest.TestCase):

    def test_evaluate_expression(self):
        self.assertEqual(evaluate_expression('Max_value + Threshold'), 150)
        self.assertEqual(evaluate_expression('Max_value - Min_value'), 100)
        self.assertEqual(evaluate_expression('sqrt(16)'), 4.0)
        self.assertEqual(evaluate_expression('max(10, 20)'), 20)

    def test_evaluate_expression_invalid(self):
        with self.assertRaises(ValueError):
            evaluate_expression('invalid_expression')

class TestCustomSyntaxTransformer(unittest.TestCase):

    def test_transform_to_custom_syntax(self):
        yaml_data = {
            'Max_value': 100,
            'Min_value': 0,
            'Threshold': 50,
            'Settings': {
                'Resolution': '1920x1080',
                'Fullscreen': True,
                'Volume': 75,
            },
            'Players': [
                {
                    'Name': 'Иван',
                    'Age': 25,
                    'Sport': ['football', 'basketball', 'swimming'],
                }
            ]
        }
        
        results = {
            "Sum": 150,
            "Sub": 100,
            "Sqrt": 4.0,
            "Max": 20,
        }

        expected_output = (
            "Max_value is 100;\n"
            "Min_value is 0;\n"
            "Threshold is 50;\n"
            "struct {\n"
            " Resolution = '1920x1080',\n"
            " Fullscreen = True,\n"
            " Volume = 75,\n"
            "}\n"
            "struct {\n"
            " Name = 'Иван',\n"
            " Age = 25,\n"
            " Sport = ['football', 'basketball', 'swimming'],\n"
            "}\n"
        )

        output = transform_to_custom_syntax(yaml_data, results)
        
        # Убираем лишние пробелы и переносы строк для сравнения
        self.assertEqual(output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
