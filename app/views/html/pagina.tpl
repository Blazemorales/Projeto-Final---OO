<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/favicon.ico" />
    <title>Página inicial</title>
    <script src="/static/js/pagina.js"></script>
</head>
<body>
    % if transfered:
    <link rel="stylesheet" type="text/css" href="/static/css/pagina.css">
    <div class=".centralizar">
        <h1>Olá, Você está logado como superusuário</h1>
        <div>
            <h2>Dados do {{"Super" if current_user.isAdmin() else ""}} Usuário:</h2>
            <p>Username: {{current_user.username}} </p>
            <p>Password: {{current_user.password}} </p>
            <div class= "button-container">
                <form action="/logout" method="post" style="text-align: center;">
                    <button type="submit">Logout</button>
                </form>
                <form action="/edit" method="get" style="text-align: center;">
                    <button type="submit">Editar usuário</button>
                </form>
                <form action="/chat" method="get" style="text-align: center;">
                    <button type="submit">Área de mensagens</button>
                </form>
                <form action="/portal" method="get" style="text-align: center;">
                    <button type="submit">Portal</button>
                </form>
                <form action="/admin" method="get" style="text-align: center;">
                    <button type="submit">Administração</button>
                </form>
            </div>
        </div>
    </div>

    % else:
    <link rel="stylesheet" type="text/css" href="/static/css/pagina.css">
    <div class=".centralizar">
        <h1>Opa, Amigo! Seja Bem-Vindo!!! </h1>
        <h1>Você ainda não se registrou em nossa página</h1>
        <h3>Faça AGORA seu login clicando no botão abaixo!</h3>
        <form action="/portal" method="get" style="text-align: center;">
          <button type="submit">LOGIN</button>
        </form>
    </div>    
    % end
</body>
</html>
