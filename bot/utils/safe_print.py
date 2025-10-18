"""Безопасный вывод в консоль для Windows"""
import sys

def safe_print(*args, **kwargs):
    """Безопасный print для Windows консоли"""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Заменяем проблемные символы
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Сначала пробуем cp1251, потом ascii
                try:
                    safe_arg = arg.encode('cp1251', errors='replace').decode('cp1251')
                except:
                    safe_arg = arg.encode('ascii', errors='replace').decode('ascii')
                safe_args.append(safe_arg)
            else:
                safe_args.append(arg)
        print(*safe_args, **kwargs)

def setup_console_utf8():
    """Попытка настроить UTF-8 для Windows консоли"""
    try:
        # Для Windows 10+ можно попробовать установить UTF-8
        if sys.platform == "win32":
            import os
            os.system("chcp 65001 >nul 2>&1")  # UTF-8 codepage
    except:
        pass