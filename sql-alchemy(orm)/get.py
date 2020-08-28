import requests

def main():
#    res = requests.get("https://google.es/")
#   print(res.text)
    res = requests.get("http://data.fixer.io/api/latest?access_key=76a823a36290510d766e776633ea8280&base?EUR&symbols=GBP&format=1")
    if res.status_code != 200:
        raise Exception("Error: Hubo un problema con la petición")
    datos = res.json()
    cambio = datos["rates"]["GBP"]
    print(f"1 EUR es igual a {cambio} GBP")
if __name__ =="__main__":
    main()