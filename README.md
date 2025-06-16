# 💣 Campo Minado com Pygame

Uma recriação completa do clássico jogo **Campo Minado**, desenvolvida em **Python** com a biblioteca **Pygame**. O projeto traz uma interface gráfica inspirada na versão do Windows, com menus interativos, telas de vitória/derrota e todas as funcionalidades esperadas do jogo.

> 💡 **Dica:** Para adicionar uma imagem ao seu README, tire um screenshot do jogo, crie uma *issue* no repositório, arraste a imagem para lá e copie o link gerado. Substitua `URL_DA_SUA_IMAGEM_AQUI` abaixo:

![Screenshot do Jogo](URL_DA_SUA_IMAGEM_AQUI)

---

### ✨ Funcionalidades

- **Menu Inicial Interativo:** Tela com opções para "Iniciar" e ver os "Créditos".
- **Jogabilidade Clássica:**
  - Clique esquerdo: Revela a célula.
  - Clique direito: Coloca ou remove uma bandeira 🚩.
  - Revelação em cascata para células vazias.
- **Interface Gráfica Completa:**
  - Contador de minas restantes e cronômetro.
  - Smiley interativo que muda de expressão (😀, 😮, 😎, 😵).
  - Efeito 3D nos botões e células.
- **Telas de Vitória e Derrota:** Feedback visual ao final de cada partida.
- **Sistema de Reinício:** Clique no smiley ou botão para recomeçar.

---

### 🎮 Como Jogar

1. **Iniciar:** Clique em "Iniciar" no menu principal.
2. **Primeiro Clique:** Sempre seguro — o tabuleiro só é gerado após ele.
3. **Revelar Células:** Clique esquerdo para revelar.
4. **Marcar Minas:** Clique direito para adicionar uma bandeira.
5. **Objetivo:** Revele todas as células sem minas para vencer. Clicar em uma mina encerra o jogo.

---

### 🛠️ Pré-requisitos

- **Python 3.x**
- **Pygame**

Instale o Pygame com:

```bash
pip install pygame
```

---

### 🚀 Como Executar

1 - Clone o repositório:

```bash
git clone https://github.com/LeonardoMachado1/pygame.git
```

2 - Acesse a pasta do projeto:

```bash
cd seu-repositorio (AKTEASNDAKSJDKAJSDKADS)
```

3 - Acesse a pasta do projeto:

```bash
python jogo_cg.py
```

---

### 📂 Estrutura do Código

O projeto está em um único arquivo Python, com as seguintes seções:

- **Configurações Globais:** Tamanho do grid, número de minas, cores, etc.
- **Classe `Cell`:** Representa cada célula e sua lógica.
- **Classe `Smiley`:** Gerencia o botão de reinício.
- **Funções de UI:** Desenho de botões e telas de fim de jogo.
- **Função `main()`:** Loop principal do jogo, estados e eventos.

---

### 🔧 Personalização

Você pode alterar a dificuldade modificando estas constantes no topo do código:

```
GRID_SIZE = 20     # Tamanho do grid
CELL_SIZE = 30     # Tamanho visual das células
NUM_MINES = 40     # Número de minas
```

---

### 👥 Criadores

Desenvolvido por:

- Pedro Henrique Canabarro  
- Leonardo Pinto Machado  
- Felipe Lemos

