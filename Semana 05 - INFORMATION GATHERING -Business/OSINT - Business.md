
### LAB 01 - OSINT - Business

---

**ID do Lab:** `90ffda96ffce620d4ac8a08357bacc391a11f794`

**Análise / Alvo:** `businesscorp.com.br`

**Pergunta:** Realizar uma coleta de endereços e-mails para o domínio `businesscorp.com.br`.

![[Pasted image 20251102194850.png]]

**Resposta:** Para realizar a coleta de e-mails (OSINT), Abri o site e encontrei os 3 emails. 


### LAB 02 - OSINT - Business

---

**ID do Lab:** `96c62208eddb3eda917a32c79436f7b2a62b5a7b`

**Análise / Alvo:** `businesscorp.com.br`

**Pergunta:** Utilizar técnicas de Google Hacking no domínio `businesscorp.com.br` para encontrar um arquivo que contém informações sensíveis e inserir a "key" encontrada.

**Resposta:** Para encontrar arquivos sensíveis de forma passiva (OSINT), utilizamos o Google Hacking (Google Dorks). O objetivo é instruir o Google a filtrar resultados que correspondam a padrões de arquivos de configuração ou senhas expostas.

**Comando Utilizado (Google Dork):**

```
site:businesscorp.com.br inurl:senha
```

![[Pasted image 20251102195320.png]]


**Explicação do Comando:**

- **`site:businesscorp.com.br`**: Restringe a pesquisa do Google apenas para páginas indexadas dentro deste domínio específico.
    
- **`inurl:senha`**: Filtra os resultados, mostrando apenas páginas que contenham a palavra "senha" em sua URL. Isso é um forte indicador de arquivos de configuração, painéis de teste ou credenciais acidentalmente expostas.
    

**Resultado Obtido:** O Google Dork levou ao seguinte resultado:

- **URL Encontrada:** `http://www.businesscorp.com.br/config`
    

Ao acessar essa URL, foi encontrado um arquivo de configurações com o seguinte conteúdo:

```
CONFIGURACOES DO SERVIDOR

HARDWARE DELL

usuario: admin
senha: b3sac992883
```

- **KEY:** `Gh4ck1ng9988299311`

### LAB 03 - OSINT - Business

---

**ID do Lab:** `75957300bfb4e3f5aa0a0ea1fbc139a05cda5bcd`

**Análise / Alvo:** `businesscorp.com.br`

**Pergunta:** Utilizar técnicas de pesquisa em cache no domínio `businesscorp.com.br` e conseguir a key para pontuar.

**Resposta:** A investigação foi realizada em duas etapas. Primeiro, analisamos o arquivo `robots.txt` para identificar arquivos ou diretórios que o alvo tentou esconder dos motores de busca. Em seguida, usamos uma ferramenta de cache (Wayback Machine) para acessar o conteúdo de um arquivo que já havia sido removido do servidor.

**Metodologia / URLs Acessadas:**

1. **Análise do `robots.txt`:** `http://businesscorp.com.br/robots.txt`
2. ![[Pasted image 20251102200619.png]]

    
3. **Consulta ao Cache (Wayback Machine):** `http://web.archive.org/web/20191126114209/http://businesscorp.com.br/configuracoes/comunicacao/projeto.txt`
4. ![[Pasted image 20251102200637.png]]

    

**Explicação da Metodologia:**

1. O `robots.txt` é um arquivo que instrui _crawlers_ (como o Google). Paradoxalmente, ele é público e frequentemente vaza a localização de áreas sensíveis (como `/admin`, `/bkp`). Em vez de um `Disallow`, encontramos um `Allow` explícito para `.../projeto.txt`, o que é altamente suspeito.
    
2. Ao tentar acessar o arquivo diretamente (conforme implícito no lab), ele não estava mais disponível. A "técnica de cache" foi usar o **Wayback Machine (archive.org)** para encontrar um _snapshot_ (cópia histórica) dessa URL.
    

**Resultado Obtido:** O snapshot da Wayback Machine (datado de 26/Nov/2019) revelou o conteúdo do arquivo `projeto.txt`, que continha informações internas e a _key_ do desafio:

```
COMUNICACAO INTERNA PROJETO BUSINESSCORP
...
DEPARTAMENTOS ENVOLVIDOS
MARKETING, DESENVOLVIMENTO
...
TRELLO:
https://trello.com/b/kaqiiGDI/businesscorpcombr
...
KEY: c4ch3_1666277399911a
```

- **KEY:** `c4ch3_1666277399911a`


### LAB 04 - OSINT - Business

---

**ID do Lab:** `80c6f98a362afaad0135c0148222920fc8777711`

**Análise / Alvo:** `businesscorp.com.br` (Registros DNS e Trello)

**Pergunta:** Qual a senha e o nome do serviço é possível descobrir no painel do Trello da `businesscorp.com.br`?

