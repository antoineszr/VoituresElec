import zeep

wsdl = 'https://mycv.glaivemedia.fr/?wsdl'
client = zeep.Client(wsdl)

result = client.service.tempsParcours("-0.6756162643432286", "45.8786949940647", "-0.34465312957759703", "46.015243021856286", "30")

print(result)