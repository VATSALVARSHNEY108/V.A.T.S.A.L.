"""
Advanced Calculator Module
Provides complex calculations, unit conversions, and currency conversion
"""

import math
import re
import requests
from datetime import datetime

class AdvancedCalculator:
    def __init__(self):
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'phi': 1.618033988749895,  # Golden ratio
            'c': 299792458  # Speed of light (m/s)
        }
        
        self.unit_conversions = {
            'length': {
                'meter': 1,
                'm': 1,
                'kilometer': 0.001,
                'km': 0.001,
                'centimeter': 100,
                'cm': 100,
                'millimeter': 1000,
                'mm': 1000,
                'mile': 0.000621371,
                'yard': 1.09361,
                'foot': 3.28084,
                'ft': 3.28084,
                'inch': 39.3701,
                'in': 39.3701
            },
            'weight': {
                'kilogram': 1,
                'kg': 1,
                'gram': 1000,
                'g': 1000,
                'milligram': 1000000,
                'mg': 1000000,
                'pound': 2.20462,
                'lb': 2.20462,
                'ounce': 35.274,
                'oz': 35.274,
                'ton': 0.001,
                'tonne': 0.001
            },
            'temperature': {
                'celsius': 'base',
                'c': 'base',
                'fahrenheit': 'f',
                'f': 'f',
                'kelvin': 'k',
                'k': 'k'
            },
            'volume': {
                'liter': 1,
                'l': 1,
                'milliliter': 1000,
                'ml': 1000,
                'gallon': 0.264172,
                'gal': 0.264172,
                'quart': 1.05669,
                'pint': 2.11338,
                'cup': 4.22675,
                'ounce': 33.814,
                'fl oz': 33.814
            }
        }
    
    def calculate(self, expression):
        """Evaluate mathematical expression safely using controlled parsing"""
        try:
            expression = expression.lower()
            
            for name, value in self.constants.items():
                expression = expression.replace(name, str(value))
            
            expression = expression.replace('^', '**')
            
            allowed_chars = set('0123456789+-*/().** esincotaglrqxpbfhdmw')
            if not all(c in allowed_chars for c in expression.replace(' ', '')):
                return "Invalid characters in expression. Only numbers and math operators allowed."
            
            dangerous_patterns = ['__', 'import', 'exec', 'eval', 'compile', 'open', 'file']
            if any(pattern in expression for pattern in dangerous_patterns):
                return "Expression contains forbidden patterns."
            
            safe_functions = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                'exp': math.exp, 'pow': math.pow, 'abs': abs,
                'ceil': math.ceil, 'floor': math.floor, 'round': round,
                'pi': math.pi, 'e': math.e
            }
            
            safe_globals = {"__builtins__": {}}
            
            result = eval(expression, safe_globals, safe_functions)
            
            if not isinstance(result, (int, float, complex)):
                return "Calculation result must be a number."
            
            return self._format_calculation(expression, result)
            
        except Exception as e:
            return f"Calculation error: {str(e)}\nPlease use valid mathematical expressions."
    
    def convert_units(self, value, from_unit, to_unit):
        """Convert between different units"""
        try:
            value = float(value)
            from_unit = from_unit.lower()
            to_unit = to_unit.lower()
            
            for category, units in self.unit_conversions.items():
                if from_unit in units and to_unit in units:
                    if category == 'temperature':
                        result = self._convert_temperature(value, from_unit, to_unit)
                    else:
                        base_value = value / units[from_unit]
                        result = base_value * units[to_unit]
                    
                    return self._format_conversion(value, from_unit, result, to_unit)
            
            return f"Cannot convert from {from_unit} to {to_unit}. Check unit names."
            
        except Exception as e:
            return f"Conversion error: {str(e)}"
    
    def _convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
        to_celsius = {
            'celsius': lambda x: x,
            'c': lambda x: x,
            'fahrenheit': lambda x: (x - 32) * 5/9,
            'f': lambda x: (x - 32) * 5/9,
            'kelvin': lambda x: x - 273.15,
            'k': lambda x: x - 273.15
        }
        
        from_celsius = {
            'celsius': lambda x: x,
            'c': lambda x: x,
            'fahrenheit': lambda x: (x * 9/5) + 32,
            'f': lambda x: (x * 9/5) + 32,
            'kelvin': lambda x: x + 273.15,
            'k': lambda x: x + 273.15
        }
        
        celsius = to_celsius[from_unit](value)
        result = from_celsius[to_unit](celsius)
        
        return result
    
    def get_currency_rate(self, from_currency='USD', to_currency='EUR'):
        """Get current currency exchange rate"""
        try:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rate = data['rates'].get(to_currency)
                
                if rate:
                    return self._format_currency_rate(from_currency, to_currency, rate)
                else:
                    return f"Currency {to_currency} not found."
            else:
                return "Currency service temporarily unavailable."
                
        except Exception as e:
            return f"Currency error: {str(e)}"
    
    def convert_currency(self, amount, from_currency='USD', to_currency='EUR'):
        """Convert amount from one currency to another"""
        try:
            amount = float(amount)
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rate = data['rates'].get(to_currency)
                
                if rate:
                    converted = amount * rate
                    return self._format_currency_conversion(amount, from_currency, converted, to_currency, rate)
                else:
                    return f"Currency {to_currency} not found."
            else:
                return "Currency service temporarily unavailable."
                
        except Exception as e:
            return f"Currency conversion error: {str(e)}"
    
    def percentage_calculator(self, number, percentage):
        """Calculate percentage of a number"""
        try:
            num = float(number)
            pct = float(percentage)
            result = (num * pct) / 100
            
            output = f"\n{'='*50}\n"
            output += f"📊 PERCENTAGE CALCULATION\n"
            output += f"{'='*50}\n\n"
            output += f"{pct}% of {num} = {result}\n"
            output += f"{'='*50}\n"
            
            return output
            
        except Exception as e:
            return f"Percentage error: {str(e)}"
    
    def _format_calculation(self, expression, result):
        """Format calculation result"""
        output = f"\n{'='*50}\n"
        output += f"🧮 CALCULATION\n"
        output += f"{'='*50}\n\n"
        output += f"Expression: {expression}\n"
        output += f"Result: {result}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _format_conversion(self, value, from_unit, result, to_unit):
        """Format unit conversion result"""
        output = f"\n{'='*50}\n"
        output += f"🔄 UNIT CONVERSION\n"
        output += f"{'='*50}\n\n"
        output += f"{value} {from_unit} = {result:.4f} {to_unit}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _format_currency_rate(self, from_curr, to_curr, rate):
        """Format currency rate"""
        output = f"\n{'='*50}\n"
        output += f"💱 EXCHANGE RATE\n"
        output += f"{'='*50}\n\n"
        output += f"1 {from_curr} = {rate:.4f} {to_curr}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _format_currency_conversion(self, amount, from_curr, converted, to_curr, rate):
        """Format currency conversion"""
        output = f"\n{'='*50}\n"
        output += f"💱 CURRENCY CONVERSION\n"
        output += f"{'='*50}\n\n"
        output += f"{amount:.2f} {from_curr} = {converted:.2f} {to_curr}\n"
        output += f"Exchange Rate: 1 {from_curr} = {rate:.4f} {to_curr}\n"
        output += f"{'='*50}\n"
        
        return output

if __name__ == "__main__":
    calc = AdvancedCalculator()
    
    print("Testing Calculator...")
    print(calc.calculate("2 + 2 * 3"))
    print(calc.calculate("sqrt(16) + pi"))
    
    print("\nTesting Unit Conversion...")
    print(calc.convert_units(100, "km", "mile"))
    print(calc.convert_units(25, "celsius", "fahrenheit"))
    
    print("\nTesting Currency...")
    print(calc.get_currency_rate("USD", "EUR"))
    print(calc.convert_currency(100, "USD", "EUR"))
