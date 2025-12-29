"""
Паттерн Адаптер (Adapter)
Позволяет объектам с несовместимыми интерфейсами работать вместе.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Dict, List, Any
import xml.etree.ElementTree as ET



class LegacyUserSystem:
    """Старая система работы с пользователями (нельзя изменить)"""
    
    def get_user_data(self, user_id: int) -> str:
        """Возвращает данные пользователя в XML формате"""
       
        xml_data = f"""
        <user>
            <id>{user_id}</id>
            <name>Иван Иванов</name>
            <email>ivan@example.com</email>
            <registration_date>2020-05-15</registration_date>
            <status>active</status>
        </user>
        """
        return xml_data.strip()
    
    def get_all_users(self) -> str:
        """Возвращает всех пользователей в XML формате"""
        xml_data = """
        <users>
            <user>
                <id>1</id>
                <name>Иван Иванов</name>
                <email>ivan@example.com</email>
            </user>
            <user>
                <id>2</id>
                <name>Мария Петрова</name>
                <email>maria@example.com</email>
            </user>
            <user>
                <id>3</id>
                <name>Алексей Сидоров</name>
                <email>alex@example.com</email>
            </user>
        </users>
        """
        return xml_data.strip()
    
    def create_user_xml(self, xml_string: str) -> bool:
        """Создает пользователя из XML строки"""
        print(f"📄 Создаем пользователя из XML: {xml_string[:50]}...")
        return True
    
    def format_report(self, data: List[Dict]) -> str:
        """Формирует отчет в старом формате"""
        report = "=== ОТЧЕТ ПО ПОЛЬЗОВАТЕЛЯМ ===\n"
        for item in data:
            report += f"Пользователь: {item.get('name', 'Неизвестно')}\n"
            report += f"Email: {item.get('email', 'Неизвестно')}\n"
            report += "-" * 30 + "\n"
        return report



class ModernUserSystem(ABC):
    """Современная система работы с пользователями"""
    
    @abstractmethod
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Возвращает данные пользователя в формате словаря"""
        pass
    
    @abstractmethod
    def get_users(self) -> List[Dict[str, Any]]:
        """Возвращает всех пользователей в формате списка словарей"""
        pass
    
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Создает пользователя из словаря данных"""
        pass
    
    @abstractmethod
    def generate_json_report(self) -> str:
        """Генерирует отчет в JSON формате"""
        pass



class UserSystemAdapter(ModernUserSystem):
    """
    Адаптер, который преобразует интерфейс LegacyUserSystem
    в интерфейс ModernUserSystem
    """
    
    def __init__(self, legacy_system: LegacyUserSystem):
        self._legacy_system = legacy_system
    
    def _parse_xml_to_dict(self, xml_string: str) -> Dict[str, Any]:
        """Парсит XML строку в словарь"""
        try:
            root = ET.fromstring(xml_string)
            result = {}
            
            for element in root:
                if len(element) == 0:  
                    result[element.tag] = element.text
                else:  
                    result[element.tag] = self._parse_xml_to_dict(ET.tostring(element, encoding='unicode'))
            
            return result
        except ET.ParseError as e:
            print(f"❌ Ошибка парсинга XML: {e}")
            return {}
    
    def _parse_xml_users_list(self, xml_string: str) -> List[Dict[str, Any]]:
        """Парсит список пользователей из XML"""
        users = []
        try:
            root = ET.fromstring(xml_string)
            
            for user_element in root.findall('user'):
                user_data = {}
                for child in user_element:
                    user_data[child.tag] = child.text
                users.append(user_data)
            
            return users
        except ET.ParseError as e:
            print(f"❌ Ошибка парсинга XML: {e}")
            return []
    
    def _dict_to_xml(self, user_data: Dict[str, Any]) -> str:
        """Преобразует словарь в XML строку"""
        root = ET.Element("user")
        
        for key, value in user_data.items():
            element = ET.SubElement(root, key)
            element.text = str(value)
        
        return ET.tostring(root, encoding='unicode')
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Получить пользователя в формате словаря"""
        print(f"🔍 Запрашиваем пользователя с ID {user_id}...")
        
       
        xml_data = self._legacy_system.get_user_data(user_id)
        
      
        user_dict = self._parse_xml_to_dict(xml_data)
        
      
        user_dict['formatted_date'] = datetime.strptime(
            user_dict.get('registration_date', '2020-01-01'),
            '%Y-%m-%d'
        ).strftime('%d.%m.%Y')
        
        return user_dict
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Получить всех пользователей в формате списка словарей"""
        print("📋 Запрашиваем всех пользователей...")
        
       
        xml_data = self._legacy_system.get_all_users()
        
       
        users = self._parse_xml_users_list(xml_data)
        
        for user in users:
            if 'id' in user:
                user['id'] = int(user['id'])
        
        return users
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Создать пользователя из словаря данных"""
        print(f"👤 Создаем пользователя: {user_data.get('name')}")
        
    
        xml_string = self._dict_to_xml(user_data)
        
   
        return self._legacy_system.create_user_xml(xml_string)
    
    def generate_json_report(self) -> str:
        """Сгенерировать отчет в JSON формате"""
        print("📊 Генерируем JSON отчет...")
        
      
        xml_data = self._legacy_system.get_all_users()
        users = self._parse_xml_users_list(xml_data)
        
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_users": len(users),
            "users": users
        }
        
        return json.dumps(report, ensure_ascii=False, indent=2)



