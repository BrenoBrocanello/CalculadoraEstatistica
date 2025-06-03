# 📊 Calculadora Estatística VAC

Uma aplicação de interface gráfica (GUI) desenvolvida em Python com Tkinter para realizar cálculos de estatística descritiva e probabilidades em uma distribuição normal estimada a partir dos dados da amostra.

## ✨ Funcionalidades Principais

* **Entrada de Dados Flexível:**
    * **Agrupamento Discreto:** Insira valores individuais (Xi) e suas respectivas frequências (Fi).
    * **Agrupamento em Classes:** Defina classes por limites inferior (Li) e superior (Ls) com suas frequências (Fi). O Ponto Médio (PM) e a Amplitude (h) da classe são calculados automaticamente.
* **Cálculos de Estatística Descritiva:**
    * Tamanho da Amostra (n)
    * Média Amostral (x̄)
    * Variância Amostral (s²)
    * Desvio Padrão Amostral (s)
    * Coeficiente de Variação (CV) com interpretação (Baixa, Moderada, Alta).
* **Distribuição Normal:**
    * Utiliza a média (x̄) e o desvio padrão (s) calculados da amostra como parâmetros (μ ≈ x̄, σ ≈ s).
    * Calcula probabilidades para a distribuição normal ajustada:
        * P(X > a)
        * P(X < a)
        * P(a < X < b)
    * Apresenta a fórmula Z utilizada: $Z = (x - \bar{x}) \cdot \sqrt{n} / s$.
    * **Visualização Gráfica:** Gera um gráfico da curva normal com a área de probabilidade hachurada.
* **Interface Intuitiva:**
    * Interface organizada em abas para facilitar a navegação:
        1.  Seleção do Tipo de Dados
        2.  Entrada de Dados
        3.  Resultados Descritivos
        4.  Distribuição Normal
    * Design moderno com temas e estilos (`ttk.Style`).
    * Feedback ao usuário através de uma barra de status.
    * Validação de entradas e mensagens de erro/aviso.
* **Gerenciamento de Dados:**
    * Botão para limpar dados da tabela atual.
    * Botão "RESET" para limpar todos os dados, resultados e redefinir seleções.
* **Formatação de Números:**
    * Função customizada para arredondamento e formatação de números com precisão decimal.

## 📋 Pré-requisitos

* Python 3.x
* Bibliotecas Python:
    * `numpy`
    * `scipy`
    * `matplotlib`

