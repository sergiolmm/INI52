"""
Classe de funções uteis, com teste local dessas funções

"""
import re

def _read_header(response):
    if type(response) == bytes:
        return _read_header_sb(response)
    header = {}
    lines = response.split('\r\n')
    # retira a linha 0
    header_lines = lines[1:]
    for line in header_lines:        
        if len(line) > 0:
            m = re.match(r'(\S+?): (.*)', line)
            if m:
                key = m.group(1).upper()
                header[key] = m.group(2)
    return header                
            
def _read_header2(response):
    assert type(response) == str
    lines = response.split('\r\n')
    return { 
        k: v for [k, v] in (line.split(': ',1) for line in lines[1:] if ': ' in line) 
        }

def _read_header_sb(response):
    assert type(response) == bytes
    lines = response.split(b'\r\n')
    return { 
        k.decode(): ''.join(map(chr,v)) for [k, v] in (line.split(b': ',1) for line in lines[1:] if b': ' in line) 
        }


def teste(response):
    assert type(response) == bytes
    if type(response) != bytes:
      raise TypeError("Erro de tipo")
    #raise Exception("Levantei uma exceção")
    print("É binário")
    lines = response.split(b'\r\n')
    l = lines[1:]       
    print(l)
    p2 = []
    for line in l:
        if b': ' in line:
            p2.append(line)
    print(p2)
    resp = {} # dicionario   (chave e valor)
    for linha in p2:
        k,v = linha.split(b': ', 1)
        print(k, v)
        resp[k.decode()] = ''.join(map(chr, v))
    print(resp)
    # fazer a mesma coisa em 1 linha
    resp2 = { k.decode(): ''.join(map(chr,v)) for [k, v] in (line.split(b': ',1) for line in lines[1:] if b': ' in line) }
    print(resp2)
    resp3 = {'nome': 'Valor','nnn':'vvv'}
    for k in resp3:
        print(k)
        print(resp3[k])
 
    print(resp3)


  
# executa somente se for execução direta
# assim permite que possamos testar a função
# sem depender de que a chama.
if __name__ == "__main__":
    print("Nome : ",__name__)
    DISCOVER_TEMPLATE = b"""\
M-SEARCH * HTTP/1.1\r\n\
host: 239.255.255.250:1900\r\n\
man: "ssdp:discover"\r\n\
mx: 5\r\n\
st: ssdp:all\r\n\
\r\n\
"""
    try:
        header = _read_header_sb(DISCOVER_TEMPLATE)
        print(header)
    except AssertionError:
        print("peguei erro de Assert")
    except TypeError:
        print("Erro de tipo")            
    except:
        print("Geral..;")    
    finally:
        print("fim")    
    print("Novo metodo")
    print(_read_header(DISCOVER_TEMPLATE.decode()))
    print(_read_header2(DISCOVER_TEMPLATE.decode()))