class OldPaymentProcessor:
    """Старая система обработки платежей (в долларах)"""
    
    def process_payment(self, amount_usd: float, description: str) -> str:
        """Обработка платежа в долларах"""
        return f"Оплачено ${amount_usd:.2f} за '{description}'"
    
    def get_balance_usd(self) -> float:
        """Получить баланс в долларах"""
        return 1000.0



class ModernPaymentSystem(ABC):
    """Современная система обработки платежей"""
    
    @abstractmethod
    def pay(self, amount_rub: float, description: str) -> str:
        pass
    
    @abstractmethod
    def get_balance_rub(self) -> float:
        pass



class PaymentAdapter(ModernPaymentSystem):
    """Адаптер для конвертации рублей в доллары"""
    
    def __init__(self, old_processor: OldPaymentProcessor, exchange_rate: float = 75.0):
        self._old_processor = old_processor
        self._exchange_rate = exchange_rate
    
    def _convert_rub_to_usd(self, rub: float) -> float:
        """Конвертировать рубли в доллары"""
        return rub / self._exchange_rate
    
    def _convert_usd_to_rub(self, usd: float) -> float:
        """Конвертировать доллары в рубли"""
        return usd * self._exchange_rate
    
    def pay(self, amount_rub: float, description: str) -> str:
        """Оплата в рублях"""
        amount_usd = self._convert_rub_to_usd(amount_rub)
        print(f"💱 Конвертация: {amount_rub:.2f} RUB → {amount_usd:.2f} USD")
        
        result = self._old_processor.process_payment(amount_usd, description)
      
        return result.replace("$", "RUB ")
    
    def get_balance_rub(self) -> float:
        """Получить баланс в рублях"""
        balance_usd = self._old_processor.get_balance_usd()
        return self._convert_usd_to_rub(balance_usd)



