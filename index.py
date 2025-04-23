#Alunos: Giovanne Dilly #24114290100, Bruno Vieira #24114290064, Vinicius Massaranduba #24114290023

import tkinter as tk  # Importa uma biblioteca usada para interfaces simples com um apelido "tk"
from tkinter import messagebox  # Chama uma caixa de mensagem

# === FUNÇÕES DE CÁLCULO ===

# Função para converter taxa anual em taxa diária (base 365 dias)
def calcular_taxa_diaria(taxa_anual):
    return (1 + taxa_anual) ** (1 / 365) - 1

#Cria uma função que serve para gerar uma tabela 
def gerar_tabela_iof():
    tabela = {} #Cria um dicionário vazio chamado tabela.
    for dia in range(1, 31):
        tabela[dia] = 0.96 * (30 - dia) / 30  # de 0.96 no 1º até 0 no 30º
    return tabela

# Função para obter a alíquota do Imposto de Renda com base no número de dias investidos
def obter_aliquota_ir(dias):
    # Se o investimento for de até 180 dias, a alíquota é de 22,5%
    if dias <= 180:
        return 0.225
    # Se for de até 360 dias, a alíquota é de 20%
    elif dias <= 360:
        return 0.20
    # Se for de até 720 dias, a alíquota é de 17,5%
    elif dias <= 720:
        return 0.175
    # Acima de 720 dias, a alíquota é de 15%
    else:
        return 0.15
    
# Função para calcular o rendimento bruto e o montante final do investimento
def calcular_rendimento(valor, dias):
    # Define a taxa de juros anual (14,15%)
    taxa_anual = 0.1415

    # Chama a função que converte a taxa anual em taxa diária
    taxa_diaria = calcular_taxa_diaria(taxa_anual)

    # Calcula o montante final usando juros compostos: M = P * (1 + i)^n
    montante = valor * (1 + taxa_diaria) ** dias

    # Calcula o rendimento bruto (quanto o dinheiro rendeu sem descontar impostos)
    rendimento_bruto = montante - valor

    # Retorna o rendimento bruto e o montante final
    return rendimento_bruto, montante

# Função para calcular o valor de IOF a ser cobrado sobre o rendimento bruto
def aplicar_iof(rendimento_bruto, dias, tabela_iof):
    # Se o investimento for de até 30 dias, aplica o IOF
    if dias <= 30:
        # Busca a alíquota de IOF na tabela com base na quantidade de dias
        aliquota_iof = tabela_iof.get(dias, 1.0)  # Se não encontrar, usa 1.0 (100%)

        # Calcula o valor do IOF a pagar
        return rendimento_bruto * aliquota_iof

    # Se passou de 30 dias, não há IOF
    return 0.0

# Função para calcular o Imposto de Renda sobre o rendimento líquido (após IOF)
def aplicar_ir(rendimento_bruto_menos_iof, dias):
    # Obtém a alíquota de IR correspondente ao prazo do investimento
    aliquota = obter_aliquota_ir(dias)

    # Calcula o valor do imposto de renda aplicando a alíquota sobre o rendimento líquido
    return rendimento_bruto_menos_iof * aliquota

# === INTERFACE GRÁFICA ===

 # Função que será chamada ao clicar em um botão
def receber_dados(): 

    try:
            # Pega os dados inseridos pelo usuário
        valor = float(entrada_valor.get())
        dias = int(entrada_dias.get())

        if valor <= 0 or dias <= 0:
            messagebox.showerror("Erro", "O valor e o prazo devem ser positivos.")
            return

        tabela_iof = gerar_tabela_iof()

        #Gera a tabela regressiva do IOF (de 96% no 1º dia até 0% no 30º)
        tabela_iof = gerar_tabela_iof()

        #Calcula o rendimento bruto e o montante total (antes dos impostos)
        rendimento_bruto, montante = calcular_rendimento(valor, dias)

        #Calcula o valor do IOF com base na tabela e nos dias
        imposto_iof = aplicar_iof(rendimento_bruto, dias, tabela_iof)

        #Calcula a base de cálculo do IR (rendimento - IOF)
        base_ir = rendimento_bruto - imposto_iof

        #Aplica o IR com base no prazo da aplicação
        imposto_ir = aplicar_ir(base_ir, dias)

        #Calcula o rendimento líquido (o que sobra depois dos impostos)
        rendimento_liquido = rendimento_bruto - imposto_iof - imposto_ir

        #Soma o rendimento líquido ao valor inicial para obter o valor final
        valor_final = valor + rendimento_liquido

        #Adiciona uma observação se o resgate for antes de 30 dias
        if dias <= 30:
            aviso_iof = " IOF aplicado (resgate em menos de 30 dias)."
        else:
            aviso_iof = " Sem IOF (resgate após 30 dias)."
 
        #Monta a mensagem com os resultados do cálculo
        mensagem = (
            f"{aviso_iof}\n\n"
            f"Valor investido: R$ {valor:.2f}\n"
            f"Rendimento bruto: R$ {rendimento_bruto:.2f}\n"
            f"Desconto IOF: R$ {imposto_iof:.2f}\n"
            f"Desconto IR: R$ {imposto_ir:.2f}\n"
            f"Rendimento líquido: R$ {rendimento_liquido:.2f}\n"
            f"Valor final: R$ {valor_final:.2f}"
        )
    #  Exibe a mensagem final com todos os valores em uma janela popup
        messagebox.showinfo("Resultado", mensagem)

    except ValueError: # Mostra um erro caso os dados não sejam inseridos
        messagebox.showerror("Erro", "Por favor, digite um valor e dias válidos!")

# Criação da janela
janela = tk.Tk()
janela.title("Simulador Super Cofrinho") # Titulo da janela
janela.geometry("320x250") # Largura e altura

# Rótulo e campo de entrada para o valor
tk.Label(janela, text="Valor do Investimento (R$):").pack(pady=5)# Rótulo
entrada_valor = tk.Entry(janela)# Campo de entrada
entrada_valor.pack()# Adiciona o campo de entrada a janela

# Rótulo e campo de entrada para os dias
tk.Label(janela, text="Tempo do investimento (dias):").pack(pady=5)
entrada_dias = tk.Entry(janela)
entrada_dias.pack()

# Botão para enviar os dados e utilizar a função receber_dados()
tk.Button(janela, text="Calcular", command=receber_dados).pack(pady=10)

# Inicia o loop da nossa interface
janela.mainloop()