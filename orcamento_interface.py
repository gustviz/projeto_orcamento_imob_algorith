import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tipos_imoveis import calcular_aluguel, calcular_parcela_contrato, gerar_parcelas_mensais
import csv

class OrcamentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Orçamento Imobiliário - R.M.")
        self.root.geometry("500x700")

        self.tipo_imovel = tk.StringVar()
        self.quartos = tk.StringVar(value="1")
        self.garagem = tk.StringVar(value="0")
        self.tem_criancas = tk.StringVar(value="nao")
        self.parcelas_contrato = tk.StringVar(value="1")
        
        self.criar_interface()
        
    def criar_interface(self):
        titulo = tk.Label(self.root, text="Gerador de Orçamento Imobiliário", 
                         font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        info_frame = tk.LabelFrame(self.root, text="Informações sobre os valores", padx=10, pady=10)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_text = """Apartamento: R$ 700,00 / 1 Quarto
Casa: R$ 900,00 / 1 Quarto
Estudio: R$ 1.200,00
Contrato: R$ 2.000,00 (parcelado em até 5 vezes)
Desconto de 5% em apartamentos para quem não possui crianças"""
        
        tk.Label(info_frame, text=info_text, justify="left", anchor="w").pack(anchor="w")
        
        # Formulário
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Tipo de Imóvel
        tk.Label(form_frame, text="Tipo de Imóvel:").grid(row=0, column=0, sticky="w", pady=5)
        tipo_combo = ttk.Combobox(form_frame, textvariable=self.tipo_imovel, 
                                  values=["Apartamento", "Casa", "Estudio"], 
                                  state="readonly", width=30)
        tipo_combo.grid(row=0, column=1, pady=5, sticky="ew")
        tipo_combo.bind("<<ComboboxSelected>>", self.on_tipo_change)
        
        # Quartos
        tk.Label(form_frame, text="Número de Quartos:").grid(row=1, column=0, sticky="w", pady=5)
        self.quartos_combo = ttk.Combobox(form_frame, textvariable=self.quartos, 
                                          values=["1", "2"], state="readonly", width=30)
        self.quartos_combo.grid(row=1, column=1, pady=5, sticky="ew")
        
        # Garagem
        tk.Label(form_frame, text="Vagas de Garagem:").grid(row=2, column=0, sticky="w", pady=5)
        garagem_entry = tk.Entry(form_frame, textvariable=self.garagem, width=32)
        garagem_entry.grid(row=2, column=1, pady=5, sticky="ew")
        tk.Label(form_frame, text="(Para Estudio: 2 vagas = R$ 250,00, cada vaga adicional = R$ 60,00)", 
                font=("Arial", 8)).grid(row=3, column=1, sticky="w")
        
        # Crianças
        tk.Label(form_frame, text="Possui crianças?").grid(row=4, column=0, sticky="w", pady=5)
        criancas_frame = tk.Frame(form_frame)
        criancas_frame.grid(row=4, column=1, sticky="w", pady=5)
        tk.Radiobutton(criancas_frame, text="Sim", variable=self.tem_criancas, 
                      value="sim").pack(side="left", padx=10)
        tk.Radiobutton(criancas_frame, text="Não", variable=self.tem_criancas, 
                      value="nao").pack(side="left")
        
        # Parcelas do Contrato
        tk.Label(form_frame, text="Parcelas do Contrato:").grid(row=5, column=0, sticky="w", pady=5)
        parcelas_spin = tk.Spinbox(form_frame, from_=1, to=5, textvariable=self.parcelas_contrato, 
                                   width=29)
        parcelas_spin.grid(row=5, column=1, pady=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botão Calcular
        btn_calcular = tk.Button(self.root, text="Calcular Orçamento", 
                                command=self.calcular, bg="#4CAF50", fg="white", 
                                font=("Arial", 10, "bold"), padx=20, pady=10)
        btn_calcular.pack(pady=15)
        
        # Resultado
        self.resultado_frame = tk.LabelFrame(self.root, text="Resultado", padx=10, pady=10)
        self.resultado_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.resultado_text = tk.Text(self.resultado_frame, height=8, wrap="word", 
                                      state="disabled", font=("Arial", 10))
        self.resultado_text.pack(fill="both", expand=True)
        
        # Botão Gerar CSV
        self.btn_csv = tk.Button(self.root, text="Gerar CSV (12 parcelas)", 
                                command=self.gerar_csv, state="disabled")
        self.btn_csv.pack(pady=5)
        
    def on_tipo_change(self, event=None):
        tipo = self.tipo_imovel.get()
        if tipo == "Estudio":
            self.quartos_combo.config(values=["0"], state="readonly")
            self.quartos.set("0")
        else:
            self.quartos_combo.config(values=["1", "2"], state="readonly")
            if self.quartos.get() == "0":
                self.quartos.set("1")
        
    def calcular(self):
        try:
            # Valida tipo de imóvel
            tipo = self.tipo_imovel.get()
            if not tipo:
                messagebox.showerror("Erro", "Por favor, selecione o tipo de imóvel.")
                return
            
            # Converte valores
            quartos = int(self.quartos.get())
            garagem = int(self.garagem.get() or 0)
            tem_criancas = self.tem_criancas.get() == "sim"
            num_parcelas = int(self.parcelas_contrato.get())
            
            # Calcula
            valor_aluguel = calcular_aluguel(tipo, quartos, garagem, tem_criancas)
            valor_parcela_contrato = calcular_parcela_contrato(num_parcelas)
            
            # Exibe resultado
            self.resultado_text.config(state="normal")
            self.resultado_text.delete("1.0", tk.END)
            
            resultado = f"""Imóvel: {tipo}
Quartos: {quartos if tipo != "Estudio" else "0 (Estudio)"}
Vagas: {garagem}
Crianças: {"Sim" if tem_criancas else "Não"}

Aluguel: R$ {valor_aluguel:.2f}
Contrato: R$ 2000.00 · {num_parcelas}x de R$ {valor_parcela_contrato:.2f}
"""
            self.resultado_text.insert("1.0", resultado)
            self.resultado_text.config(state="disabled")
            
            # Habilita botão CSV
            self.btn_csv.config(state="normal")
            self.resultado_atual = {
                'tipo': tipo,
                'quartos': quartos,
                'garagem': garagem,
                'tem_criancas': tem_criancas,
                'valor_aluguel': valor_aluguel,
                'num_parcelas_contrato': num_parcelas,
                'valor_parcela_contrato': valor_parcela_contrato
            }
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {str(e)}")
    
    def gerar_csv(self):
        try:
            if not hasattr(self, 'resultado_atual'):
                messagebox.showerror("Erro", "Calcule o orçamento primeiro.")
                return
            
            # Pede local para salvar
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="orcamento_12_parcelas.csv"
            )
            
            if not filename:
                return
            
            # Gera parcelas (incluindo parcelas do contrato nos primeiros meses)
            parcelas = gerar_parcelas_mensais(
                self.resultado_atual['valor_aluguel'], 
                12,
                self.resultado_atual['num_parcelas_contrato'],
                self.resultado_atual['valor_parcela_contrato']
            )
            
            # Salva CSV
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Mês', 'Valor Total (R$)'])
                for parcela in parcelas:
                    writer.writerow([parcela['mes'], f"{parcela['valor']:.2f}"])
            
            messagebox.showinfo("Sucesso", f"CSV gerado com sucesso!\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar CSV: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrcamentoApp(root)
    root.mainloop()

