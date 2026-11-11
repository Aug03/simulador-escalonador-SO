import os
import sys

class BCP:
    def __init__(self, nome, codigo, prioridade):
        self.nome = nome
        self.codigo = codigo
        self.pc = 0
        self.estado = "PRONTO"
        self.prioridade = prioridade
        self.creditos = prioridade
        self.registrador_x = 0
        self.registrador_y = 0
        self.tempo_espera_es = 0
        self.total_interrupcoes = 0

    def __repr__(self):
        return f"<BCP {self.nome} | Estado: {self.estado} | Créditos: {self.creditos} | PC: {self.pc}>"


class Escalonador:
    def __init__(self, diretorio_programas="programas"):
        self.diretorio_programas = diretorio_programas
        self.tabela_processos = []
        self.todos_bcps_criados = []
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.quantum = 0
        self.log_linhas = []
        self.total_instrucoes_executadas = 0
        self.total_quanta_executados = 0
        self.total_processos_iniciais = 0

    def carregar_arquivos(self):
        caminho_quantum = os.path.join(self.diretorio_programas, "quantum.txt")
        caminho_prioridades = os.path.join(self.diretorio_programas, "prioridades.txt")

        with open(caminho_quantum, "r") as f:
            self.quantum = int(f.read().strip())

        with open(caminho_prioridades, "r") as f:
            prioridades = [int(line.strip()) for line in f if line.strip()]

        arquivos = sorted([
            f for f in os.listdir(self.diretorio_programas)
            if f.endswith(".txt") and f not in ["quantum.txt", "prioridades.txt"]
        ])

        for idx, arq in enumerate(arquivos):
            prio = prioridades[idx]
            caminho_prog = os.path.join(self.diretorio_programas, arq)
            with open(caminho_prog, "r") as f:
                linhas = [l.strip() for l in f if l.strip()]

            nome_programa = linhas[0]
            codigo_instrucoes = linhas[1:]

            bcp = BCP(nome_programa, codigo_instrucoes, prio)
            self.tabela_processos.append(bcp)
            self.todos_bcps_criados.append(bcp)

        self.total_processos_iniciais = len(self.tabela_processos)

        self.fila_prontos = list(self.tabela_processos)
        self.ordenar_fila_prontos()

        for bcp in self.fila_prontos:
            self.log_linhas.append(f"Carregando {bcp.nome}")

    def ordenar_fila_prontos(self):
        self.fila_prontos.sort(key=lambda b: b.creditos, reverse=True)

    def verificar_redistribuicao_creditos(self):
        todos_zerados_prontos = all(b.creditos == 0 for b in self.fila_prontos)
        todos_zerados_bloqueados = all(b.creditos == 0 for b in self.fila_bloqueados)

        if todos_zerados_prontos and todos_zerados_bloqueados and (self.fila_prontos or self.fila_bloqueados):
            for bcp in self.tabela_processos:
                bcp.creditos = bcp.prioridade

    def decrementar_tempos_espera_es(self):
        desbloqueados = []
        for bcp in list(self.fila_bloqueados):
            bcp.tempo_espera_es -= 1
            if bcp.tempo_espera_es <= 0:
                bcp.estado = "PRONTO"
                self.fila_bloqueados.remove(bcp)
                desbloqueados.append(bcp)

        for bcp in desbloqueados:
            self.fila_prontos.append(bcp)

        if desbloqueados:
            self.ordenar_fila_prontos()

    def executar(self):
        self.carregar_arquivos()

        while self.tabela_processos:
            if not self.fila_prontos:
                while not self.fila_prontos and self.fila_bloqueados:
                    self.decrementar_tempos_espera_es()
                if not self.tabela_processos:
                    break

            self.verificar_redistribuicao_creditos()
            self.ordenar_fila_prontos()

            if not self.fila_prontos:
                continue

            processo = self.fila_prontos.pop(0)
            processo.estado = "EXECUTANDO"

            processo.creditos = max(0, processo.creditos - 1)

            self.log_linhas.append(f"Executando {processo.nome}")

            instrucoes_no_quantum = 0
            bloqueado_por_es = False
            terminou = False

            while instrucoes_no_quantum < self.quantum and processo.pc < len(processo.codigo):
                instrucao = processo.codigo[processo.pc]
                processo.pc += 1
                instrucoes_no_quantum += 1

                if instrucao.startswith("X="):
                    processo.registrador_x = int(instrucao.split("=")[1])
                elif instrucao.startswith("Y="):
                    processo.registrador_y = int(instrucao.split("=")[1])
                elif instrucao == "COM":
                    pass
                elif instrucao == "E/S":
                    bloqueado_por_es = True
                    break
                elif instrucao == "SAIDA":
                    terminou = True
                    break

            self.total_instrucoes_executadas += instrucoes_no_quantum
            self.total_quanta_executados += 1
            processo.total_interrupcoes += 1

            if terminou:
                self.log_linhas.append(
                    f"Interrompendo {processo.nome} após {instrucoes_no_quantum} "
                    f"{'instrução' if instrucoes_no_quantum == 1 else 'instruções'}"
                )
                self.log_linhas.append(
                    f"{processo.nome} terminado. X={processo.registrador_x}. Y={processo.registrador_y}"
                )
                self.tabela_processos.remove(processo)

            elif bloqueado_por_es:
                self.log_linhas.append(f"E/S iniciada em {processo.nome}")
                self.log_linhas.append(
                    f"Interrompendo {processo.nome} após {instrucoes_no_quantum} "
                    f"{'instrução' if instrucoes_no_quantum == 1 else 'instruções'}"
                )
                processo.estado = "BLOQUEADO"
                processo.tempo_espera_es = 2  
                self.fila_bloqueados.append(processo)

            else:
                self.log_linhas.append(
                    f"Interrompendo {processo.nome} após {instrucoes_no_quantum} "
                    f"{'instrução' if instrucoes_no_quantum == 1 else 'instruções'}"
                )
                processo.estado = "PRONTO"
                self.fila_prontos.append(processo)
                self.ordenar_fila_prontos()

            bloqueados_antigos = [b for b in self.fila_bloqueados if b != processo]
            for bcp in bloqueados_antigos:
                bcp.tempo_espera_es -= 1
                if bcp.tempo_espera_es <= 0:
                    bcp.estado = "PRONTO"
                    self.fila_bloqueados.remove(bcp)
                    self.fila_prontos.append(bcp)
            
            if self.fila_bloqueados:
                self.ordenar_fila_prontos()

        self.escrever_logfile()

    def _formatar_numero(self, valor):
        texto = f"{valor:.1f}"
        if texto.endswith(".0"):
            return texto[:-2]
        return texto

    def escrever_logfile(self):
        if self.total_processos_iniciais > 0:
            media_trocas = sum(b.total_interrupcoes for b in self.todos_bcps_criados) / self.total_processos_iniciais
        else:
            media_trocas = 0

        if self.total_quanta_executados > 0:
            media_instrucoes = self.total_instrucoes_executadas / self.total_quanta_executados
        else:
            media_instrucoes = 0

        self.log_linhas.append(f"MEDIA DE TROCAS: {self._formatar_numero(media_trocas)}")
        self.log_linhas.append(f"MEDIA DE INSTRUCOES: {self._formatar_numero(media_instrucoes)}")
        self.log_linhas.append(f"QUANTUM: {self.quantum}")

        nome_log = f"log{self.quantum:02d}.txt"
        with open(nome_log, "w") as f:
            f.write("\n".join(self.log_linhas) + "\n")


if __name__ == "__main__":
    diretorio = "programas"
    if len(sys.argv) > 1:
        diretorio = sys.argv[1]

    esc = Escalonador(diretorio_programas=diretorio)
    esc.executar()