**Resposta:** Para descobrir o painel Trello, foi realizada uma enumeração de subdomínios via **Transferência de Zona DNS (AXFR)**. Esta técnica explorou uma má configuração no nameserver do alvo, permitindo listar todos os registros DNS do domínio. A listagem revelou um subdomínio `trello.businesscorp.com.br` que, através de um registro CNAME, apontava para o painel Trello público.

**Comando Utilizado (Transferência de Zona):**

Bash

```
dig -t axfr businesscorp.com.br @ns2.businesscorp.com.br
```
![[Pasted image 20251102201957.png]]



**Explicação do Comando:**

- **`dig`**: Ferramenta de linha de comando para consulta de servidores DNS.
    
- **`-t axfr`**: Define o tipo (`-t`) de consulta como `AXFR` (Full Zone Transfer), solicitando ao servidor DNS todos os registros que ele possui para o domínio.
    
- **`businesscorp.com.br`**: O domínio alvo da enumeração.
    
- **`@ns2.businesscorp.com.br`**: Especifica o nameserver (`@`) que será consultado (o `ns2`, que estava vulnerável à transferência de zona).
    

**Resultado Obtido:** A transferência de zona (mostrada na segunda imagem) foi bem-sucedida e revelou o seguinte registro CNAME:

DNS Zone file

```
trello.businesscorp.com.br. 3600 IN CNAME trello.com/b/bl7wd8HN/businesscorpcombr.
```

![[Pasted image 20251102202036.png]]

Ao acessar a URL `https://trello.com/b/bl7wd8HN/businesscorpcombr`, um painel Trello público foi encontrado (primeira imagem). A análise dos _cards_ revelou as seguintes credenciais:

- **Serviço:** `webmin` (identificado no _card_ "Configurar webmin")
    
- **Senha:** `123qweAm` (identificada no _card_ "senha do businesscorp.com.br")


### LAB 05 - OSINT - Business

---

**ID do Lab:** `d2a19f76f7538e1ef65ee248e6bc513ccdcdf138`

**Análise / Alvo:** `Pastebin` (Vazamentos da `businesscorp.com.br`)

**Pergunta:** Existe alguma informação sensível da `businesscorp.com.br` no Pastebin?

**Resposta:** Sim. Dando continuidade à investigação do Lab 04, analisamos o link do Pastebin (`https://pastebin.com/57J3tLmc`) que foi encontrado em um _card_ do painel Trello público. Sites de _paste_ são comumente usados para compartilhar dados vazados (data leaks).

**Metodologia / URL Acessada:**

```
https://pastebin.com/57J3tLmc
```

![[Pasted image 20251102202406.png]]


**Explicação da Metodologia:**

- A URL foi obtida na análise do painel Trello no Lab 04.
    
- Acessamos o link, que levou a um _paste_ público intitulado "Leak businesscorp", datado de 6 de julho de 2021.
    
- Analisamos o conteúdo deste _paste_ em busca de credenciais ou outras informações sensíveis.
    

**Resultado Obtido:** O _paste_ continha um vazamento de credenciais de um e-mail corporativo:

```
1. camila@businesscorp.com.br
2. ca123456
```

As informações sensíveis encontradas foram:

- **Usuário:** `camila@businesscorp.com.br`
    
- **Senha:** `ca123456`


### LAB 06 - OSINT - Business

---

**ID do Lab:** `83ff4b5f8d2cb305c5a9b1f01b340e3131dd2ba4`

**Análise / Alvo:** `businesscorp.com.br`

**Pergunta:** Qual o nome do documento é possível encontrar via Google Hacking no `businesscorp.com.br`?

**Resposta:** Para encontrar documentos específicos indexados pelo Google, utilizamos uma técnica de Google Dork focada em extensões de arquivo. O objetivo é filtrar resultados que sejam arquivos de documento (como `.doc`, `.docx`, `.pdf`) que possam conter informações corporativas.

**Comando Utilizado (Google Dork):**

```
site:businesscorp.com.br .doc
```

![[Pasted image 20251102203039.png]]


**Explicação do Comando:**

- **`site:businesscorp.com.br`**: Restringe a pesquisa do Google apenas para páginas indexadas dentro deste domínio.
    
- **`.doc`**: Filtra os resultados para incluir páginas que contenham a string `.doc`, que o Google associa fortemente a arquivos do tipo "Microsoft Word Document". Alternativas como `ext:doc` ou `filetype:doc` teriam um efeito similar.
    

**Resultado Obtido:** O Google Dork (conforme a primeira imagem) revelou uma URL `http://www.businesscorp.com.br/ri/` com o título "Index of /ri".

Ao acessar esta URL (conforme a segunda imagem), foi confirmado que se tratava de um diretório com a opção de "Index of" (Listagem de Diretório) habilitada. Dentro deste diretório, foi encontrado o seguinte documento:

- **Nome do Documento:** `RI.doc`
-

### LAB 07 - OSINT - Business

---

