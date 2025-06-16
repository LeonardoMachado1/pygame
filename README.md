### 💣 Campo Minado com Pygame
Uma recriação completa do clássico jogo Campo Minado, desenvolvida em Python com a biblioteca Pygame. O projeto possui uma interface gráfica inspirada na versão do Windows, com menus interativos, telas de vitória/derrota e todas as funcionalidades esperadas do jogo.

### ✨ Funcionalidades
'''Menu Inicial Interativo: '''Uma tela de boas-vindas com opções para "Iniciar" e ver os "Créditos".

Jogabilidade Clássica:

Clique com o botão esquerdo para revelar uma célula.

Clique com o botão direito para colocar/remover uma bandeira 🚩.

Revelação em cascata (flood fill) para células vazias.

Interface Gráfica Completa:

Contador de minas restantes e cronômetro.

Smiley interativo que muda de expressão conforme o estado do jogo (😀, 😮, 😎, 😵).

Efeito 3D nos botões e células.

Telas de Vitória e Derrota: Feedback visual claro ao final de cada partida.

Sistema de Reinício: Reinicie o jogo a qualquer momento clicando no smiley ou no botão correspondente nas telas de fim de jogo.

 ### 🎮 Como Jogar
Iniciar: Abra o jogo e clique no botão "Iniciar" no menu principal.

Primeiro Clique: O primeiro clique é sempre seguro. O tabuleiro e as minas são gerados após sua primeira jogada.

Revelar Células: Clique com o botão esquerdo para revelar as células. Um número indica quantas minas estão adjacentes àquela célula.

Marcar Minas: Use o botão direito para colocar uma bandeira onde você suspeita que haja uma mina.

Objetivo: Revele todas as células que não contêm minas para vencer o jogo. Se você clicar em uma mina, o jogo termina.

### 🛠️ Pré-requisitos
Para executar este projeto, você precisará ter o Python e a biblioteca Pygame instalados em sua máquina.

Python 3.x

Pygame

Se você não tiver o Pygame instalado, pode instalá-lo facilmente usando o pip:

pip install pygame

### 🚀 Como Executar
Clone ou baixe o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git

Substitua a URL pelo link do seu próprio repositório.

Navegue até a pasta do projeto:

cd seu-repositorio

Execute o arquivo Python:

python nome_do_arquivo.py

Substitua nome_do_arquivo.py pelo nome real do seu arquivo de jogo.

### 📂 Estrutura do Código
O código está contido em um único arquivo Python e é dividido nas seguintes seções:

Configurações Globais: Define constantes como tamanho do grid, número de minas, cores e dimensões da tela.

Classe Cell: Modela cada célula do tabuleiro, controlando seu estado (se é uma mina, se foi revelada, etc.) e sua lógica de desenho.

Classe Smiley: Gerencia o botão de reinício interativo.

Funções de UI: Funções auxiliares para desenhar elementos da interface, como botões e telas de sobreposição.

Função main(): O loop principal do jogo, que gerencia os diferentes estados (menu, jogando, fim de jogo), trata os eventos do usuário e atualiza a tela.

### 🔧 Personalização
Você pode facilmente modificar a dificuldade do jogo alterando as seguintes constantes no topo do arquivo de código:

# --- Configurações do Jogo ---
GRID_SIZE = 20  # Altere para um grid maior ou menor
CELL_SIZE = 30  # Altere o tamanho visual das células
NUM_MINES = 40  # Aumente ou diminua o número de minas

### ⚖️ Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

### 👥 Criadores
Este projeto foi desenvolvido por:

Pedro Henrique Canabarro

Leonardo Pinto Machado

Felipe Lemos
