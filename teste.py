def calcular_multa(dias_atraso):

    if dias_atraso <= 0:
        return 0.0
    
    return dias_atraso * 2.0

print("Iniciando os testes da multa...")

resultado1 = calcular_multa(5)
assert resultado1 == 10.0, f"Erro no teste 1! Esperava 10.0, mas veio {resultado1}"

resultado2 = calcular_multa(0)
assert resultado2 == 0.0, f"Erro no teste 2! Esperava 0.0, mas veio {resultado2}"

print("Parabéns! Todos os testes passaram com sucesso!")