**ID do Lab:** `66c68c619b7f8a14b4eb33258f319112fb7b5734`

**Análise / Alvo:** Metadados do arquivo `RI.doc` (encontrado no Lab 06).

**Pergunta:** Realizar uma pesquisa por metadados em documentos encontrados no domínio `businesscorp.com.br` e responder: Qual o nome do colaborador encontrado?

**Resposta:** Dando continuidade ao Lab 06, analisamos os metadados do arquivo `RI.doc` que foi baixado. Metadados são "dados sobre dados" que ficam embutidos em arquivos e podem vazar informações como autores, softwares, datas e, neste caso, nomes de colaboradores. Para esta tarefa, utilizamos a ferramenta `exiftool`.

**Comando Utilizado:**

Bash

```
exiftool RI.doc
```
![[Pasted image 20251102203746.png]]


**Explicação do Comando:**

- **`exiftool`**: É uma ferramenta de linha de comando padrão no Kali Linux, usada para ler, escrever e editar metadados de uma vasta gama de tipos de arquivo.
    
- **`RI.doc`**: O arquivo alvo que foi baixado para análise.
    

**Resultado Obtido:** A análise dos metadados com o `exiftool` (conforme a imagem) revelou diversas informações, incluindo:

- **`Author`**: `Rogerio Severovisk`
    
- **`Company`**: `Business Corp - businesscorp.com.br`
    
- **`Keywords`**: `rogerio@businesscorp.com.br | LinkedIn: https://www.linkedin.com/in/rogerio-severo`
    

O nome do colaborador encontrado nos metadados é **Rogerio Severovisk**.

### LAB 08 - OSINT - Business

---

**ID do Lab:** `c91a488330e650e2119d2ddffe5eb97f44e0f2b2`

**Análise / Alvo:** Perfil LinkedIn de `Rogerio Severovisk` (colaborador da `businesscorp.com.br`).

**Pergunta:** Realizar uma pesquisa pelo colaborador da `businesscorp.com.br` e obter a key para pontuar.

**Resposta:** Dando continuidade ao Lab 07, onde o nome "Rogerio Severovisk" e um link de LinkedIn foram descobertos nos metadados do arquivo `RI.doc`, esta etapa consistiu em analisar o perfil público desse colaborador. O objetivo é encontrar informações sensíveis ou a _key_ do desafio, que poderiam ser vazadas em posts públicos.

**Metodologia / URL Acessada:**

```
https://www.linkedin.com/in/rogerio-severovisk-businesscorp/
```
![[Pasted image 20251102204047.png]]


**Explicação da Metodologia:**

- A URL foi acessada com base nos dados (`Keywords`) encontrados na análise de metadados do Lab 07.
    
- Inspecionamos o perfil público do colaborador, com foco na seção "Activity" (Atividade), que lista os posts recentes feitos pelo usuário.
    

**Resultado Obtido:** A análise da seção "Activity" do perfil (conforme a imagem) revelou um post público feito por Rogerio Severovisk que continha a _key_ do desafio:

- **Texto do Post:** `Information Gathering KEY: 8812737123129912s`
    
- **KEY:** `8812737123129912s`
  


### LAB 09 - OSINT - Business

---

**ID do Lab:** `ff4b82f3d417ce162efa07c3c3a147dc54ad6d14`

**Análise / Alvo:** Posts do colaborador `Rogerio Severovisk` (LinkedIn).

**Pergunta:** De acordo com a vaga de emprego da `businesscorp.com.br`, qual possivelmente é o firewall utilizado na empresa?

**Resposta:** Dando continuidade à análise do perfil de `Rogerio Severovisk` (iniciada nos labs 07 e 08), foi identificado um segundo post público. Este post divulgava uma vaga de "Oportunidade - Tecnologia da Informação" na `businesscorp.com.br`. A descrição da vaga listava as tecnologias e competências desejadas, o que fornece informações valiosas sobre o _stack_ tecnológico interno da empresa.

**Metodologia / URL Acessada:**

- Análise de posts no perfil do colaborador.
    
- URL do Post: `pt.linkedin.com/posts/rogerio-severovisk-businesscorp...` (conforme imagem)
- ![[Pasted image 20251102204221.png]]
- 
    

**Explicação da Metodologia:**

- Ao investigar o perfil do colaborador (além do post da KEY do Lab 08), encontramos um post mais antigo (5 anos) sobre uma vaga de emprego.
    
- A leitura dos requisitos da vaga (Experiência com...) permite inferir quais são as ferramentas de infraestrutura utilizadas pela empresa, pois ela busca profissionais que já saibam operá-las.
    

**Resultado Obtido:** A descrição da vaga listava as seguintes tecnologias:

- Windows Server 2008 e Active Directory
    
- Servidores Linux
    
- Banco de dados mysql
    
- **Netgate-pfSense-Firewall**
    

O firewall possivelmente utilizado pela empresa é o **Netgate-pfSense**.
