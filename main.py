import pandas as pd

# DataFrame de exemplo com alguns cenários pré-definidos
dados = {
    "Temperatura_C": [24, 31, 38],
    "Umidade_%": [65, 40, 18],
    "Vento_km_h": [5, 18, 32],
    "Dias_sem_chuva": [1, 7, 18],
    "Alerta": ["Baixo Risco", "Médio Risco", "Alto Risco"]
}
df = pd.DataFrame(dados)


# Classe responsável pela mensagem de boas-vindas
class BemVindo:
    def __init__(self, nome):
        self.nome = nome

    def saudar(self):
        return f"Bem-vindo ao prevensor de queimadas naturais, {self.nome}!"


# Classe que prevê o risco de queimadas com base nos dados ambientais
class PrevisorQueimadas:
    def __init__(self, temperatura, umidade, vento, dias_sem_chuva):
        self.temperatura = temperatura
        self.umidade = umidade
        self.vento = vento
        self.dias_sem_chuva = dias_sem_chuva

    def calcular_probabilidade(self):
        # Cálculo simples com pesos para cada variável
        peso_temp = self.temperatura * 0.3
        peso_umid = (100 - self.umidade) * 0.3  # quanto menor a umidade, maior o risco
        peso_vento = self.vento * 0.2
        peso_seco = self.dias_sem_chuva * 0.2

        prob = peso_temp + peso_umid + peso_vento + peso_seco

        # Garante que a probabilidade não passe de 100
        prob = min(prob, 100)
        return prob

    def classificar_risco(self):
        prob = self.calcular_probabilidade()

        if prob < 35:
            return "Baixo Risco"
        elif prob < 65:
            return "Médio Risco"
        else:
            return "Alto Risco"


# Função auxiliar genérica para perguntas de "sim/não"
def perguntar_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("sim", "não"):
            return resposta
        print("Resposta inválida. Por favor, responda com 'sim' ou 'não'.")


# Função que coleta os dados ambientais digitados pelo usuário
def coletar_dados_ambientais():
    print("\nPor favor, insira os seguintes dados ambientais:")

    temperatura = float(input("Insira a temperatura em °C: "))
    umidade = float(input("Insira a umidade em %: "))
    vento = float(input("Insira a velocidade do vento em km/h: "))
    dias_sem_chuva = int(input("Insira o número de dias sem chuva: "))

    # Retorna um dicionário com os dados para ser usado depois
    return {
        "Temperatura_C": temperatura,
        "Umidade_%": umidade,
        "Vento_km_h": vento,
        "Dias_sem_chuva": dias_sem_chuva
    }


# Função que recebe os dados, prevê o risco e mostra o DataFrame
def prever_risco(dados, nome_usuario=None):
    # Função encadeada para montar o DataFrame
    def montar_dataframe(dados_locais, risco_locais):
        """
        Função interna (encadeada) que monta o DataFrame
        a partir dos dados e do risco calculado.
        Ela só existe dentro de prever_risco.
        """
        dados_usuario = {
            "Temperatura_C": [dados_locais["Temperatura_C"]],
            "Umidade_%": [dados_locais["Umidade_%"]],
            "Vento_km_h": [dados_locais["Vento_km_h"]],
            "Dias_sem_chuva": [dados_locais["Dias_sem_chuva"]],
            "Risco_Classificado": [risco_locais]
        }
        return pd.DataFrame(dados_usuario)

    # Cria o objeto PrevisorQueimadas com os dados fornecidos
    previsor = PrevisorQueimadas(
        dados["Temperatura_C"],
        dados["Umidade_%"],
        dados["Vento_km_h"],
        dados["Dias_sem_chuva"]
    )

    # Calcula a classificação de risco
    risco = previsor.classificar_risco()

    # Mensagem personalizada se tiver nome de usuário
    if nome_usuario:
        print(f"\nCom base nos dados fornecidos {nome_usuario}, o risco de queimadas é classificado como: {risco}")
    else:
        print(f"\nCom base nos dados fornecidos, o risco de queimadas é classificado como: {risco}")

    # Usa a FUNÇÃO ENCADEADA para montar o DataFrame
    df_usuario = montar_dataframe(dados, risco)

    print("\nDataFrame gerado com os dados informados:")
    print(df_usuario)


# Função principal que controla o fluxo do programa
def main():
    # Pergunta se o usuário quer informar nome
    resposta_nome = perguntar_sim_nao("Deseja inserir nome de usuário? (sim/não): ")

    nome_usuario = None
    if resposta_nome == "sim":
        nome_usuario = input("Por favor, insira seu nome de usuário: ")
        bem_vindo = BemVindo(nome_usuario)
        print(bem_vindo.saudar())
        print(f"\nNosso programa {nome_usuario}, ajuda a identificar e prevenir problemas ecológicos através da análise de dados ambientais.")
    else:
        print("Bem-vindo ao prevensor de queimadas")
        print("\nNosso programa ajuda a identificar e prevenir problemas ecológicos através da análise de dados ambientais.")

    # Mostra o DataFrame de exemplo
    print("\nAqui estão alguns exemplos de dados ambientais coletados para prevenir queimadas:\n")
    print(df)

    # Pergunta se quer inserir dados ambientais
    resposta_dados = perguntar_sim_nao("\nDeseja inserir dados ambientais para prever o risco de queimadas? (sim/não): ")

    if resposta_dados == "sim":
        dados_usuario = coletar_dados_ambientais()
        prever_risco(dados_usuario, nome_usuario)
    else:
        if nome_usuario:
            print(f"\nObrigado por usar o prevensor de queimadas, {nome_usuario}. Até mais!")
        else:
            print("\nObrigado por usar o prevensor de queimadas. Até mais!")


# Garante que o main só rode quando o arquivo for executado diretamente
if __name__ == "__main__":
    main()