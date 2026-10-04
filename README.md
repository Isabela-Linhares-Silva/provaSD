Sistema distribuído de mensagens desenvolvido em Python, utilizando Flask, HTTP/REST, JSON e Docker Compose.

Arquitetura:
O sistema é composto por um servidor Flask e três clientes independentes: Alice, Bob e Carol. Cada componente é executado em um container Docker separado.
Os clientes não se comunicam diretamente entre si, a comunicação ocorre por meio de requisições HTTP para API REST do servidor, que é responsavel pelo cadastro de usuários, armazenamento das mensagens e atualização de estado das leituras de mensagens.

End-points:
POST/usuarios: Utilizado para cadastrar um novo usuário;
GET/usuarios: Permite consultar usuarios cadastrados;
POST/mensagens: Cria e envia uma mensagem, informando rementente, destinatário e conteúdo;
GET/mensagens: Consulta mensagens e são utilizados como parametros de consulta para filtrat os resultados, como destinatário, remetente e lida.
O endpoint PATCH /mensagens/<id> é utilizado para atualizar uma mensagem. No projeto, ele é utilizado para marcar uma mensagem como lida.

Execução:
No inicio do projeto rodo: docker compose up --build
A execução dos clientes é automática e reproduz o cenário de demonstração: Alice e Carol enviam mensagens para Bob, Bob consulta suas mensagens não lidas, marca a mensagem de Alice como lida e realiza uma nova consulta.
E pra finalizar: docker compose down.