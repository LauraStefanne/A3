import mysql.connector  # Conecta com o MySQL
from mysql.connector import Error

# Conectar ao banco de dados MySQL
def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='temperaturas_db',  # Nome do banco de dados
            user='root',  # Nome de usuário do MySQL
            password=''  # Senha do MySQL
        )
        if conn.is_connected():
            print("Conexão bem-sucedida ao MySQL!")
            return conn
    except Error as e:
        print("Erro ao conectar ao MySQL: {}".format(e))
        return None

# Inserir novas temperaturas
def inserir_temperatura(cursor, data, temperatura):
    try:
        cursor.execute("INSERT INTO temperaturas (data, temperatura) VALUES (%s, %s)", (data, temperatura))
        print("Temperatura inserida com sucesso!")
    except Error as e:
        print("Ocorreu um erro ao inserir a temperatura: {}".format(e))

# Mostrar as temperaturas registradas
def mostrar_historico(cursor):
    cursor.execute("SELECT * FROM temperaturas")
    registros = cursor.fetchall()

    if len(registros) == 0:
        print("Nenhuma temperatura registrada.")
    else:
        print("Histórico de Temperaturas:")
        for registro in registros:
            print("ID: {} | Data: {} | Temperatura: {} °C".format(registro[0], registro[1], registro[2]))

# Exibe os alertas de temperaturas elevadas
def mostrar_alertas(cursor):
    cursor.execute("SELECT data, temperatura FROM temperaturas WHERE temperatura > 60")
    alertas = cursor.fetchall()

    if len(alertas) == 0:
        print("Nenhum alerta de temperatura alta.")
    else:
        print("Alertas de Temperatura Alta:")
        for alerta in alertas:
            print("Temperatura Registrada: {} °C | Data: {}".format(alerta[1], alerta[0]))
            print("Alto Risco de Incêndio!")

# média do mês e do ano escolhido pelo usuário
def mostrar_media_mensal_anual(cursor):
    ano = input("Digite o ano (AAAA): ")
    mes = input("Digite o mês (MM): ")

    # média do mês específico
    query_mes = """
    SELECT AVG(temperatura) 
    FROM temperaturas 
    WHERE YEAR(data) = %s 
      AND MONTH(data) = %s
    """
    cursor.execute(query_mes, (ano, mes))
    media_mes = cursor.fetchone()[0]

    #média do ano inteiro
    query_ano = """
    SELECT AVG(temperatura) 
    FROM temperaturas 
    WHERE YEAR(data) = %s
    """
    cursor.execute(query_ano, (ano,))
    media_ano = cursor.fetchone()[0]

    if media_mes:
        print("Média de temperaturas em {}/{}: {:.2f} °C".format(mes, ano, media_mes))
    else:
        print("Nenhuma temperatura registrada no mês {}/{}.".format(mes, ano))

    if media_ano:
        print("Média de temperaturas no ano {}: {:.2f} °C".format(ano, media_ano))
    else:
        print("Nenhuma temperatura registrada no ano {}.".format(ano))

# quantidade de alertas de temperatura alta em um mês específico
def mostrar_alertas_mes(cursor):
    ano = input("Digite o ano (AAAA): ")
    mes = input("Digite o mês (MM): ")

    query_alertas_mes = """
    SELECT COUNT(*) 
    FROM temperaturas 
    WHERE YEAR(data) = %s 
      AND MONTH(data) = %s 
      AND temperatura > 60
    """
    cursor.execute(query_alertas_mes, (ano, mes))
    num_alertas = cursor.fetchone()[0]

    print("{} alerta(s) registrado(s) no mês {}/{}.".format(num_alertas, mes, ano))

# quantidade de alertas de temperatura alta em um ano específico
def mostrar_alertas_ano(cursor):
    ano = input("Digite o ano (AAAA): ")

    query_alertas_ano = """
    SELECT COUNT(*) 
    FROM temperaturas 
    WHERE YEAR(data) = %s 
      AND temperatura > 60
    """
    cursor.execute(query_alertas_ano, (ano,))
    num_alertas = cursor.fetchone()[0]

    print("{} alerta(s) registrado(s) no ano {}.".format(num_alertas, ano))

# inserir novas temperaturas
def inserir_dados_usuario(cursor):
    data = input("Digite a data (AAAA-MM-DD): ")
    temperatura = float(input("Digite a temperatura registrada (em Celsius): "))
    inserir_temperatura(cursor, data, temperatura)

# Principal
def main():
    conn = criar_conexao()
    if conn is None:
        return  # Sair se a conexão falhar

    cursor = conn.cursor()

    while True:
        print("Menu:")
        print("[ 1 ] Inserir nova temperatura")
        print("[ 2 ] Mostrar histórico de temperaturas")
        print("[ 3 ] Mostrar alertas de temperatura alta")
        print("[ 4 ] Mostrar média de temperaturas de um mês específico e do ano")
        print("[ 5 ] Mostrar quantidade de alertas de temperatura alta em um mês específico")
        print("[ 6 ] Mostrar quantidade de alertas de temperatura alta em um ano específico")
        print("[ 7 ] Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            inserir_dados_usuario(cursor)
            conn.commit()
        elif escolha == "2":
            mostrar_historico(cursor)
        elif escolha == "3":
            mostrar_alertas(cursor)
        elif escolha == "4":
            mostrar_media_mensal_anual(cursor)
        elif escolha == "5":
            mostrar_alertas_mes(cursor)
        elif escolha == "6":
            mostrar_alertas_ano(cursor)
        elif escolha == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

    # Fechar a conexão
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
