import argparse
import yaml
import sys
import re
import math

def parse_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла YAML: {e}")

def transform_to_custom_syntax(data, results):
    result = []
    
    def process_dict(d):
        result.append("struct {")
        for k, v in d.items():
            if k in results:
                # Заменяем выражение на вычисленное значение
                result.append(f" {k} = {results[k]},")
            else:
                result.append(f" {k} = {format_value(v)},")
        result.append("}")

    for key, value in data.items():
        if not is_valid_name(key):
            raise ValueError(f"Недопустимое имя: {key}")
        
        if isinstance(value, dict):
            process_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    process_dict(item)
                else:
                    result.append(f"{key} is {format_value(item)};")
        else:
            result.append(f"{key} is {format_value(value)};")
    
    return "\n".join(result)

def format_value(value):
    if isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, dict):
        return f"[{', '.join(format_value(v) for v in value)}]"
    elif isinstance(value, list):
        return f"[{', '.join(format_value(v) for v in value)}]"
    else:
        raise ValueError("Unsupported value type")

def is_valid_name(name):
    # Проверка на соответствие имени заданному синтаксису
    return bool(re.match(r'^[_A-Z][_a-zA-Z0-9]*$', name))

def evaluate_expression(expression):
    """Evaluates a constant expression."""
    try:
        # Заменяем имена на их значения
        expression = expression.replace('Max_value', '100').replace('Min_value', '0').replace('Threshold', '50')
        
        # Определяем функции
        expression = expression.replace('sqrt', 'math.sqrt')
        
        # Используем eval для вычисления выражения
        return eval(expression)
    except Exception as e:
        raise ValueError(f"Ошибка при вычислении выражения: {e}")

def main():
    parser = argparse.ArgumentParser(description='Transform YAML to custom config language.')
    parser.add_argument('input_file', type=str, help='Path to the input YAML file')
    
    args = parser.parse_args()
    
    try:
        yaml_data = parse_yaml(args.input_file)

        # Вычисляем выражения и сохраняем результаты
        results = {
            "Sum": evaluate_expression(yaml_data['Expressions']['Sum']),
            "Sub": evaluate_expression(yaml_data['Expressions']['Sub']),
            "Sqrt": evaluate_expression(yaml_data['Expressions']['Sqrt']),
            "Max": evaluate_expression(yaml_data['Expressions']['Max']),
        }

        output = []

        # Добавляем словари и списки в вывод с заменой выражений на вычисленные значения
        output.append(transform_to_custom_syntax(yaml_data, results))

        print("\n".join(output))
        
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
