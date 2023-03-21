# Criação de valores

Este repositório se trata de um trabalho para quando precisamos substituir valores 'nan' na base, valores ausentes, outliers etc

- parametros
- calculo_valores

## Parametros

Na função de "parametros" é realizado uma lógica à qual identifica outliers na série e, de acordo com a regra de aceitação passada, isto é, se for passado 30 no parâmetro, a função calculará os parâmetros de média, desvio padrão, máximo e mínimo daquela série, caso o número de outliers não ultrapasse 30% da base, caso contrário, ele retirará os outliers e calculará os parâmetros sem eles.

## Calculo_valores

Com os parâmetros da função anterior, calcula o valor com a formula (criada por mim) valor = media + (desvio_padrao * peso_aleatorio)) e verifica se esse valor é maior que o maior valor da série, ou menor que o menor valor da série, se for uma das 2 condições, ele refaz o calculo.

## Como usar

Para utilizar, basta chamar a funmção 'calculo_valores' passando como parâmetro o dataset, a porcentagem da base aceitável de outliers e a quantidade de valores que deseja criar!
