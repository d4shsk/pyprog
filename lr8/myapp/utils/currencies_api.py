import xml.etree.ElementTree as ET
from myapp.models.currency import Currency
import urllib.request

def get_currencies():
    # Пример XML данных
    xml_data = """
    <ValCurs Date="29.12.2024" name="Foreign Currency Market">
        <Valute ID="R01235">
            <NumCode>840</NumCode>
            <CharCode>USD</CharCode>
            <Nominal>1</Nominal>
            <Name>Доллар США</Name>
            <Value>91,50</Value>
        </Valute>
        <Valute ID="R01239">
            <NumCode>978</NumCode>
            <CharCode>EUR</CharCode>
            <Nominal>1</Nominal>
            <Name>Евро</Name>
            <Value>101,20</Value>
        </Valute>
         <Valute ID="R01280">
            <NumCode>360</NumCode>
            <CharCode>IDR</CharCode>
            <Nominal>10000</Nominal>
            <Name>Индонезийских рупий</Name>
            <Value>59,61</Value>
        </Valute>
    </ValCurs>
    """
    
    # Парсинг
    root = ET.fromstring(xml_data)
    currencies = []
    
    for valute in root.findall('Valute'):
        uid = valute.get('ID')
        num_code = valute.find('NumCode').text
        char_code = valute.find('CharCode').text
        name = valute.find('Name').text
        value = valute.find('Value').text
        nominal = int(valute.find('Nominal').text)
        
        # Создаем объект модели
        curr = Currency(uid, num_code, char_code, name, value, nominal)
        currencies.append(curr)
        
    return currencies