import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalculadoraEstatistica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Estatística VAC")
        self.root.geometry("1200x800") # Pode ser necessário ajustar a geometria geral
        self.root.resizable(True, True)

        self.status_var = tk.StringVar(value="Pronto")
        self.tipo_agrupamento = tk.StringVar(value="discreto")
        self.prob_type_var = tk.StringVar(value="entre")
        self.resultados = {}

        # Atributos para os novos labels na Aba 4
        self.n_info_label = None
        self.formula_info_label = None

        self.setup_styles()
        self.setup_interface()

    def formatar_numero(self, valor, casas_decimais=2):
        # Função para formatação customizada de números
        if not isinstance(valor, (int, float)):
            return str(valor)
        
        valor_vezes_potencia_d = valor * (10**casas_decimais)
        parte_fracionaria = valor_vezes_potencia_d - int(valor_vezes_potencia_d + np.sign(valor_vezes_potencia_d)*1e-9) 
        digito_seguinte_original = int((abs(parte_fracionaria) * 10) + 1e-9) 
        
        valor_base_int = int(valor_vezes_potencia_d + np.sign(valor_vezes_potencia_d)*1e-9)
        fator_divisao = 10**casas_decimais
        
        if digito_seguinte_original >= 6: # Sua lógica original de arredondamento
            resultado_ajustado = (valor_base_int + np.sign(valor_base_int)) / fator_divisao if valor_base_int != 0 else np.sign(valor_base_int)*(1/fator_divisao)
        else:
            resultado_ajustado = valor_base_int / fator_divisao
            
        return f"{resultado_ajustado:.{casas_decimais}f}"


    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.bg_color = "#f0f2f5"
        self.accent_color = "#2c3e50" 
        self.primary_color = "#007bff" 
        self.success_color = "#28a745"
        self.card_bg = "#ffffff"
        self.border_color = "#d1d5db"

        self.font_family = "Segoe UI"
        # Tamanhos de fonte aumentados
        self.font_header = (self.font_family, 18, 'bold') 
        self.font_label = (self.font_family, 12)        
        self.font_button = (self.font_family, 12, 'bold') 
        self.font_mono = ("Consolas", 12)              

        self.root.configure(bg=self.bg_color) 

        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', foreground=self.accent_color, font=self.font_label, background=self.bg_color) 
        self.style.configure('CardSpecific.TLabel', background=self.card_bg, foreground=self.accent_color, font=self.font_label) 
        self.style.configure('Header.TLabel', font=self.font_header, foreground=self.accent_color, background=self.card_bg) 
        
        self.style.configure('Card.TFrame', background=self.card_bg, relief='solid', borderwidth=1, bordercolor=self.border_color)
        
        self.style.configure('TButton', font=self.font_button, padding=(10, 5))
        self.style.map('TButton',
            foreground=[('active', self.card_bg), ('!active', self.card_bg)],
            background=[('active', self.primary_color), ('!active', self.primary_color), ('pressed', self.accent_color)], 
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        self.style.configure('TRadiobutton', font=self.font_label, background=self.bg_color) 
        self.style.configure('CustomRadio.TRadiobutton', background=self.card_bg, font=self.font_label) 

        self.style.configure('Treeview.Heading', font=(self.font_family, 12, 'bold')) # Aumentado
        self.style.configure('Treeview', font=self.font_label, rowheight=30) # Aumentado rowheight


    def setup_interface(self):
        main_container = ttk.Frame(self.root, padding="15", style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text="Calculadora Estatística Descritiva", style='Header.TLabel').pack(side=tk.LEFT) 
        ttk.Button(header_frame, text="🔄 RESET", command=self.reset_geral).pack(side=tk.RIGHT, padx=(10,0))

        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.setup_tab_tipo()
        self.setup_tab_dados()
        self.setup_tab_resultados()
        self.setup_tab_normal() 

        status_bar_frame = ttk.Frame(self.root, style='TFrame', padding=(10,5))
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(status_bar_frame, textvariable=self.status_var, font=(self.font_family, 11)).pack(side=tk.LEFT) # Aumentado

    def setup_tab_tipo(self):
        tab_tipo = ttk.Frame(self.notebook, style='TFrame', padding=20)
        self.notebook.add(tab_tipo, text="1. Tipo de Dados")
        card_tipo = ttk.Frame(tab_tipo, style='Card.TFrame', padding=25)
        card_tipo.pack(fill=tk.BOTH, expand=True)
        ttk.Label(card_tipo, text="Selecione o Tipo de Agrupamento dos Dados", style='Header.TLabel').pack(pady=(0, 20), anchor="w") 
        
        ttk.Radiobutton(card_tipo, text="Agrupamento Discreto (Valores individuais e suas frequências)",
                            variable=self.tipo_agrupamento, value="discreto", style='CustomRadio.TRadiobutton').pack(anchor=tk.W, pady=10) # Aumentado pady
        ttk.Radiobutton(card_tipo, text="Agrupamento em Classes (Intervalos de valores e suas frequências)",
                            variable=self.tipo_agrupamento, value="classes", style='CustomRadio.TRadiobutton').pack(anchor=tk.W, pady=10) # Aumentado pady

        explicacao_frame = ttk.Frame(card_tipo, padding=(0,15,0,0), style='Card.TFrame') 
        explicacao_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        self.explicacao_text = tk.Text(explicacao_frame, height=8, wrap=tk.WORD,
                                        font=(self.font_family, 11), bg="#f9f9f9", relief='solid', borderwidth=1, # Aumentado
                                        highlightthickness=0, padx=10, pady=10)
        self.explicacao_text.pack(fill=tk.BOTH, expand=True)
        self.explicacao_text.insert(tk.END, """**Agrupamento Discreto:**
Utilizado quando os dados são valores específicos e distintos (Xi), cada um com sua respectiva frequência (Fi).
Exemplo: Número de acertos em uma prova (0, 1, 2, ..., 10) e quantos alunos obtiveram cada escore.

**Agrupamento em Classes:**
Utilizado para dados contínuos ou quando há uma grande variedade de dados discretos. Os dados são agrupados em intervalos (classes), e a frequência (Fi) de cada classe é registrada.
Exemplo: Alturas de pessoas (150-160cm, 160-170cm, ...) e quantas pessoas se encontram em cada faixa.""")
        self.explicacao_text.config(state=tk.DISABLED)
        ttk.Button(card_tipo, text="Próximo →", command=lambda: self.notebook.select(1)).pack(pady=(20,0), anchor="e")

    def _criar_frame_entrada_dados(self, parent_tab):
        container_dados = ttk.Frame(parent_tab, padding="15", style='TFrame')
        container_dados.pack(fill=tk.BOTH, expand=True)
        tipo_atual_frame = ttk.Frame(container_dados, style='Card.TFrame', padding="10")
        tipo_atual_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(tipo_atual_frame, text="Tipo de dados selecionado: ", style='CardSpecific.TLabel', font=(self.font_family, 12, 'bold')).pack(side=tk.LEFT) 
        self.tipo_label = ttk.Label(tipo_atual_frame, text="Discreto", foreground=self.primary_color, style='CardSpecific.TLabel', font=(self.font_family, 12, 'bold')) 
        self.tipo_label.pack(side=tk.LEFT)
        return container_dados

    def _setup_entrada_discreta(self, parent_container):
        self.frame_discreto = ttk.Frame(parent_container, style='Card.TFrame', padding="15")
        ttk.Label(self.frame_discreto, text="Entrada de Dados Discretos (Xi, Fi)", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(anchor="w", pady=(0,10)) 
        controles_discreto = ttk.Frame(self.frame_discreto, style='Card.TFrame') 
        controles_discreto.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controles_discreto, text="Valor (Xi):", style='CardSpecific.TLabel').grid(row=0, column=0, padx=(0,5), pady=5, sticky="w") 
        self.xi_entry = ttk.Entry(controles_discreto, width=12, font=self.font_label)
        self.xi_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(controles_discreto, text="Frequência (Fi):", style='CardSpecific.TLabel').grid(row=0, column=2, padx=(10,5), pady=5, sticky="w") 
        self.fi_entry = ttk.Entry(controles_discreto, width=12, font=self.font_label)
        self.fi_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(controles_discreto, text="Adicionar", command=self.adicionar_discreto).grid(row=0, column=4, padx=(10,0), pady=5)
        tree_frame_discreto = ttk.Frame(self.frame_discreto, style='Card.TFrame') 
        tree_frame_discreto.pack(fill=tk.BOTH, expand=True)
        self.tree_discreto = ttk.Treeview(tree_frame_discreto, columns=('Xi', 'Fi'), show='headings', height=7, style='Treeview') # height pode precisar de ajuste
        self.tree_discreto.heading('Xi', text='Valor (Xi)'); self.tree_discreto.column('Xi', width=150, anchor=tk.CENTER) # Aumentado width
        self.tree_discreto.heading('Fi', text='Frequência (Fi)'); self.tree_discreto.column('Fi', width=150, anchor=tk.CENTER) # Aumentado width
        self.tree_discreto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_discreto = ttk.Scrollbar(tree_frame_discreto, orient="vertical", command=self.tree_discreto.yview)
        scrollbar_discreto.pack(side=tk.RIGHT, fill="y")
        self.tree_discreto.configure(yscrollcommand=scrollbar_discreto.set)

    def _setup_entrada_classes(self, parent_container):
        self.frame_classes = ttk.Frame(parent_container, style='Card.TFrame', padding="15")
        ttk.Label(self.frame_classes, text="Entrada de Dados Agrupados em Classes", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(anchor="w", pady=(0,10)) 
        controles_classes = ttk.Frame(self.frame_classes, style='Card.TFrame') 
        controles_classes.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controles_classes, text="Limite Inf. (Li):", style='CardSpecific.TLabel').grid(row=0, column=0, padx=(0,5), pady=5, sticky="w") 
        self.li_entry = ttk.Entry(controles_classes, width=10, font=self.font_label)
        self.li_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(controles_classes, text="Limite Sup. (Ls):", style='CardSpecific.TLabel').grid(row=0, column=2, padx=(10,5), pady=5, sticky="w") 
        self.ls_entry = ttk.Entry(controles_classes, width=10, font=self.font_label)
        self.ls_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(controles_classes, text="Frequência (Fi):", style='CardSpecific.TLabel').grid(row=0, column=4, padx=(10,5), pady=5, sticky="w") 
        self.fi_classe_entry = ttk.Entry(controles_classes, width=10, font=self.font_label)
        self.fi_classe_entry.grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(controles_classes, text="Adicionar", command=self.adicionar_classe).grid(row=0, column=6, padx=(10,0), pady=5)
        tree_frame_classes = ttk.Frame(self.frame_classes, style='Card.TFrame') 
        tree_frame_classes.pack(fill=tk.BOTH, expand=True)
        self.tree_classes = ttk.Treeview(tree_frame_classes, columns=('Li', 'Ls', 'h', 'Fi', 'PM'), show='headings', height=7, style='Treeview') # height pode precisar de ajuste
        col_widths_classes = {'Li': 100, 'Ls': 100, 'h': 90, 'Fi': 100, 'PM': 110} # Aumentado width
        col_names_classes = {'Li': 'Lim. Inf (Li)', 'Ls': 'Lim. Sup (Ls)', 'h': 'Ampl (h)', 'Fi': 'Freq (Fi)', 'PM': 'Ponto Médio (PM)'}
        for col_id, col_text in col_names_classes.items():
            self.tree_classes.heading(col_id, text=col_text)
            self.tree_classes.column(col_id, width=col_widths_classes[col_id], anchor=tk.CENTER)
        self.tree_classes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_classes = ttk.Scrollbar(tree_frame_classes, orient="vertical", command=self.tree_classes.yview)
        scrollbar_classes.pack(side=tk.RIGHT, fill="y")
        self.tree_classes.configure(yscrollcommand=scrollbar_classes.set)

    def setup_tab_dados(self):
        tab_dados = ttk.Frame(self.notebook, style='TFrame', padding=10)
        self.notebook.add(tab_dados, text="2. Entrada de Dados")
        container_dados = self._criar_frame_entrada_dados(tab_dados)
        self._setup_entrada_discreta(container_dados)
        self._setup_entrada_classes(container_dados)
        botoes_acao_frame = ttk.Frame(container_dados, style='Card.TFrame', padding="10")
        botoes_acao_frame.pack(fill=tk.X, pady=(10,0))
        ttk.Button(botoes_acao_frame, text="Calcular Estatísticas", command=self.calcular_estatisticas).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(botoes_acao_frame, text="Limpar Dados da Tabela", command=self.limpar_dados).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_acao_frame, text="Ver Resultados →", command=lambda: self.notebook.select(2)).pack(side=tk.RIGHT)
        self.tipo_agrupamento.trace_add("write", self.atualizar_tipo)
        self.atualizar_tipo()

    def setup_tab_resultados(self):
        tab_resultados = ttk.Frame(self.notebook, style='TFrame', padding=20)
        self.notebook.add(tab_resultados, text="3. Resultados Descritivos")
        card_resultados = ttk.Frame(tab_resultados, style='Card.TFrame', padding=20)
        card_resultados.pack(fill=tk.BOTH, expand=True)
        ttk.Label(card_resultados, text="Estatísticas Descritivas da Amostra", style='Header.TLabel').pack(pady=(0, 15), anchor="w") 
        self.resultado_text = scrolledtext.ScrolledText(card_resultados, wrap=tk.WORD,
                                                        font=self.font_mono, bg="#fdfdfd", relief='solid', borderwidth=1,
                                                        highlightthickness=0, height=18, padx=10, pady=10) # Ajustado height
        self.resultado_text.pack(fill=tk.BOTH, expand=True)
        self.resultado_text.insert(tk.END, "Aguardando cálculos...\n\nSelecione o tipo de dados e insira-os na aba '2. Entrada de Dados', depois clique em 'Calcular Estatísticas'.")
        self.resultado_text.config(state=tk.DISABLED)

    def _setup_scrollable_normal_tab(self, parent_tab):
        canvas = tk.Canvas(parent_tab, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame', padding="20")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(event):
            scroll_units = 0
            if event.num == 4: scroll_units = -1 
            elif event.num == 5: scroll_units = 1 
            else: scroll_units = int(-1 * (event.delta / 120)) 
            canvas.yview_scroll(scroll_units, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel, add="+") 
        canvas.bind_all("<Button-4>", _on_mousewheel, add="+") 
        canvas.bind_all("<Button-5>", _on_mousewheel, add="+") 
        return scrollable_frame, canvas

    def setup_tab_normal(self):
        tab_normal = ttk.Frame(self.notebook, style='TFrame', padding=0) 
        self.notebook.add(tab_normal, text="4. Distribuição Normal")
        container_normal, self.normal_canvas = self._setup_scrollable_normal_tab(tab_normal)
        self.normal_scrollable_frame = container_normal 

        info_norm_card = ttk.Frame(container_normal, style='Card.TFrame', padding="15")
        info_norm_card.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(info_norm_card, text="Distribuição Normal Estimada (Parâmetros da Amostra)", style='Header.TLabel', font=(self.font_family, 14, 'bold')).pack(anchor="w") # Aumentado
        
        self.media_label = ttk.Label(info_norm_card, text="Média (x̄): Não calculada", style='CardSpecific.TLabel', font=self.font_label) 
        self.media_label.pack(anchor=tk.W, pady=(5,2)) 
        
        self.desvio_label = ttk.Label(info_norm_card, text="Desvio Padrão (s): Não calculado", style='CardSpecific.TLabel', font=self.font_label) 
        self.desvio_label.pack(anchor=tk.W, pady=(0,2)) 

        self.n_info_label = ttk.Label(info_norm_card, text="Tamanho da Amostra (n): Não calculado", style='CardSpecific.TLabel', font=self.font_label)
        self.n_info_label.pack(anchor=tk.W, pady=(0,2))

        self.formula_info_label = ttk.Label(info_norm_card, text="Fórmula Z usada: Z = (x - x̄) * √n / s", style='CardSpecific.TLabel', font=self.font_label)
        self.formula_info_label.pack(anchor=tk.W, pady=(0,5))


        controles_prob_card = ttk.Frame(container_normal, style='Card.TFrame', padding="15")
        controles_prob_card.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controles_prob_card, text="Calcular Probabilidade na Normal", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(anchor="w", pady=(0,10)) # Aumentado
        
        prob_type_frame = ttk.Frame(controles_prob_card, style='Card.TFrame') 
        prob_type_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Radiobutton(prob_type_frame, text="P(X > a)", value="acima", variable=self.prob_type_var, command=self.atualizar_campos_prob, style='CustomRadio.TRadiobutton').pack(side=tk.LEFT, padx=(0,15))
        ttk.Radiobutton(prob_type_frame, text="P(X < a)", value="abaixo", variable=self.prob_type_var, command=self.atualizar_campos_prob, style='CustomRadio.TRadiobutton').pack(side=tk.LEFT, padx=(0,15))
        ttk.Radiobutton(prob_type_frame, text="P(a < X < b)", value="entre", variable=self.prob_type_var, command=self.atualizar_campos_prob, style='CustomRadio.TRadiobutton').pack(side=tk.LEFT)

        entrada_valores_frame = ttk.Frame(controles_prob_card, style='Card.TFrame') 
        entrada_valores_frame.pack(fill=tk.X, pady=(5,0))
        ttk.Label(entrada_valores_frame, text="Valor de 'x' (ou 'a'):", style='CardSpecific.TLabel').grid(row=0, column=0, padx=(0,5), pady=5, sticky="w") 
        self.a_entry = ttk.Entry(entrada_valores_frame, width=12, font=self.font_label)
        self.a_entry.grid(row=0, column=1, padx=0, pady=5)
        self.b_label = ttk.Label(entrada_valores_frame, text="Valor de 'b':", style='CardSpecific.TLabel') 
        self.b_label.grid(row=0, column=2, padx=(15,5), pady=5, sticky="w")
        self.b_entry = ttk.Entry(entrada_valores_frame, width=12, font=self.font_label)
        self.b_entry.grid(row=0, column=3, padx=0, pady=5)
        ttk.Button(entrada_valores_frame, text="Calcular Probabilidade", command=self.calcular_probabilidade).grid(row=0, column=4, padx=(20,0), pady=5, sticky="e")
        entrada_valores_frame.grid_columnconfigure(4, weight=1) 

        resultado_prob_card = ttk.Frame(container_normal, style='Card.TFrame', padding="15")
        resultado_prob_card.pack(fill=tk.X, pady=(0, 10))
        self.prob_resultado_text = scrolledtext.ScrolledText(resultado_prob_card, wrap=tk.WORD,
                                                              font=self.font_mono, bg="#fdfdfd", relief='solid', borderwidth=1,
                                                              highlightthickness=0, height=10, padx=10, pady=10) # Aumentado height
        self.prob_resultado_text.pack(fill=tk.BOTH, expand=True)
        self.prob_resultado_text.insert(tk.END, "Aguardando cálculo de probabilidade...")
        self.prob_resultado_text.config(state=tk.DISABLED)

        self.grafico_frame = ttk.Frame(container_normal, style='Card.TFrame', padding="15")
        self.grafico_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        ttk.Label(self.grafico_frame, text="Visualização Gráfica da Distribuição Normal", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(pady=(0,10), anchor="w") # Aumentado
        self.atualizar_campos_prob()
        self.atualizar_labels_normal() 

    def atualizar_tipo(self, *args):
        tipo = self.tipo_agrupamento.get()
        self.frame_discreto.pack_forget()
        self.frame_classes.pack_forget()
        if tipo == "discreto":
            self.frame_discreto.pack(fill=tk.BOTH, expand=True, pady=(5,0))
            self.tipo_label.configure(text="Discreto")
        else:
            self.frame_classes.pack(fill=tk.BOTH, expand=True, pady=(5,0))
            self.tipo_label.configure(text="Classes")
        self.status_var.set(f"Modo de entrada alterado para: {tipo.capitalize()}")

    def atualizar_campos_prob(self):
        if self.prob_type_var.get() == "entre":
            self.b_label.grid()
            self.b_entry.grid()
        else:
            self.b_label.grid_remove()
            self.b_entry.grid_remove()

    def adicionar_discreto(self):
        try:
            xi_str = self.xi_entry.get().replace(',', '.')
            fi_str = self.fi_entry.get()
            if not xi_str or not fi_str:
                messagebox.showwarning("Entrada Vazia", "Os campos 'Valor (Xi)' e 'Frequência (Fi)' devem ser preenchidos.")
                return
            xi = float(xi_str); fi = int(fi_str)
            if fi <= 0:
                messagebox.showerror("Valor Inválido", "A frequência (Fi) deve ser um inteiro positivo.")
                return
            for item_id in self.tree_discreto.get_children():
                if float(self.tree_discreto.item(item_id)['values'][0].replace(',','.')) == xi:
                    messagebox.showwarning("Dado Duplicado", f"O valor Xi = {self.formatar_numero(xi)} já foi inserido.")
                    return
            self.tree_discreto.insert('', 'end', values=(self.formatar_numero(xi), fi))
            self.xi_entry.delete(0, tk.END); self.fi_entry.delete(0, tk.END)
            self.xi_entry.focus()
            self.status_var.set(f"Adicionado: Xi={self.formatar_numero(xi)}, Fi={fi}")
        except ValueError: messagebox.showerror("Entrada Inválida", "Xi deve ser um número e Fi um inteiro.")

    def adicionar_classe(self):
        try:
            li_str = self.li_entry.get().replace(',', '.')
            ls_str = self.ls_entry.get().replace(',', '.')
            fi_str = self.fi_classe_entry.get()

            if not li_str or not ls_str or not fi_str:
                messagebox.showwarning("Entrada Vazia", "Os campos Li, Ls e Fi devem ser preenchidos.")
                return

            li = float(li_str)
            ls = float(ls_str)
            fi = int(fi_str)

            if ls <= li:
                messagebox.showerror("Valor Inválido", "Ls deve ser maior que Li.")
                return
            if fi <= 0:
                messagebox.showerror("Valor Inválido", "Fi deve ser um inteiro positivo.")
                return

            h = ls - li
            pm = (li + ls) / 2
            
            li_formatado = self.formatar_numero(li)
            ls_formatado = self.formatar_numero(ls) 
            h_formatado = self.formatar_numero(h)
            pm_formatado = self.formatar_numero(pm)

            self.tree_classes.insert('', 'end', values=(
                li_formatado, ls_formatado,
                h_formatado, fi, pm_formatado))
            
            self.li_entry.delete(0, tk.END)
            self.ls_entry.delete(0, tk.END)
            self.fi_classe_entry.delete(0, tk.END)
            
            self.li_entry.insert(0, ls_formatado) 
            self.ls_entry.focus() 
            
            self.status_var.set(f"Classe [{li_formatado} ; {ls_formatado}) adicionada.")
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Li, Ls devem ser números e Fi um inteiro.")

    def _limpar_tabelas_e_resultados(self):
        for item in self.tree_discreto.get_children(): self.tree_discreto.delete(item)
        for item in self.tree_classes.get_children(): self.tree_classes.delete(item)
        self.resultados = {}
        self.resultado_text.config(state=tk.NORMAL); self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, "Dados limpos. Insira novos dados e calcule."); self.resultado_text.config(state=tk.DISABLED)
        
        self.prob_resultado_text.config(state=tk.NORMAL); self.prob_resultado_text.delete(1.0, tk.END)
        self.prob_resultado_text.insert(tk.END, "Aguardando cálculo de probabilidade."); self.prob_resultado_text.config(state=tk.DISABLED)
        
        for widget in self.grafico_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg): 
                widget.get_tk_widget().destroy()
            elif not (isinstance(widget, ttk.Label) and "Visualização Gráfica" in widget.cget("text")):
                 if widget.winfo_exists(): widget.destroy() 

        if not any(isinstance(w, ttk.Label) and "Visualização Gráfica" in w.cget("text") for w in self.grafico_frame.winfo_children()):
            ttk.Label(self.grafico_frame, text="Visualização Gráfica da Distribuição Normal", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(pady=(0,10), anchor="w") # Aumentado
            
        self.atualizar_labels_normal() 

    def limpar_dados(self):
        if messagebox.askyesno("Limpar Dados", "Limpar dados das tabelas e resultados?"):
            self._limpar_tabelas_e_resultados()
            self.status_var.set("Dados e resultados limpos.")

    def reset_geral(self):
        if messagebox.askyesno("Resetar Aplicação", "Resetar tudo? Dados, resultados e seleções serão perdidos."):
            self._limpar_tabelas_e_resultados()
            for entry in [self.xi_entry, self.fi_entry, self.li_entry, self.ls_entry,
                          self.fi_classe_entry, self.a_entry, self.b_entry]:
                if entry and entry.winfo_exists(): entry.delete(0, tk.END)
            
            self.tipo_agrupamento.set("discreto")
            self.prob_type_var.set("entre") 
            self.atualizar_campos_prob() 
            self.atualizar_tipo() 
            self.notebook.select(0) 
            self.status_var.set("Aplicação resetada.")

    def calcular_estatisticas(self):
        try:
            tipo_selecionado = self.tipo_agrupamento.get()
            if tipo_selecionado == "discreto":
                if not self.tree_discreto.get_children(): messagebox.showinfo("Sem Dados", "Não há dados discretos para calcular."); return
                self.calcular_discreto_stats()
            else: 
                if not self.tree_classes.get_children(): messagebox.showinfo("Sem Dados", "Não há dados de classes para calcular."); return
                self.calcular_classes_stats()
            
            self.exibir_resultados()
            self.atualizar_labels_normal() 
            self.notebook.select(2) 
            self.status_var.set(f"Estatísticas calculadas para dados '{tipo_selecionado.capitalize()}'.")
        except ValueError as ve: messagebox.showerror("Erro de Cálculo", str(ve)); self.status_var.set(f"Falha no cálculo: {str(ve)}")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado durante o cálculo: {str(e)}"); self.status_var.set("Erro inesperado no cálculo.")

    def calcular_discreto_stats(self):
        valores_xi = []; frequencias_fi = []
        for item_id in self.tree_discreto.get_children():
            v = self.tree_discreto.item(item_id)['values']
            valores_xi.append(float(str(v[0]).replace(',', '.'))); frequencias_fi.append(int(v[1]))
        
        if not valores_xi: raise ValueError("Dados discretos ausentes para cálculo.")
        n_total = sum(frequencias_fi)
        if n_total == 0: raise ValueError("Frequência total (n) é zero, não é possível calcular.")
        
        media_calc = sum(xi * fi for xi, fi in zip(valores_xi, frequencias_fi)) / n_total
        
        if n_total == 1: 
            variancia_calc = 0.0
        elif n_total < 1: 
             raise ValueError("n < 1, não é possível calcular estatísticas.")
        else: 
            variancia_calc = sum(fi * (xi - media_calc)**2 for xi, fi in zip(valores_xi, frequencias_fi)) / (n_total - 1)
        
        desvio_calc = np.sqrt(variancia_calc) if variancia_calc >= 0 else 0.0
        cv_calc = (desvio_calc / media_calc) * 100 if media_calc != 0 else 0.0 
        
        self.resultados = {'tipo': 'discreto', 'n': n_total, 'media': media_calc, 
                           'variancia': variancia_calc, 'desvio': desvio_calc, 'cv': cv_calc}

    def calcular_classes_stats(self):
        pontos_medios_pm = []; frequencias_fi = []
        for item_id in self.tree_classes.get_children():
            v = self.tree_classes.item(item_id)['values'] 
            pontos_medios_pm.append(float(str(v[4]).replace(',', '.'))); frequencias_fi.append(int(v[3]))

        if not pontos_medios_pm: raise ValueError("Dados de classes ausentes para cálculo.")
        n_total = sum(frequencias_fi)
        if n_total == 0: raise ValueError("Frequência total (n) é zero, não é possível calcular.")

        media_calc = sum(pm * fi for pm, fi in zip(pontos_medios_pm, frequencias_fi)) / n_total
        
        if n_total == 1:
            variancia_calc = 0.0
        elif n_total < 1:
             raise ValueError("n < 1, não é possível calcular estatísticas.")
        else: 
            variancia_calc = sum(fi * (pm - media_calc)**2 for pm, fi in zip(pontos_medios_pm, frequencias_fi)) / (n_total - 1)
            
        desvio_calc = np.sqrt(variancia_calc) if variancia_calc >= 0 else 0.0
        cv_calc = (desvio_calc / media_calc) * 100 if media_calc != 0 else 0.0
        
        self.resultados = {'tipo': 'classes', 'n': n_total, 'media': media_calc, 
                           'variancia': variancia_calc, 'desvio': desvio_calc, 'cv': cv_calc}

    def exibir_resultados(self):
        if not self.resultados: return
        r = self.resultados; tipo_str = "Discreto" if r['tipo'] == 'discreto' else "Classes"
        interpret_cv = "Baixa (<15%)" if r['cv'] < 15 else "Moderada (15%-30%)" if r['cv'] < 30 else "Alta (>30%)"
        
        res_str = f"""╔═ ESTATÍSTICAS DESCRITIVAS (AMOSTRA) ═╗
║ Tipo de Dados: {tipo_str}
║ Tamanho da Amostra (n): {r['n']}
╠═══════════════════════════════════╣
║ Média (x̄): {self.formatar_numero(r['media'], 2)}
║ Variância Amostral (s²): {self.formatar_numero(r['variancia'], 2)}
║ Desvio Padrão Amostral (s): {self.formatar_numero(r['desvio'], 2)}
║ Coef. de Variação (CV): {self.formatar_numero(r['cv'], 2)}% ({interpret_cv})
╠═══════════════════════════════════╣
║ Normal Estimada: N(μ≈{self.formatar_numero(r['media'],2)}, σ²≈{self.formatar_numero(r['variancia'],2)})
║ (Use Aba 4 para probabilidades com base nesta estimativa)
╚═══════════════════════════════════╝
"""
        self.resultado_text.config(state=tk.NORMAL); self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, res_str); self.resultado_text.config(state=tk.DISABLED)

    def atualizar_labels_normal(self):
        if self.resultados and 'media' in self.resultados:
            media_fmt = self.formatar_numero(self.resultados['media'], 2)
            desvio_fmt = self.formatar_numero(self.resultados['desvio'], 2)
            n_val = self.resultados['n']
            
            self.media_label.config(text=f"Média (x̄): {media_fmt}", foreground=self.success_color)
            self.desvio_label.config(text=f"Desvio Padrão (s): {desvio_fmt}", foreground=self.success_color)
            if self.n_info_label: 
                self.n_info_label.config(text=f"Tamanho da Amostra (n): {n_val}", foreground=self.success_color)
            if self.formula_info_label:
                 self.formula_info_label.config(foreground=self.accent_color) 
        else:
            self.media_label.config(text="Média (x̄): Não calculada", foreground=self.accent_color)
            self.desvio_label.config(text="Desvio Padrão (s): Não calculado", foreground=self.accent_color)
            if self.n_info_label:
                self.n_info_label.config(text="Tamanho da Amostra (n): Não calculado", foreground=self.accent_color)
            if self.formula_info_label:
                 self.formula_info_label.config(foreground=self.accent_color)


    def calcular_probabilidade(self):
        if not self.resultados or 'media' not in self.resultados:
            messagebox.showwarning("Dados Ausentes", "Calcule as estatísticas descritivas (Aba 2 e 3) primeiro."); self.notebook.select(1); return
        
        try:
            mu = self.resultados['media']      
            sigma = self.resultados['desvio']  
            n_val = self.resultados['n']       

            if sigma <= 0: 
                messagebox.showerror("Parâmetro Inválido", "Desvio Padrão (s) deve ser > 0 para calcular probabilidades na Normal. Se n=1 ou todos os valores são iguais, s=0.")
                return
            if n_val <= 0: 
                messagebox.showerror("Parâmetro Inválido", "Tamanho da amostra (n) deve ser > 0.")
                return

            tipo_prob = self.prob_type_var.get()
            val_a_str = self.a_entry.get().replace(',', '.')
            if not val_a_str: messagebox.showwarning("Entrada Vazia", "O 'Valor de x (ou a)' é obrigatório."); self.a_entry.focus(); return
            
            val_a = float(val_a_str)
            val_b = None 

            for widget in self.grafico_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg): widget.get_tk_widget().destroy()
                elif not (isinstance(widget, ttk.Label) and "Visualização Gráfica" in widget.cget("text")):
                    if widget.winfo_exists(): widget.destroy()
            if not any(isinstance(w, ttk.Label) and "Visualização Gráfica" in w.cget("text") for w in self.grafico_frame.winfo_children()):
                ttk.Label(self.grafico_frame, text="Visualização Gráfica da Distribuição Normal", style='CardSpecific.TLabel', font=(self.font_family, 13, 'bold')).pack(pady=(0,10), anchor="w") # Aumentado

            z_a = (val_a - mu) * np.sqrt(n_val) / sigma
            
            prob_calc = 0.0
            txt_calc_tipo = "" 
            z_b = None 

            if tipo_prob == "entre":
                val_b_str = self.b_entry.get().replace(',', '.')
                if not val_b_str: messagebox.showwarning("Entrada Vazia", "'Valor de b' é obrigatório para P(a<X<b)."); self.b_entry.focus(); return
                val_b = float(val_b_str)
                if val_a >= val_b: messagebox.showerror("Valores Inválidos", "Para P(a<X<b), 'a' deve ser < 'b'."); return
                
                z_b = (val_b - mu) * np.sqrt(n_val) / sigma
                prob_calc = stats.norm.cdf(z_b, 0, 1) - stats.norm.cdf(z_a, 0, 1) 
                txt_calc_tipo = f"P({self.formatar_numero(val_a)} < X < {self.formatar_numero(val_b)})"
            elif tipo_prob == "acima":
                prob_calc = 1 - stats.norm.cdf(z_a, 0, 1) 
                txt_calc_tipo = f"P(X > {self.formatar_numero(val_a)})"
            else: 
                prob_calc = stats.norm.cdf(z_a, 0, 1) 
                txt_calc_tipo = f"P(X < {self.formatar_numero(val_a)})"
            
            media_fmt = self.formatar_numero(mu, 2)
            desvio_fmt = self.formatar_numero(sigma, 2)
            z_a_fmt = self.formatar_numero(z_a, 3) 

            res_txt = f"""Parâmetros da Amostra Usados:
  Média (x̄) ≈ {media_fmt}
  Desvio Padrão (s) ≈ {desvio_fmt}
  Tamanho da Amostra (n) = {n_val}

Fórmula Z aplicada: Z = (x - x̄) * √n / s
--------------------------------------
Cálculo: {txt_calc_tipo}

  Para x = {self.formatar_numero(val_a)}:
    Z = ({self.formatar_numero(val_a)} - {media_fmt}) * √{n_val} / {desvio_fmt} 
      ≈ {z_a_fmt}
"""
            if tipo_prob == "entre" and z_b is not None:
                z_b_fmt = self.formatar_numero(z_b, 3)
                res_txt += f"""
  Para x = {self.formatar_numero(val_b)}:
    Z = ({self.formatar_numero(val_b)} - {media_fmt}) * √{n_val} / {desvio_fmt} 
      ≈ {z_b_fmt}
"""
            res_txt += f"""
Probabilidade ≈ {self.formatar_numero(prob_calc, 4)} ({self.formatar_numero(prob_calc*100, 2)}%)
"""
            self.prob_resultado_text.config(state=tk.NORMAL); self.prob_resultado_text.delete(1.0, tk.END)
            self.prob_resultado_text.insert(tk.END, res_txt); self.prob_resultado_text.config(state=tk.DISABLED)
            
            self.criar_grafico_normal(mu, sigma, val_a, val_b, tipo_prob, prob_calc)
            self.status_var.set(f"{txt_calc_tipo} calculado com Z modificado.")

        except ValueError: messagebox.showerror("Erro de Valor", "Os valores de 'x' (a e/ou b) devem ser numéricos.")
        except Exception as e: messagebox.showerror("Erro no Cálculo de Probabilidade", f"Falha: {str(e)}")


    def criar_grafico_normal(self, media, desvio, val_a, val_b, tipo_prob, prob_res):
        if desvio <= 0: return 
        
        fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=100) # Ligeiramente maior para acomodar fontes
        
        lim_x_inf, lim_x_sup = media - 3.8*desvio, media + 3.8*desvio
        eixo_x = np.linspace(lim_x_inf, lim_x_sup, 400)
        eixo_y_pdf = stats.norm.pdf(eixo_x, media, desvio) 
        
        ax.plot(eixo_x, eixo_y_pdf, color=self.primary_color, lw=1.8, label=f'N(x̄≈{self.formatar_numero(media,2)}, s≈{self.formatar_numero(desvio,2)})')
        
        a_f=self.formatar_numero(val_a,2)
        p_f=self.formatar_numero(prob_res,4)
        pc_f=self.formatar_numero(prob_res*100,2)
        tit="" 

        if tipo_prob == "acima":
            ax.fill_between(eixo_x,0,eixo_y_pdf,where=(eixo_x>=val_a),color=self.primary_color,alpha=0.45,interpolate=True)
            ax.axvline(val_a,color=self.accent_color,ls='--',lw=1.5)
            tit=f"P(X > {a_f}) ≈ {p_f} ({pc_f}%)"
        elif tipo_prob == "abaixo":
            ax.fill_between(eixo_x,0,eixo_y_pdf,where=(eixo_x<=val_a),color=self.primary_color,alpha=0.45,interpolate=True)
            ax.axvline(val_a,color=self.accent_color,ls='--',lw=1.5)
            tit=f"P(X < {a_f}) ≈ {p_f} ({pc_f}%)"
        else: 
            b_f=self.formatar_numero(val_b,2)
            ax.fill_between(eixo_x,0,eixo_y_pdf,where=((eixo_x>=val_a)&(eixo_x<=val_b)),color=self.primary_color,alpha=0.45,interpolate=True)
            ax.axvline(val_a,color=self.accent_color,ls='--',lw=1.5)
            ax.axvline(val_b,color=self.accent_color,ls='--',lw=1.5)
            tit=f"P({a_f} < X < {b_f}) ≈ {p_f} ({pc_f}%)"
        
        # Fontes do gráfico aumentadas
        ax.axvline(media,color=self.success_color,ls=':',lw=1.5,label=f'Média (x̄) ≈ {self.formatar_numero(media,2)}')
        ax.set_title(tit,fontsize=12,fontweight='bold',pad=10) # Aumentado
        ax.set_xlabel('Valores de X',fontsize=11) # Aumentado
        ax.set_ylabel('Densidade de Probabilidade',fontsize=11) # Aumentado
        ax.legend(fontsize=10,loc='best') # Aumentado
        ax.grid(True,ls=':',alpha=0.4)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10) # Aumentado
        
        plt.tight_layout(pad=0.8) # Ajustado pad
        canvas_tk = FigureCanvasTkAgg(fig,master=self.grafico_frame)
        canvas_tk.draw()
        canvas_tk.get_tk_widget().pack(fill=tk.BOTH,expand=True,pady=(3,0))
        
        self.status_var.set("Gráfico da Distribuição Normal gerado.")
        if hasattr(self, 'normal_canvas') and self.normal_canvas:
             self.root.after(100, lambda: self.normal_canvas.yview_moveto(0.6)) 


def main():
    root = tk.Tk()
    app = CalculadoraEstatistica(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"Erro fatal ao iniciar a aplicação: {e}")
        print(traceback.format_exc()) 
        print("\nVerifique se todas as bibliotecas necessárias estão instaladas:")
        print("  pip install numpy scipy matplotlib")
