# Indexador e Buscador de Palavras

Um indexador e buscador de palavras desenvolvido em **C**.

Encontre todas as ocorrências de uma palavra em um texto qualquer, identificando as linhas em que ela aparece e sua frequência. O programa também contabiliza o número de comparações realizadas durante as buscas.

O índice remissivo pode ser construído utilizando duas estruturas de dados diferentes: **Lista Ligada** ou **Árvore Binária**. Dessa forma, é possível comparar empiricamente o custo das operações e observar suas respectivas complexidades assintóticas.

Além disso, o programa contabiliza as comparações realizadas durante a inserção dos elementos em cada estrutura.

## Complexidade das Estruturas de Dados

### 1. Lista Ligada

- **Custo de inserção:** \(O(N^2)\). É necessário comparar cada novo elemento com os elementos já inseridos para evitar duplicatas.
- **Custo de busca:** \(O(N)\). No pior caso, é necessário percorrer toda a lista para encontrar o elemento procurado.

### 2. Árvore Binária

- **Custo de inserção:** \(O(N \log N)\), considerando uma árvore aproximadamente balanceada. Cada inserção exige, em média, \(O(\log N)\) comparações.
- **Custo de busca:** \(O(\log N)\), considerando uma árvore balanceada. O número de comparações é proporcional à altura da árvore.

## Compilação e Execução

O projeto permite escolher qual estrutura de dados será utilizada durante a compilação.

### Lista Ligada

Compile utilizando:

```bash
gcc -Wall -o ep main2.c texto2.c indice_lista2.c
```

### Árvore Binária

Compile utilizando:

```bash
gcc -Wall -o ep main2.c texto2.c indice_arvore2.c
```

### Executando o programa

Após a compilação, execute o programa passando o caminho do arquivo `.txt` e a estrutura de dados desejada:

```bash
./ep <arquivo> <lista|arvore>
```

### Comandos disponíveis

Durante a execução, os seguintes comandos podem ser utilizados:

| Comando | Descrição |
|---|---|
| `busca <palavra>` | Busca todas as ocorrências da palavra informada. |
| `fim` | Encerra o programa. |
