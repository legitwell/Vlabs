

### WEB RECON - BANNER

### LAB 01 - Versão do Web Server

---

**ID do Lab:** `3ac410dc6d3272268e955e1a7c50c17ffc621951`

**Alvo:** `172.16.1.60`

**Pergunta:** Utilize as técnicas de reconhecimento web no host 172.16.1.60 e informe qual a versão do Web Server.

**Resposta:** Para identificar o Web Server, utilizamos o `curl`. O `curl` é uma ferramenta de linha de comando para transferir dados com URLs. Usando a flag `-v` (verbose), ele nos mostra os cabeçalhos (headers) da resposta HTTP.

**Comando Utilizado:**

Bash

```
curl -v -s 172.16.1.60
```

**Explicação do Comando:**

- **`curl`**: A ferramenta de linha de comando.
    
- **`-v`**: (Verbose) Modo falador. Pede ao `curl` para mostrar os _headers_ da requisição ( `>` ) e da resposta ( `<` ).
    
- **`-s`**: (Silent) Modo silencioso. Esconde a barra de progresso, deixando a saída mais limpa.
    
- **`172.16.1.60`**: O IP do alvo.
    

**Resultado Obtido:** O cabeçalho `Server` na resposta HTTP revelou a versão do software:

```
< Server: Microsoft-IIS/7.5
```

- **Versão do Web Server:** `Microsoft-IIS/7.5`
    

### Evidência (Print do Resultado)

![](../assets/Pasted%20image%2020251111224902.png)


---

### WEB RECON - BANNER

### LAB 02 - Linguagem de Programação

---

**ID do Lab:** `b163c928848658140595de425edd41c26ce436a6`

**Alvo:** `172.16.1.60`

**Pergunta:** Utilize as técnicas de reconhecimento web no host 172.16.1.60 e informe qual a linguagem de programação é utilizada no WebServer.

**Resposta:** Usando o mesmo comando `curl` anterior, analisamos os cabeçalhos HTTP em busca do `X-Powered-By`. Este cabeçalho é frequentemente usado por servidores para anunciar a tecnologia de _back-end_ (como PHP, ASP.NET, Java, etc.).

**Comando Utilizado:**

Bash

```
curl -v -s 172.16.1.60
```

**Explicação do Comando:**

- **`curl -v -s`**: Novamente, usamos o `curl` em modo _verbose_ e _silent_ para ler os cabeçalhos da resposta.
    

**Resultado Obtido:** O cabeçalho `X-Powered-By` na resposta HTTP revelou a linguagem:

```
< X-Powered-By: ASP.NET
```

- **Linguagem:** `ASP.NET`
    

### Evidência (Print do Resultado)

![](../assets/Pasted%20image%2020251111224911.png)


---

### WEB RECON - BANNER

### LAB 03 - Versão da Linguagem

---

**ID do Lab:** `9b785135d804b3e8b068eacd3876b4d2884ec4a4`

**Alvo:** `172.16.1.60`

**Pergunta:** Utilize as técnicas de reconhecimento web no host 172.16.1.60 e informe qual a versão da linguagem de programação utilizada no WebServer.

**Resposta:** A resposta padrão (do Lab 02) não nos deu a versão _específica_ do ASP.NET. Para forçar o servidor a nos dar mais detalhes, fizemos uma requisição para um arquivo `.aspx` que não existe. Servidores IIS frequentemente respondem a erros de arquivos `.aspx` com um cabeçalho `X-AspNet-Version` detalhado.

**Comando Utilizado:**

Bash

```
curl -I 172.16.1.60/asdasdas.aspx
```

**Explicação do Comando:**

- **`curl`**: A ferramenta de linha de comando.
    
- **`-I`**: (HEAD) Pede ao `curl` para fazer uma requisição do tipo `HEAD`. Isso pede ao servidor para enviar **apenas os cabeçalhos** (headers) e não o corpo da página 404, tornando a saída limpa.
    
- **`172.16.1.60/asdasdas.aspx`**: O IP do alvo com um nome de arquivo `.aspx` inexistente para forçar o erro.
    

**Resultado Obtido:** A resposta `404 Not Found` incluiu o cabeçalho `X-AspNet-Version` que procurávamos:

```
Server: Microsoft-IIS/7.5
X-AspNet-Version: 2.0.50727
X-Powered-By: ASP.NET
```

- **Versão da Linguagem:** `2.0.50727`
    

### Evidência (Print do Resultado)

![](../assets/Pasted%20image%2020251111224929.png)