class AnalyticsSystem:
    """Система аналитики, которая работает только с JSON"""
    
    def analyze_json(self, json_data: str) -> Dict:
        """Анализирует данные в JSON формате"""
        print("📈 Анализируем JSON данные...")
        data = json.loads(json_data)
        
        analysis = {
            "record_count": len(data.get("users", [])),
            "first_user": data.get("users", [{}])[0].get("name", "Неизвестно") if data.get("users") else "Нет данных",
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return analysis


class XMLToJSONAdapter:
    """Адаптер для преобразования XML в JSON"""
    
    def __init__(self, xml_system: LegacyUserSystem):
        self._xml_system = xml_system
    
    def get_users_json(self) -> str:
        """Получить пользователей в JSON формате"""
        
        xml_data = self._xml_system.get_all_users()
        
    
        root = ET.fromstring(xml_data)
        users = []
        
        for user_element in root.findall('user'):
            user_data = {}
            for child in user_element:
                user_data[child.tag] = child.text
            users.append(user_data)
        
     
        json_data = {
            "users": users,
            "source": "legacy_xml_system",
            "converted_at": datetime.now().isoformat()
        }
        
        return json.dumps(json_data, ensure_ascii=False)


if __name__ == "__main__":
    print("=== Паттерн Адаптер (Adapter) ===\n")
    
   
    print("1. Адаптер пользовательской системы:")
    print("=" * 60)
    
   
    legacy_system = LegacyUserSystem()
    
   
    adapter = UserSystemAdapter(legacy_system)
    
    
    print("\nПолучение пользователя (современный интерфейс):")
    user = adapter.get_user(1)
    print(f"Данные пользователя (словарь):")
    for key, value in user.items():
        print(f"  {key}: {value}")
    
    print("\nПолучение всех пользователей:")
    users = adapter.get_users()
    for u in users:
        print(f"  • {u['name']} ({u['email']})")
    
    print("\nСоздание нового пользователя:")
    new_user = {
        "name": "Екатерина Волкова",
        "email": "ekaterina@example.com",
        "age": "28",
        "city": "Москва"
    }
    success = adapter.create_user(new_user)
    print(f"Результат: {'Успешно' if success else 'Ошибка'}")
    
    print("\nГенерация JSON отчета:")
    json_report = adapter.generate_json_report()
    print(f"Отчет (первые 200 символов):\n{json_report[:200]}...")
    
    
    print("\n\n2. Адаптер платежной системы с конвертацией валют:")
    print("=" * 60)
    
    old_payment = OldPaymentProcessor()
    payment_adapter = PaymentAdapter(old_payment, exchange_rate=80.0)
    
    print(f"Баланс в рублях: {payment_adapter.get_balance_rub():.2f} RUB")
    
    print("\nОплата в рублях через адаптер:")
    result = payment_adapter.pay(5000.0, "Покупка ноутбука")
    print(f"Результат: {result}")
    
    print("\nПрямой вызов старой системы (в долларах):")
    old_result = old_payment.process_payment(100.0, "Абонемент")
    print(f"Результат: {old_result}")
    
    
    print("\n\n3. Адаптер для системы аналитики (XML → JSON):")
    print("=" * 60)
    
    analytics = AnalyticsSystem()
    xml_to_json_adapter = XMLToJSONAdapter(legacy_system)
    

    json_data = xml_to_json_adapter.get_users_json()
    print(f"Сконвертированные данные (первые 150 символов):\n{json_data[:150]}...")
    
    
    analysis = analytics.analyze_json(json_data)
    print("\nРезультаты анализа:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
   
    print("\n\n4. Сравнение: старая система напрямую vs через адаптер")
    print("=" * 60)
    
    print("\nСтарая система напрямую (XML):")
    xml_direct = legacy_system.get_user_data(1)
    print(f"Данные: {xml_direct[:80]}...")
    
    print("\nЧерез адаптер (словарь):")
    dict_via_adapter = adapter.get_user(1)
    print(f"Имя: {dict_via_adapter.get('name')}")
    print(f"Email: {dict_via_adapter.get('email')}")
    print(f"Дата регистрации: {dict_via_adapter.get('formatted_date')}")
    
   
    print("\n\n5. Гибкость адаптера:")
    print("=" * 60)
    
    print("\nМожно создать разные адаптеры для одной старой системы:")
    
    class UserAdapterForReporting(UserSystemAdapter):
        """Специальный адаптер для отчетности"""
        def generate_detailed_report(self) -> str:
            users = self.get_users()
            
            report_lines = ["ДЕТАЛЬНЫЙ ОТЧЕТ ПО ПОЛЬЗОВАТЕЛЯМ", "=" * 40]
            for i, user in enumerate(users, 1):
                report_lines.append(f"{i}. {user['name']} - {user['email']}")
            
            report_lines.append(f"\nВсего пользователей: {len(users)}")
            report_lines.append(f"Отчет сгенерирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            
            return "\n".join(report_lines)
    
    reporting_adapter = UserAdapterForReporting(legacy_system)
    detailed_report = reporting_adapter.generate_detailed_report()
    print("\n" + detailed_report)
    
    print("\n✅ Адаптер работает корректно!")
    print("\n📌 Итог: Адаптер позволяет использовать старую систему")
    print("через современный интерфейс без изменения её исходного кода.")