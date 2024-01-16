import tkinter as tk
from tkinter import messagebox, IntVar


def toggle_seguro_entry():
    if chk_value.get() == 1:  # Se o checkbox estiver marcado
        seguro_entry.config(state='normal')  # Habilita o campo de texto
    else:
        seguro_entry.config(state='disabled')  # Desabilita o campo de texto


def calcular():
    try:
        # Obter valores dos campos de entrada
        total = float(total_entry.get())
        tg = float(tg_entry.get())
        noites = int(noites_entry.get())
        pax = int(pax_entry.get())
        seguro = float(seguro_entry.get())
        seguro_incluso = chk_value.get()
        porcentagemNAD = float(porcentagemNAD_entry.get())
        porcentagemOperador = float(porcentagemOP_entry.get())

        # Calcular a taxa de porto com base no número de noites e pax
        tp_por_noite = 30 if noites > 5 else 25
        # tp = 840  #
        tp = tp_por_noite * noites * pax

        # Deduzir as taxas do valor total
        TsT = total - tg - tp - (seguro if seguro_incluso else 0)

        # Calcular a porcentagem da NAD
        rawcomissao18NAD = TsT * (porcentagemNAD / 100)

        # Calcular a porcentagem do Operador
        rawcomissaoOperador = TsT * (porcentagemOperador / 100)

        # Adicionar a porcentagens do seguro aos custos porcentagem, se o seguro estiver incluso
        RealComissao18NAD = (rawcomissao18NAD + (seguro * 0.1)) \
            if seguro_incluso else rawcomissao18NAD

        RealComissaoOperador = (rawcomissaoOperador + (seguro * 0.05)) \
            if seguro_incluso else rawcomissaoOperador

        custo_NET = total - RealComissao18NAD
        valor_VENDA = total - RealComissaoOperador

        # Mostrar os resultados
        compra = f"Valor de Compra: {custo_NET:.2f}"
        venda = f"Valor de Venda: {valor_VENDA:.2f}"
        messagebox.showinfo("Resultado", compra)
        messagebox.showinfo("Resultado", venda)

        print(f'Total: {total}')
        print(f'TST: {TsT:.2f}')
        print(compra)
        print(venda)
        print(f'TP: {tp} USD')
        print(f'TG: {tg} USD')
        print(f'Custo p/Noite: {tp_por_noite} USD')
        print(f'Num Pax: {pax}')

        if RealComissao18NAD == rawcomissao18NAD and RealComissaoOperador == rawcomissaoOperador:
            print(f'{int(porcentagemNAD)}% NAD: {RealComissao18NAD:.2f}')
            print(
                f'{int(porcentagemOperador)}% do Operador: {RealComissaoOperador:.2f}')
            print()

        else:
            print(
                f'{int(porcentagemNAD)}% NAD (com +10% do seguro): {RealComissao18NAD:.2f}')
            print(
                f'{int(porcentagemOperador)}% do Operador (com +5% do seguro): {RealComissaoOperador:.2f}')
            print()

    except ValueError:
        messagebox.showerror(
            "Erro", 'Por favor, insira valores numéricos válidos, lembre-se de não usar vírgulas e caso não haja seguro, digite 0 no custo dele.')


# Criar a janela principal
root = tk.Tk()
root.title("Clovinho's Calculator")

# Criar variáveis de controle
chk_value = IntVar(value=0)

# Criar campos de entrada
tk.Label(root, text="Valor total do cruzeiro (USD):").grid(row=0, column=0)
total_entry = tk.Entry(root)
total_entry.grid(row=0, column=1)

tk.Label(root, text="Taxa de governo (TG) (USD):").grid(row=1, column=0)
tg_entry = tk.Entry(root)
tg_entry.grid(row=1, column=1)

tk.Label(root, text="Número de noites no cruzeiro:").grid(row=2, column=0)
noites_entry = tk.Entry(root)
noites_entry.grid(row=2, column=1)

tk.Label(root, text="Número de passageiros (pax):").grid(row=3, column=0)
pax_entry = tk.Entry(root)
pax_entry.grid(row=3, column=1)

tk.Label(root, text="Valor do seguro (USD):").grid(row=4, column=0)
seguro_entry = tk.Entry(root, state='disabled')
seguro_entry.grid(row=4, column=1)
seguro_entry.insert(0, '0')


checkbox = tk.Checkbutton(root, text="Seguro incluso?",
                          variable=chk_value, onvalue=1, offvalue=0, command=toggle_seguro_entry).grid(row=5, columnspan=2)


tk.Label(root, text="Porcentagem da NAD (%):").grid(row=6, column=0)
porcentagemNAD_entry = tk.Entry(root)
porcentagemNAD_entry.grid(row=6, column=1)

tk.Label(root, text="Porcentagem do Operador (%):").grid(row=7, column=0)
porcentagemOP_entry = tk.Entry(root)
porcentagemOP_entry.grid(row=7, column=1)

# Botão para calcular
calcular_button = tk.Button(root, text="Calcular", command=calcular)
calcular_button.grid(row=8, columnspan=3)


# Iniciar o loop principal da GUI
root.mainloop()
