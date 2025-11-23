
### LAB 01 - Arquivo Suspeito (Análise de Integridade)

---

**ID do Lab:** `2d0ca0338671c349fc7ef8466b8f22b589c8756c`

**Pergunta:** Qual o nome do arquivo do suposto malware?

**Resposta:** O suposto malware é o arquivo que tem o hash MD5 divergente (único) em relação a todos os outros arquivos da amostra. Utilizamos o comando `md5sum` combinado com `sort`, `uniq -c` e `grep -v` para isolar a anomalia.

**Comando Utilizado:**

```
md5sum * | sort | uniq -c | grep -v '92'
```

**Explicação do Comando:**

- **`md5sum *`**: Calcula o hash MD5 de todos os arquivos.
    
- **`sort | uniq -c`**: Agrupa e conta hashes idênticos.
    
- **`grep -v '92'`**: Exclui (inverte a busca) todas as linhas que contêm o hash majoritário (`...92`), deixando apenas o hash único.
    

**Resultado Obtido:** O arquivo com a contagem de `1` e o hash exclusivo é:

- **Nome do Arquivo Suspeito:** `CleanZoomHost38.exe`
    

### Evidência (Print do Resultado)

![](../assets/Pasted%20image%2020251118021541.png)

### LAB 02 - Hash do Arquivo Verdadeiro

---

**ID do Lab:** `3f9574657d50564a04141146805aef66b923a7ce`

**Pergunta:** Qual o hash md5 do arquivo verdadeiro?

**Resposta:** O hash do arquivo "verdadeiro" é o hash majoritário, compartilhado por quase todos os arquivos na amostra (49 cópias), indicando a versão original não modificada.

**Comando Utilizado (Implícito no Lab 01):**


```
md5sum CleanZoom.exe
```

**Resultado Obtido:** O hash que aparece em 49 instâncias é:

- **Hash MD5 Verdadeiro:** `37ecb62f912e85ac16faf220a3d09292`
    
### Evidência (Print do Resultado)

![](../assets/Pasted%20image%2020251118021621.png)


### LAB 03 - Hash do Arquivo Suspeito

---

**ID do Lab:** `06a2282dee4b129309e936d86eba4f979d11c046`

**Pergunta:** Qual o hash md5 do arquivo suspeito?

**Resposta:** O hash do arquivo suspeito é o valor único encontrado apenas na anomalia `CleanZoomHost38.exe`.

**Comando Utilizado (Implícito no Lab 01):**

Bash

```
md5sum CleanZoomHost38.exe
```

**Resultado Obtido:** O hash encontrado apenas uma vez é:

- **Hash MD5 Suspeito:** `6bc664de142144d81576fe4788d60327`
    

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251118021721.png)


### LAB 04 - Hash SHA-512

---

**ID do Lab:** `8ea65f3c8b9439b2ff70519abdb73469eb325cfa`

**Pergunta:** Qual o hash sha512 da palavra `keeplearning`?

**Resposta:** Utilizamos o comando `echo -n` para evitar que a quebra de linha (`\n`) seja incluída na string antes de passar para o `sha512sum`.

**Comando Utilizado:**

Bash

```
echo -n "keeplearning" | sha512sum
```

**Explicação do Comando:**

- **`echo -n "..."`**: Imprime a string sem o caractere de nova linha.
    
- **`| sha512sum`**: Pipe (envia) a string para o programa que calcula o hash SHA-512.
    

**Resultado Obtido:**

- **Hash SHA-512:** `1d2da0cc838de8996cc71dc72bdbbe03d347b573cb3a4ab46c9e68987832f6bfe192579ab7604cdea76347828b3a0382602401e3417cc8a53e87da7565da4766`
    

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251118021755.png)


### LAB 05 - Hash (passwd) + Base64

---

**ID do Lab:** `4fe73c50da0bb9a565542ff267e6837340c1f715`

