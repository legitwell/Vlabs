#!/usr/bin/env python3
# DesecParsing.py – parsing, AXFR e Subdomain Takeover
# Banner por LegiT

import re, sys, socket, urllib.request, ssl, urllib.error
from colorama import init, Fore, Style

# --- [Bibliotecas de DNS] ---
try:
    import dns.resolver
    import dns.query
    import dns.zone
    import dns.exception 
    from dns.rdatatype import RdataType
    from dns.rdataclass import RdataClass
except ImportError:
    print(Fore.RED + "Erro: Biblioteca 'dnspython' não encontrada.")
    print(Fore.YELLOW + "Execute: apt install python3-dnspython")
    sys.exit(1)
# -------------------------

init(autoreset=True)  

# Funções de Log
def log_info(msg):
    print(f"{Fore.CYAN}[i] {msg}{Style.RESET_ALL}")

def log_warn(msg):
    print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")
    
def log_vuln(msg):
    print(Fore.RED + Style.BRIGHT + f"  [!!!] {msg}" + Style.RESET_ALL)


# --- [CORREÇÃO 1: FINGERPRINTS EXPANDIDO] ---
# Dicionário muito mais completo de fingerprints de takeover
FINGERPRINTS = {
    "NoSuchBucket": "Amazon S3",
    "The specified bucket does not exist": "Amazon S3",
    "There isn't a GitHub Pages site here": "GitHub Pages",
    "no-such-app": "Heroku",
    "The gods are wise, but do not know of the site which you seek.": "Pantheon",
    "Whatever you were looking for doesn't currently exist at this address": "Surge.sh",
    "Sorry, this shop is currently unavailable.": "Shopify",
    "This domain is available for registration": "Vários (Expirado)",
    "Do you want to register": "WordPress.com", # <--- A CHAVE PARA O WORDPRESS
    "Unrecognized domain": "Kinsta",
    "is not a registered domain": "Vários (Expirado)",
    "page not found": "Vários (Genérico 404)",
    "404 Not Found": "Vários (Genérico 404)"
}
# ----------------------------------------------------

