import logging
import re
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_logs(log_file):
    """
    Парсинг логов из файла.
    """
    logs = []
    with open(log_file, 'r') as file:
        for line in file:
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (.*)', line)
            if match:
                timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S,%f')
                level = match.group(2)
                module = match.group(3)
                message = match.group(4)
                logs.append({
                    'timestamp': timestamp,
                    'level': level,
                    'module': module,
                    'message': message
                })
    return logs

def analyze_logs(logs):
    """
    Анализ логов для выявления ошибок и проблем.
    """
    errors = [log for log in logs if log['level'] == 'ERROR']
    warnings = [log for log in logs if log['level'] == 'WARNING']

    if errors:
        logger.warning(f"Найдены ошибки в логах: {len(errors)}")
        for error in errors:
            logger.error(f"Ошибка: {error['message']} в {error['module']}")

    if warnings:
        logger.warning(f"Найдены предупреждения в логах: {len(warnings)}")
        for warning in warnings:
            logger.warning(f"Предупреждение: {warning['message']} в {warning['module']}")

    if not errors and not warnings:
        logger.info("Логи не содержат ошибок и предупреждений.")

if __name__ == "__main__":
    log_file = 'bot.log'
    logs = parse_logs(log_file)
    analyze_logs(logs)