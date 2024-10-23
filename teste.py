import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados MySQL
def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Altere se necessário
            database='temperaturas_db',  # O nome do seu banco de dados
            user='root',  # Seu nome de usuário do MySQL
            password=''  # Sua senha do MySQL
        )
        if conn.is_connected():
            print("Conexão bem-sucedida ao MySQL!")
            return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para inserir novas temperaturas
def inserir_temperatura(cursor, data, temperatura):
    try:
        cursor.execute("INSERT INTO temperaturas (data, temperatura) VALUES (%s, %s)", (data, temperatura))
        print("Temperatura inserida com sucesso!")
    except Error as e:
        print(f"Ocorreu um erro ao inserir a temperatura: {e}")

# Função para mostrar as temperaturas registradas
def mostrar_historico(cursor):
    cursor.execute("SELECT * FROM temperaturas")
    registros = cursor.fetchall()

    if len(registros) == 0:
        print("\nNenhuma temperatura registrada.")
    else:
        print("\nHistórico de Temperaturas:")
        for registro in registros:
            print(f"ID: {registro[0]} | Data: {registro[1]} | Temperatura: {registro[2]} °C")

# Função para exibir os alertas de temperaturas elevadas
def mostrar_alertas(cursor):
    cursor.execute("SELECT data, temperatura FROM temperaturas WHERE temperatura > 50")
    alertas = cursor.fetchall()

    if len(alertas) == 0:
        print("\nNenhum alerta de temperatura alta.")
    else:
        print("\nAlertas de Temperatura Alta:")
        for alerta in alertas:
            print(f"Temperatura Registrada: {alerta[1]} °C | Data: {alerta[0]}")
            if alerta[1] > 60:
                print("Alto Risco de Incêndio!")

# Função para inserir novas temperaturas pelo usuário
def inserir_dados_usuario(cursor):
    data = input("Digite a data (YYYY-MM-DD): ")
    temperatura = float(input("Digite a temperatura registrada (em Celsius): "))
    inserir_temperatura(cursor, data, temperatura)

# Função principal
def main():
    conn = criar_conexao()
    if conn is None:
        return  # Sair se a conexão falhar

    cursor = conn.cursor()

    while True:
        print("\nMenu:")
        print("1. Inserir nova temperatura")
        print("2. Mostrar histórico de temperaturas")
        print("3. Mostrar alertas de temperatura alta")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            inserir_dados_usuario(cursor)
            conn.commit()  # Commit após a inserção
        elif escolha == "2":
            mostrar_historico(cursor)
        elif escolha == "3":
            mostrar_alertas(cursor)
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

    # Fechar a conexão
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main() 
