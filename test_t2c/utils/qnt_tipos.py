
import json
from collections import Counter


def contagem_tipos():
    try:
        tipo_qnt = []
        
        with open('dados_excel.json', 'r') as file:
            dados_total = json.load(file)

        quantidades_por_tipo = Counter(item['Type'] for item in dados_total)

        for tipo, quantidade in sorted(quantidades_por_tipo.items()):
            print(f"Type: {tipo}={quantidade}")
            
            tipo_qnt.append({tipo: quantidade})
            
        return True, tipo_qnt
            
    except Exception as e:
        print(f'Erro metodo contagem_tipos: {e}')