**Pergunta:** Gere o hash (passwd) sha256 com o salt definido como "desec" e senha "1337" e informe o resultado encodado em base64.

**Resposta:** Primeiro, geramos o hash com `openssl passwd` e depois usamos `echo -n` com pipe para encodá-lo em Base64. O `sha256` usa o identificador `$5$`.

**Comando Utilizado:**

Bash

```
# Geração do hash ($5$desec$KcaDk1xKzoNseKHrUDCMB.3jpw80sSTQrW1ltnzFiy0)
openssl passwd -5 -salt desec 1337

# Encodificação em Base64:
echo -n '$$desec$KcaDk1xKzoNseKHrUDCMB.3jpw80sSTQrW1ltnzFiy0' | base64
```

**Explicação do Comando:**

- **`openssl passwd -5 -salt desec 1337`**: Gera um hash usando SHA-256 (`-5`), com salt `desec` e senha `1337`.
    
- **`echo -n '...' | base64`**: Envia o hash gerado (incluindo o `$`) para o `base64`.
    

**Resultado Obtido:**

- **Hash (Base64):** `JDUkZGVzZWMkS2NhRGsxeEt6b05zZUtIclVEQ01CLjNqcHc4MHNzVFFydzFMdG56Rml5MA==`
    

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251118021915.png)

### LAB 06 - Quebra Simples

---

**ID do Lab:** `48a049e6aaabd7471fbb1fd00fe8f3a88c17c5b6`

**Pergunta:** Descubra qual a senha do seguinte hash: `7084668f3a53d5545a823399ed561b3d`

**Resposta:** O hash tem 32 caracteres, indicando ser **MD5**. Usamos um serviço de quebra online (como o Hashes.com, citado na evidência) para quebrar o hash, pois MD5 sem salt é facilmente encontrado em Rainbow Tables.

**Comando Utilizado (Para Referência - Não obrigatório):**


```
 Encontrar o tipo (MD5)
hash-identifier 7084668f3a53d5545a823399ed561b3d
```

**Resultado Obtido:**

- **Senha Descoberta:** `_power11`

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251118021944.png)


### LAB 07 - Quebra com Múltiplos Hashes

---

**ID do Lab:** `2a90888ad0b436693738646821d351384a596a6d`

**Pergunta:** Descubra a senha do hash `806825f0827b628e81620f0d83922fb2c52c7136`, que é gerado por **MD5 -> Base64 -> SHA1**.

**Resposta:** É necessário criar um script em Bash que simule o algoritmo de hashing complexo (MD5 da senha, Base64 do MD5, e SHA1 do Base64) para cada senha em uma wordlist e compare o resultado com o hash alvo.

**Comando Utilizado (Script):**


```
./HasheScript.sh
```

**Código do Script (`HasheScript.sh`):**


```
#!/bin/bash

# Define a wordlist (dica do lab) e o hash alvo
wordlist="/usr/share/john/password.lst"
hash="806825f0827b628e81620f0d83922fb2c52c7136"

# Loop para ler cada linha (senha) da wordlist
while read senha; do
    # Gera o hashx aplicando o algoritmo de 3 passos:
    # 1. echo -n "$senha" | md5sum | head -c 32  (MD5 da senha)
    # 2. base64 -w 0 (Base64 do MD5)
    # 3. sha1sum | head -c 40 (SHA1 do Base64)
    hashx=$(echo -n "$senha" | md5sum | head -c 32 | base64 -w 0 | sha1sum | head -c 40)
    
    # Compara o hash gerado (hashx) com o hash alvo
    if [ "$hash" = "$hashx" ]; then
        echo "Hash encontrado ====> $hashx"
        echo "Senha encontrada ====> $senha"
        exit 0
    fi
done < $wordlist

exit 1
```

**Resultado Obtido:** O script encontra a correspondência após testar várias senhas:

- **Senha Descoberta:** `help123`

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251118022044.png)
![](../assets/Pasted%20image%2020251118022052.png)