# --- Função para baixar HTML (Etapa 5) ---
def fetch_content(url):
    """ Tenta baixar o conteúdo de uma URL (HTTP e HTTPS). """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    # Tenta HTTPS primeiro
    try:
        req = urllib.request.Request(f"https://{url}", headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            return resp.read().decode(errors="ignore")
    except Exception:
        pass # Ignora falha de HTTPS

    # Tenta HTTP
    try:
        req = urllib.request.Request(f"http://{url}", headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            return resp.read().decode(errors="ignore")
    except Exception:
        return None # Retorna None se ambos falharem
# ----------------------------------------------------

DOM = sys.argv[1] if len(sys.argv) == 2 else None
if not DOM:
    print(Fore.RED + "Uso: {} <domínio>".format(sys.argv[0]))
    sys.exit(1)

URLS = [f"https://{DOM}", f"http://{DOM}"]

# --- [CORREÇÃO 2: hosts_totais agora é um DICIONÁRIO] ---
# Isso vai guardar o host E o tipo de registro (ex: 'A', 'CNAME')
hosts_totais = {} 

# Banner do LegiT
banner = f"""{Fore.RED}{Style.BRIGHT}

  _    ___   ___   ___   _____ 
 | |   | __| / __| |_ _| |_   _|
 | |__ | _|  | (_ |  | |    | |  
 |____||___| \\___| |___|    |_|  
                                
{Style.RESET_ALL}{Fore.YELLOW}     Script de Recon por LegiT{Style.RESET_ALL}
"""
print(banner)

# --- 1) Baixa HTML da página principal ---
print(Fore.YELLOW + Style.BRIGHT + f"\n[ETAPA 1] Baixando HTML de {DOM}...\n")
html = ""
for url in URLS:
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(url, context=ctx, timeout=10) as resp:
            html = resp.read().decode(errors="ignore")
        log_info(f"Sucesso ao baixar {url}")
        break 
    except urllib.error.URLError as e:
        log_warn(f"Falha ao tentar {url} (Erro: {e}). Tentando próxima URL...")
        continue

if not html:
    print(Fore.RED + "Erro: Não foi possível baixar a página (HTTPS e HTTP). Encerrando.")
    sys.exit(1)

# --- 2) Extrai hosts únicos do HTML ---
print(Fore.YELLOW + Style.BRIGHT + "\n[ETAPA 2] Extraindo Hosts do HTML...\n")
hosts_html = set()
pattern = re.compile(r'href=["\']?[^"\'>]*://([^/"\'>\s:]+)', re.I)
for m in pattern.finditer(html):
    host = m.group(1).lower() 
    if host.endswith(f".{DOM}") or host == DOM or re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        hosts_html.add(host)

if not hosts_html:
    log_warn("Nenhum host encontrado no HTML da página inicial.")
else:
    for h in sorted(hosts_html):
        print(Fore.GREEN + f"[+] Host encontrado (via HTML): {h}")
        # Adiciona à lista mestre, marcando o tipo como 'HTML' (desconhecido)
        if h not in hosts_totais:
            hosts_totais[h] = 'HTML'

# --- 3) Resolve DNS dos hosts (do HTML) ---
print(Fore.YELLOW + Style.BRIGHT + "\n[ETAPA 3] Resolvendo DNS (via HTML Parsing)...\n")
if not hosts_html:
    log_warn("Nenhum host para resolver.")
else:
    for h in sorted(hosts_html):
        try:
            ip = socket.gethostbyname(h.split(":")[0])
            print(f"{Fore.CYAN}{h:<30} {Fore.WHITE}tem o IP {Fore.MAGENTA}{ip}")
        except socket.gaierror:
            print(f"{Fore.CYAN}{h:<30} {Fore.RED}não pôde ser resolvido")
        except Exception as e:
            pass 

# --- 4) Tentativa de Transferência de Zona (AXFR) ---
print(Fore.YELLOW + Style.BRIGHT + f"\n[ETAPA 4] Tentando Transferência de Zona (AXFR) em {DOM}...\n")
try:
    ns_records = dns.resolver.resolve(DOM, 'NS')
    nameservers = [str(ns.target) for ns in ns_records]
    
    if not nameservers:
        print(Fore.RED + "Nenhum Name Server (NS) encontrado.")
    else:
        print(f"{Fore.CYAN}[i] Name Servers encontrados: {', '.join(nameservers)}\n")
        transfer_sucesso = False
        for ns in nameservers:
            try:
                ns_ip = socket.gethostbyname(ns)
                print(f"{Fore.WHITE}Resolvido: {ns} -> {ns_ip}")
                print(f"{Fore.WHITE}Tentando AXFR em {ns} ({ns_ip})...")
            except socket.gaierror:
                print(f"{Fore.RED}[-] Falha: Não foi possível resolver o IP do nameserver {ns}\n")
                continue 

            try:
                z = dns.zone.from_xfr(dns.query.xfr(ns_ip, DOM, timeout=15))
                
                print(Fore.GREEN + Style.BRIGHT + f"\n[!!!] SUCESSO! Transferência de Zona obtida de {ns}\n")
                transfer_sucesso = True
                
                for (name, node) in z.items():
                    for rdataset in node.rdatasets:
                        # --- [CORREÇÃO 2: Armazena o TIPO do registro] ---
                        record_type = RdataType.to_text(rdataset.rdtype)
                        host_completo = f"{name.to_text()}.{DOM}"
                        if name.to_text() == '@':
                            host_completo = f"{DOM}"
                        
                        # Adiciona o host E seu tipo ao dicionário mestre
                        hosts_totais[host_completo] = record_type
                        
                        for record in rdataset:
                            print(f"{Fore.GREEN}{host_completo:<30} "
                                  f"{Fore.WHITE}{rdataset.ttl:<8} "
                                  f"{Fore.WHITE}{RdataClass.to_text(rdataset.rdclass):<4} "
                                  f"{Fore.WHITE}{record_type:<5} "
                                  f"{Fore.CYAN}{record.to_text()}")
                print("\n") 

            except (dns.query.TransferError, dns.exception.Timeout, Exception) as e:
                print(f"{Fore.RED}[-] Falha na Transferência: {repr(e)}\n")

        if not transfer_sucesso:
            print(Fore.YELLOW + "[!] Nenhum Name Server permitiu a Transferência de Zona (AXFR).")

except (dns.resolver.NoNameservers, dns.resolver.NXDOMAIN, Exception) as e:
    print(Fore.RED + f"Erro na Etapa 4: {repr(e)}")


# --- [ETAPA 5 - CORREÇÃO 2: Checagem "Inteligente"] ---
print(Fore.YELLOW + Style.BRIGHT + f"\n[ETAPA 5] Checando Subdomain Takeover em {len(hosts_totais)} hosts totais...\n")

if not hosts_totais:
    log_warn("Nenhum host total encontrado para checar.")
else:
    vulneraveis = 0
    # Itera pelo dicionário (host, tipo)
    for host, record_type in sorted(hosts_totais.items()):
        
        # Ignora IPs puros que podem ter sido encontrados
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
            continue
            
        # --- Lógica "Inteligente": Só testa CNAMEs ou hosts do HTML ---
        if record_type not in ['CNAME', 'HTML']:
            continue
            
        print(f"{Fore.WHITE}Testando [ {record_type} ]: {host}")
        
        content = fetch_content(host)
        
        if content:
            # Compara o HTML com nossas fingerprints
            for fingerprint, service in FINGERPRINTS.items():
                if fingerprint.lower() in content.lower(): # Checa case-insensitive
                    log_vuln(f"VULNERÁVEL: {host} (Serviço: {service})")
                    log_vuln(f"      -> Fingerprint: \"{fingerprint}\"")
                    vulneraveis += 1
                    break # Para de procurar fingerprints neste host
                    
    if vulneraveis == 0:
        print(Fore.GREEN + "\n[i] Nenhum host parece vulnerável a Subdomain Takeover (baseado nas fingerprints atuais).")
    else:
        print(Fore.RED + Style.BRIGHT + f"\n[!!!] {vulneraveis} host(s) potencialmente vulneráveis encontrados!")


print(Fore.YELLOW + Style.BRIGHT + "\n[FIM] Script de Recon Concluído.\n")
