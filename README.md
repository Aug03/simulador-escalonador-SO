# Escalonador de Processos

Um simulador de escalonamento de processos desenvolvido em **Python**.

O programa simula a execução concorrente de múltiplos processos, utilizando um algoritmo de escalonamento baseado em **prioridades e créditos**. Cada processo possui um quantum de execução, registradores próprios (X e Y), um contador de programa (PC) e um estado que determina sua disponibilidade para utilizar a CPU.

A simulação contempla a execução de instruções, interrupções por esgotamento do quantum, bloqueios por operações de entrada e saída (E/S) e término de processos.

Os processos são representados por estruturas de controle de processos (**BCP**), responsáveis por armazenar seus respectivos estados e contextos de execução.

## Funcionamento do Escalonador

### 1. Prioridades e Créditos

Cada processo recebe uma prioridade inicial, definida no arquivo `prioridades.txt`. Essa prioridade também determina sua quantidade inicial de créditos.

- **Seleção de processos:** A fila de prontos é ordenada em ordem decrescente de créditos. O processo com mais créditos recebe a CPU primeiro.
- **Consumo de créditos:** A cada despacho para execução, o processo perde um crédito, independentemente da quantidade de instruções executadas.
- **Redistribuição:** Quando todos os processos ativos, incluindo os bloqueados, esgotam seus créditos, eles são restaurados de acordo com suas prioridades originais.

### 2. Quantum de Execução

O quantum determina o número máximo de instruções que um processo pode executar em cada despacho.

Quando o quantum é esgotado, o processo é interrompido e retorna à fila de prontos, aguardando uma nova oportunidade de execução.

A interrupção também pode ocorrer quando o processo solicita uma operação de E/S ou executa a instrução `SAIDA`.

### 3. Operações de Entrada e Saída

Quando um processo executa a instrução `E/S`, ele é transferido para a fila de bloqueados e recebe um tempo de espera de dois ciclos.

Durante esse período, outros processos podem utilizar a CPU. Quando o tempo de espera termina, o processo retorna à fila de prontos.

Caso todos os processos estejam bloqueados, o escalonador avança o tempo de espera até que algum processo seja desbloqueado.

### 4. Estados dos Processos

Os processos podem assumir três estados durante a simulação:

| Estado | Descrição |
|---|---|
| `PRONTO` | Aguarda na fila de prontos para utilizar a CPU. |
| `EXECUTANDO` | Está utilizando a CPU e executando suas instruções. |
| `BLOQUEADO` | Aguarda a conclusão de uma operação de E/S. |

Ao executar a instrução `SAIDA`, o processo é finalizado e removido da tabela de processos ativos.

## Estrutura dos Arquivos

O diretório `programas/` contém os arquivos de configuração e os dez programas utilizados na simulação.

| Arquivo | Descrição |
|---|---|
| `01.txt` a `10.txt` | Programas compostos pelas instruções utilizadas na simulação. |
| `prioridades.txt` | Define a prioridade inicial de cada processo, seguindo a ordem alfabética dos arquivos. |
| `quantum.txt` | Define o quantum de execução utilizado pelo escalonador. |

Cada arquivo de programa contém um identificador na primeira linha, seguido pelas instruções que serão executadas.

### Instruções disponíveis

| Instrução | Descrição |
|---|---|
| `X=<valor>` | Atribui um valor inteiro ao registrador X. |
| `Y=<valor>` | Atribui um valor inteiro ao registrador Y. |
| `COM` | Representa uma instrução de processamento, consumindo uma unidade do quantum. |
| `E/S` | Interrompe a execução e bloqueia o processo por dois ciclos. |
| `SAIDA` | Finaliza a execução do processo. |

## Execução

O escalonador pode ser executado diretamente pelo terminal, a partir do diretório raiz do projeto.

### Executando o escalonador

```bash
python Escalonador.py
```

Por padrão, o programa procura os arquivos de entrada no diretório `programas/`.

Também é possível especificar outro diretório contendo os arquivos de configuração e os programas:

```bash
python Escalonador.py <diretorio>
```

### Arquivos de Log

Ao finalizar a simulação, o programa gera um arquivo de log no diretório de execução, contendo o histórico de carregamento, execução, interrupção e término dos processos.

O nome do arquivo é definido pelo quantum utilizado:

| Quantum | Arquivo gerado |
|---|---|
| 1 | `log01.txt` |
| 2 | `log02.txt` |
| 5 | `log05.txt` |
| 10 | `log10.txt` |
| 20 | `log20.txt` |

Ao final de cada log, são apresentadas as seguintes estatísticas:

- **Média de trocas:** média de interrupções contabilizadas por processo.
- **Média de instruções:** média de instruções executadas por despacho de CPU.
- **Quantum:** valor utilizado durante a simulação.

## Automação dos Testes

O arquivo `gerar_testes.py` automatiza a execução do escalonador para diferentes valores de quantum.

Para executar os testes:

```bash
python gerar_testes.py
```

O script percorre os seguintes valores:

```python
[1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
```

Para cada valor, o programa:

1. Atualiza o conteúdo de `programas/quantum.txt`.
2. Executa novamente `Escalonador.py`.
3. Gera o respectivo arquivo de log.

Ao final, são produzidos dez arquivos de log, permitindo comparar os resultados da simulação para diferentes configurações de quantum.
