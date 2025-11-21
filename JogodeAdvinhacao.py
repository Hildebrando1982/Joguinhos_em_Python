import random

def jogo_de_adivinhacao():
    """
    Função principal que contém a lógica do jogo de adivinhação.
    """
    # Loop principal para permitir novo jogo com novo jogador
    while True:
        # 1. Obter o nome do jogador
        print("|------------------------------------------|")
        print("|           Jogo de Advinhação             |")
        print("|      Desenvolvido por Hildebrando        |")
        print("|------------------------------------------|\n")
        nome = input("Olá! Por favor, digite seu nome: ")
        print(f"\nBem-vindo(a) ao Jogo de Adivinhação, {nome}!")
        print("O objetivo é adivinhar o número secreto entre 1 e 100.")
        
        # Loop para rodadas do mesmo jogador
        continuar_jogando = True
        while continuar_jogando:
            # 2. Configurar o jogo
            
            # Gerar um número aleatório secreto
            numero_secreto = random.randint(1, 100)
            
            # Inicializar os limites do intervalo de dicas
            limite_inferior = 1
            limite_superior = 100
            
            # Variável para controlar o número de tentativas
            tentativas = 0
            
            # Início do loop principal do jogo
            while True:
                try:
                    # 3. Solicitar o palpite do jogador                  
                    palpite = int(input(f"\nDigite seu palpite (entre {limite_inferior} e {limite_superior}): "))
                    tentativas += 1
                    
                    # 4. Verificar se o palpite está dentro do intervalo válido
                    if palpite < 1 or palpite > 100:
                        print("Seu palpite deve estar entre 1 e 100. Tente novamente.")
                        tentativas -= 1  # Não conta essa tentativa
                        continue # Volta para o início do loop sem contar como tentativa válida
                    
                    # 5. Lógica do jogo (Acertou ou Errou)
                    if palpite == numero_secreto:
                        # O jogador acertou!
                        print(f"\n🏆 **PARABÉNS, {nome}! VOCÊ VENCEU!!!** 🏆")
                        print(f"O número secreto era {numero_secreto}.")
                        print(f"Você acertou em {tentativas} tentativas.")
                        break # Sai do loop e termina o jogo
                    
                    elif palpite < numero_secreto:
                        # O palpite é muito baixo
                        print("⬇️  Chute Baixo!")
                        # Atualizar o limite inferior para refinar a dica
                        limite_inferior = max(palpite + 1, limite_inferior)
                        
                    else: # palpite > numero_secreto
                        # O palpite é muito alto
                        print("⬆️  Chute Alto!")
                        # Atualizar o limite superior para refinar a dica
                        limite_superior = min(palpite - 1, limite_superior)

                    # 6. Mostrar a dica do novo intervalo (se o jogo não acabou)
                    print(f"💡 Dica: O número escolhido está entre {limite_inferior} e {limite_superior}.")
                    
                    # Se o limite inferior se tornar maior que o superior (o que não deve acontecer
                    # com a lógica acima, mas é um bom "fail-safe"), significa um erro lógico.
                    if limite_inferior > limite_superior:
                         print("🚫 Erro lógico no jogo. O intervalo de busca está inválido.")
                         break
                         
                except ValueError:
                    # Capturar erro se o usuário digitar algo que não é um número inteiro
                    print("🚫 Entrada inválida. Por favor, digite apenas um **número inteiro**.")
                    tentativas -= 1  # Não conta essa tentativa
            
            # 7. Perguntar se o jogador quer jogar novamente
            print("\n" + "="*50)
            print("Escolha uma opção:")
            print("1 - Jogar novamente (mesmo jogador)")
            print("2 - Novo jogo (trocar de jogador)")
            print("3 - Sair")
            opcao = input("\n👉 Digite sua escolha (1/2/3): ").strip()
            
            if opcao == '1':
                print("\n" + "="*50)
                print(f"🔄 Iniciando nova rodada para {nome}...\n")
                print("="*50)
                continue  # Continua no loop interno (mesma pessoa)
            elif opcao == '2':
                print("\n" + "="*50)
                print("🔄 Iniciando novo jogo...\n")
                print("="*50)
                continuar_jogando = False  # Sai do loop interno
                break  # Volta para pedir novo nome
            else:
                print(f"\n👋 Obrigado por jogar, {nome}! Até a próxima!")
                return  # Encerra a função completamente
            
# Executar o jogo
if __name__ == "__main__":
    jogo_de_adivinhacao()
