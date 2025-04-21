#Alunos: Giovanne Dilly #24114290100, Bruno Vieira #24114290064, Vinicius Massaranduba #24114290023

import tkinter as tk
from tkinter import messagebox

# === FUNÇÕES DE CÁLCULO ===

def calcular_taxa_diaria(taxa_anual):
    return (1 + taxa_anual) ** (1 / 365) - 1

def gerar_tabela_iof():
    tabela = {}
    for dia in range(1, 31):
        tabela[dia] = 0.96 * (30 - dia) / 30  # de 0.96 no 1º até 0 no 30º
    return tabela

def obter_aliquota_ir(dias):
    if dias <= 180:
        return 0.225
    elif dias <= 360:
        return 0.20
    elif dias <= 720:
        return 0.175
    else:
        return 0.15

def calcular_rendimento(valor, dias):
    taxa_anual = 0.1415
    taxa_diaria = calcular_taxa_diaria(taxa_anual)
    montante = valor * (1 + taxa_diaria) ** dias
    rendimento_bruto = montante - valor
    return rendimento_bruto, montante

def aplicar_iof(rendimento_bruto, dias, tabela_iof):
    if dias <= 30:
        aliquota_iof = tabela_iof.get(dias, 1.0)
        return rendimento_bruto * aliquota_iof
    return 0.0

def aplicar_ir(rendimento_bruto_menos_iof, dias):
    aliquota = obter_aliquota_ir(dias)
    return rendimento_bruto_menos_iof * aliquota

# === INTERFACE GRÁFICA ===

def receber_dados():
    try:
        valor = float(entrada_valor.get())
        dias = int(entrada_dias.get())

        if valor <= 0 or dias <= 0:
            messagebox.showerror("Erro", "O valor e o prazo devem ser positivos.")
            return

        tabela_iof = gerar_tabela_iof()

        rendimento_bruto, montante = calcular_rendimento(valor, dias)
        imposto_iof = aplicar_iof(rendimento_bruto, dias, tabela_iof)
        base_ir = rendimento_bruto - imposto_iof
        imposto_ir = aplicar_ir(base_ir, dias)
        rendimento_liquido = rendimento_bruto - imposto_iof - imposto_ir
        valor_final = valor + rendimento_liquido

        if dias <= 30:
            aviso_iof = "⚠️ IOF aplicado (resgate em menos de 30 dias)."
        else:
            aviso_iof = "✅ Sem IOF (resgate após 30 dias)."

        mensagem = (
            f"{aviso_iof}\n\n"
            f"Valor investido: R$ {valor:.2f}\n"
            f"Rendimento bruto: R$ {rendimento_bruto:.2f}\n"
            f"Desconto IOF: R$ {imposto_iof:.2f}\n"
            f"Desconto IR: R$ {imposto_ir:.2f}\n"
            f"Rendimento líquido: R$ {rendimento_liquido:.2f}\n"
            f"Valor final: R$ {valor_final:.2f}"
        )

        messagebox.showinfo("Resultado", mensagem)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor e dias válidos!")

# Criação da janela
janela = tk.Tk()
janela.title("Simulador Super Cofrinho")
janela.geometry("320x250")

tk.Label(janela, text="Valor do Investimento (R$):").pack(pady=5)
entrada_valor = tk.Entry(janela)
entrada_valor.pack()

tk.Label(janela, text="Tempo do investimento (dias):").pack(pady=5)
entrada_dias = tk.Entry(janela)
entrada_dias.pack()

tk.Button(janela, text="Calcular", command=receber_dados).pack(pady=10)

janela.mainloop()
