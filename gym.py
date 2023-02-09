#!/usr/bin/env python
import sqlite3
import PySimpleGUI as sg

# Definicao tema PySimpleGui
sg.theme('Material2')


layout = [
    [sg.Text('Bem vindo a academia', font=('Helvatica', '24'), size=(100, 1))],
    [sg.Button('Listar Membros', key='LIST', size=(50, 2)), sg.Button(
        'Cadastrar Novo Membro', key="CREATE", size=(50, 2))],
    [sg.Button('Atulizar Membros', key="UPDATE", size=(50, 2)),
     sg.Button('Excluir Membros', key="DELETE", size=(50, 2))],
    [sg.Button('Sair', key='EXIT', size=(109, 2),
               button_color=(sg.DEFAULT_ERROR_BUTTON_COLOR[1]))],
]

window = sg.Window('Gym', layout, font=('Helvatica', '14'))

# Conexao banco de dados
db = sqlite3.connect('gym.db')

# Criar tabela no banco de dados


def createTable():
    q = """CREATE TABLE IF NOT EXISTS users
       (account_code INTEGER PRIMARY KEY,
        name TEXT NOT NULL, plan TEXT NOT NULL)"""""

    db.execute(q)

# Buscar usuario pela matricula


def getById(account_code):
    try:
        q = f"SELECT * FROM users WHERE account_code={account_code}"
        return db.execute(q).fetchone()
    except:
        print('sss')

# Criar usuario


def uiCreateUser():
    createLayout = [[sg.Text('Incluir Usuario', font=('Helvatica', '24'), key='UI_CREATE_USER')],
                    [sg.Text('Matricula'), sg.Input(
                        s=(15, 2), key="account_code")],
                    [sg.Text('Nome'), sg.Input(s=(15, 2), key="name")],
                    [sg.Text("Plano"), sg.Combo(
                        ['Light', 'Premiun', 'God'], key="plan")],
                    [sg.Button("Sair", key="CLOSE"), sg.Button("Salvar", key='SAVE')]]

    windowList = sg.Window('Gym - Create User', createLayout,
                           font=('Helvatica', '14'), modal=True)

    while True:
        event, values = windowList.read()
        print(event, values)
        if (event == 'SAVE'):
            createUser(values["account_code"], values["name"], values["plan"])

        elif event == sg.WIN_CLOSED or event == 'CLOSE':
            break

    windowList.close()


def createUser(accountCode, name, plan):
    try:

        q = f"INSERT INTO users (account_code, name, plan) VALUES ('{str(accountCode)}','{name}', '{plan}')"

        db.execute(q)

        db.commit()
        sg.popup(">>> Novo Usuario cadastrado")
    except sqlite3.IntegrityError:
        sg.popup('">>> Matricula ja cadastrada"')

# Listar todos os usuarios


def uiListUser():
    listLayout = [[sg.Text('Lista de Usuarios', font=(
        'Helvatica', '24'), key='UI_LIST_USER')]]

    users = listUsers()
    row = []
    for user in users:
        print(user[1])
        row.append(user[1])

    listLayout.append([sg.Listbox(row, s=(15, 15))])

    windowList = sg.Window('Gym Lista de usuarios',
                           listLayout, modal=True, font=('Helvatica', '14'))

    while True:
        event, values = windowList.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    windowList.close()


def listUsers():
    q = "SELECT * FROM users ORDER BY name"
    return db.execute(q)


# Atualizar usuario


def updateUsers():
    try:
        account_code = int(input("Digite a matricula do aluno"))

        userAlreadyExiste = getById(account_code)

        if userAlreadyExiste:
            name = input('Digite o novo nome: ')
            plan = input('Digite o novo plano: ')
            q = f"UPDATE users SET name='{name}', plan='{plan}' WHERE account_code='{str(account_code)}'"

            db.execute(q)
            db.commit()
        else:
            print('User not found')
    except:
        print('ERROU')


def deleteUser():
    try:
        account_code = int(input('Digite a matricula do aluno: '))
        q = f"DELETE FROM users WHERE account_code={account_code}"
        db.execute(q)
        db.commit()

        print('Usuario removido')
    except:
        print('Error')


def main():
    createTable()
    while True:
        event, value = window.read()

        if event == 'LIST':
            print(event)
            uiListUser()
        elif event == 'CREATE':
            print(event)
            uiCreateUser()
        elif event == 'UPDATE':
            print(event)
        elif event == 'DELETE':
            print(event)
        else:
            break


main()
