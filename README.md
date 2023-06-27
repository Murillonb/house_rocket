# HOUSE ROCKET

----
<img src='img/house_rocket.png'>
A empresa e as perguntas de negócio deste projeto são fictícias.

----
## 1.0. Descrição

A House Rocket é uma plataforma de compra e venda de imóveis.<br>
Basicamente eles realizam uma pesquisa de mercado para comprar, reformar e revender os imóveis.<br>
O CEO da empresa gostaria de maximizar o lucro através de bons negócios. Encontrando imóveis baratos para comprá-los e depois revendê-los com o maior lucro possível. <br>
Com isso, tendo como desafio identificar esses imóveis, ele solicitou ao time de Data Science que fizessem um estudo com todos os imóveis disponíveis no banco de dados da empresa.

## 2.0. Questões do negócio

1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
2. Uma vez que o imóvel seja comprado, qual o melhor momento para vendê-lo e por qual preço?

## 3.0. Premissas

Premissas adotadas para execução deste projeto:

* O valor da área útil quadrada foi considerada a melhor medida de preço dos imóveis;
* Imóveis repetidos foram removidos deixando o último cadastro apenas, para evitar que a análise seja enviesada;
* Imóveis com 0 (zero) banheiro ou quarto foram considerados um erro e por isso foram removidos;
* O imóvel com 33 (trinta e três) quartos foi considerado um erro de digitação e alterado para 3 (três);
* A localização e a condição do imóvel foram consideradas fundamentais na determinação do preço de compra dos imóvel;
* A localização e a estação do ano foram consideradas fundamentais na determinação do preço de venda dos imóveis.

## 4.0. Planejamento da Solução

### 4.1. Produto Final

a) Dois relatórios:
* Relatório com as sugestões de compra de apartamento com um valor recomendado;
* Relatório com as sugestões de venda de um imóvel por um valor recomendado.

b) Dashboard (<a href="https://mnb-house-rocket.streamlit.app/">link</a>).

### 4.2. Ferramentas
* Python 3.10.1
* Streamlit Cloud
* VS Code
* Google Colab

### 4.3. Processo
#### 4.3.1. Estratégia da solução

Passo 01 - Descrição dos dados: ganho de conhecimento sobre os dados que serão utilizados;<br>
Passo 02 - Feature Engineering: criação de novas features para melhor entendimento do negócio;<br>
Passo 03 - Filtragem das variáveis: remoção de linhas e colunas que não contribuem com o fenômeno estudado;<br>
Passo 04 - Análise Exploratória dos Dados (EDA): verificação de hipóteses e das correlações entre as features;<br>
Passo 05 - Responder problemas de negócio: responder as questões de negócio;<br>
Passo 06 - Resultados para o negócio: resultados finais encontrados.

#### 4.3.2. Detalhamento da solução

**1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?**
		
* Calcular os preços da área quadrada de cada imóvel;
* Agrupar os imóveis por região;
* Encontrar a mediana dos preços da área quadrada para cada região;
* Comparar os preços da área quadrada de cada imóvel com a mediana da região;
* Quando o preço da área quadrada do imóvel for menor do que a mediana da região e a condição for classificada como 4 ou 5, indicamos o imóvel para ‘Compra’.

**2. Uma vez que o imóvel seja comprado, qual o melhor momento para vendê-lo e por qual preço?**

* Calcular os preços da área quadrada de cada imóvel;
* Agrupar os imóveis por região e por estação do ano;
* Encontrar a mediana dos preços da área quadrada para cada região por estação;
* Comparar os preços da área quadrada de cada imóvel com a mediana encontrada;
* Quando o preço da área quadrada do imóvel for menor do que a mediana, sugerimos o valor de venda do imóvel como valor de compra + 30%, caso contrário como valor de compra + 10%.

## 5.0. Top Insights

**01. Imóveis que possuem vista para água são mais caros na média.**<br>
**Verdadeiro**. Verificamos que a área quadrada de imóveis com vista para o mar são 93.74% mais caros na média.

**02. O valor do imóvel variam mais de 40% dependendo do zipcode.**<br>
**Verdadeiro**. A diferença entre os preços médios por área quadrada do zipcode mais barato com o mais caro chega a 281.47%.

**03. Imóveis com condições muito boas (5) podem valer mais de 50%, na média, do que os com condição média (3).**<br>
**Falso**. Verificamos uma diferença de apenas 16.34% no valor médio da área quadrada, quando comparados imóveis em condições muito boas ($ 298,98/sqft) e imóveis em boas condições ($ 257.41/sqft).<br>
Algo que nos chama a atenção é o fato do valor médio da área quadrada de imóveis em condições ruins serem maiores do que de imóveis em boas condições. Seria interessante analisar o motivo dessa diferença. Talvez começando pela localização dos imóveis.

**04. Imóveis com alguma vista são 30% mais caros, na média, do que os imóveis sem vista.**<br>
**Falso**. A diferença de preço médio entre imóveis sem vista ($ 256.86/sqft) e o menor preço médio dos imóveis com alguma vista ($ 304.26/sqft) é de 18.45%.<br>
Podemos verificar também que a diferença entre a vista 4 e 3 é de 34.84%. O que mostra ser uma variação bastante significativa. Podendo ser levantando mais detalhes sobre o que motiva um imóvel ter sua avaliação de view = 4.


## 6.0. Resultados para o negócio

Com as premissas que foram adotadas ao início do projeto, foi possível listar 743 imóveis como passíveis de compra. Com o valor de revenda menor do que a mediana dos valores dos imóveis da região, levando em conta também a estação do ano, o lucro desses imóveis foi calculado com 30% do valor de compra, porém por estarem abaixo do valor da mediana calculada ainda seria possível aumentar essa margem.<br>
Com esses 743 imóveis a estimativa de lucro é de $ 102.839.213,40.

## 7.0. Conclusão

O objetivo do projeto foi alcançado, sendo indicados os melhores imóveis para compra e calculados os valores de venda caso os imóveis sejam adquiridos, conforme premissas adotadas.<br>
Foi construído também um Dashboard com o Streamlit (<a href="https://mnb-house-rocket.streamlit.app/">link</a>), o qual pode ser acessado clicando aqui. Esse dashboard tem a intenção de auxiliar na tomada de decisões de negócio, disponibilizando ao final do mesmo os imóveis e suas classificações como ‘Compra’ ou ‘Não Compra’.

## 8.0. Próximos passos

Implementar novas tabelas e gráficos no dashboard para auxiliar ainda mais o time de negócio na tomada de decisão.<br>
Verificar quanto de lucro teríamos se reformássemos os imóveis antigos.<br>
Realizar o estudo para prevermos qual seria a valorização dos imóveis nos próximos meses para podermos adquirir novos imóveis e revendê-los com maior lucro.

----
**Fontes:**<br>
Imagem do Pexels (<a href="https://www.pexels.com/pt-br/foto/arquitetura-predios-edificios-cidade-13898912/">link</a>)<br>
Dados do Kaggle (<a href="https://www.kaggle.com/datasets/harlfoxem/housesalesprediction">link</a>)