## ⚙️ Instalação

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    # Se estiver usando git
    git clone <url_do_repositorio>
    cd <pasta_do_repositorio>
    ```
2.  **Instale as dependências:**
    ```bash
    pip install numpy scipy matplotlib
    ```
    (Tkinter geralmente já vem incluído na instalação padrão do Python).

## 🚀 Como Usar

1.  **Execute o script Python:**
    ```bash
    python nome_do_seu_arquivo.py
    ```
    (Substitua `nome_do_seu_arquivo.py` pelo nome real do arquivo que contém o código).

2.  **Navegação e Uso:**
    * **Aba 1. Tipo de Dados:**
        * Selecione "Agrupamento Discreto" ou "Agrupamento em Classes".
        * Leia as explicações se necessário.
        * Clique em "Próximo →".
    * **Aba 2. Entrada de Dados:**
        * O tipo de entrada mudará conforme a seleção na Aba 1.
        * **Discreto:** Insira "Valor (Xi)" e "Frequência (Fi)" e clique em "Adicionar".
        * **Classes:** Insira "Limite Inf. (Li)", "Limite Sup. (Ls)" e "Frequência (Fi)" e clique em "Adicionar". O próximo "Li" será preenchido automaticamente com o "Ls" anterior para facilitar.
        * Após inserir todos os dados, clique em "Calcular Estatísticas".
        * Use "Limpar Dados da Tabela" para limpar apenas os dados inseridos.
        * Clique em "Ver Resultados →" para ir à aba de resultados.
    * **Aba 3. Resultados Descritivos:**
        * Visualize as estatísticas calculadas (n, média, variância, desvio padrão, CV).
    * **Aba 4. Distribuição Normal:**
        * Os parâmetros (média, desvio padrão, n) calculados da amostra serão exibidos.
        * Selecione o tipo de probabilidade: P(X > a), P(X < a) ou P(a < X < b).
        * Insira os valores de 'x' (ou 'a' e 'b').
        * Clique em "Calcular Probabilidade".
        * O resultado detalhado do cálculo de Z e da probabilidade será exibido, junto com um gráfico da distribuição normal.
    * **Botão 🔄 RESET (canto superior direito):** Reseta toda a aplicação, limpando todos os dados, resultados e seleções.

## 🛠️ Estrutura do Código

O código é organizado dentro da classe `CalculadoraEstatistica`:

* `__init__(self, root)`: Inicializa a janela principal, variáveis de estado e chama os métodos de configuração.
* `formatar_numero(self, valor, casas_decimais=2)`: Função utilitária para formatação customizada de números.
* `setup_styles(self)`: Configura os estilos visuais dos componentes ttk.
* `setup_interface(self)`: Cria a estrutura principal da interface, incluindo o cabeçalho e o notebook de abas.
* `setup_tab_tipo(self)`: Configura a primeira aba para seleção do tipo de dados.
* `_criar_frame_entrada_dados(self, parent_tab)`: Cria um frame base para a entrada de dados na segunda aba.
* `_setup_entrada_discreta(self, parent_container)`: Configura os campos e a tabela para entrada de dados discretos.
* `_setup_entrada_classes(self, parent_container)`: Configura os campos e a tabela para entrada de dados agrupados em classes.
* `setup_tab_dados(self)`: Configura a segunda aba, integrando as interfaces de entrada discreta e de classes.
* `setup_tab_resultados(self)`: Configura a terceira aba para exibir os resultados estatísticos.
* `_setup_scrollable_normal_tab(self, parent_tab)`: Cria uma aba com rolagem para a Distribuição Normal.
* `setup_tab_normal(self)`: Configura a quarta aba para cálculos e visualização da distribuição normal.
* `atualizar_tipo(self, *args)`: Alterna a visibilidade dos frames de entrada de dados (discreto/classes) com base na seleção.
* `atualizar_campos_prob(self)`: Mostra/esconde o campo para o valor 'b' na Aba 4 dependendo do tipo de probabilidade.
* `adicionar_discreto(self)` / `adicionar_classe(self)`: Adicionam os dados inseridos às respectivas tabelas (Treeview).
* `_limpar_tabelas_e_resultados(self)`: Limpa os dados das tabelas e os resultados exibidos.
* `limpar_dados(self)`: Ação do botão "Limpar Dados da Tabela".
* `reset_geral(self)`: Ação do botão "RESET".
* `calcular_estatisticas(self)`: Orquestra o cálculo das estatísticas com base no tipo de dado.
* `calcular_discreto_stats(self)` / `calcular_classes_stats(self)`: Realizam os cálculos estatísticos específicos para cada tipo de dado.
* `exibir_resultados(self)`: Formata e exibe os resultados estatísticos na Aba 3.
* `atualizar_labels_normal(self)`: Atualiza os labels com média, desvio padrão e 'n' na Aba 4.
* `calcular_probabilidade(self)`: Calcula a probabilidade na distribuição normal e chama a função de plotagem.
* `criar_grafico_normal(self, media, desvio, val_a, val_b, tipo_prob, prob_res)`: Gera e exibe o gráfico da distribuição normal com Matplotlib.
* `main()`: Função principal para instanciar e executar a aplicação.

## 📝 Observação sobre a Fórmula Z

Na Aba 4 (Distribuição Normal), a padronização para o escore Z utiliza a seguinte fórmula baseada nos parâmetros da amostra:
$Z = \frac{(x - \bar{x}) \cdot \sqrt{n}}{s}$
Onde:
* $x$: valor de interesse
* $\bar{x}$: média amostral
* $s$: desvio padrão amostral
* $n$: tamanho da amostra

Este escore Z é então usado com a função de distribuição acumulada (CDF) da normal padrão para calcular as probabilidades.

---

Desenvolvido como uma ferramenta para auxiliar em estudos estatísticos.
