# Introducción

En Ciencias de la Computación, la compresión de datos permite codificar un set de datos mediante diferentes algoritmos para almacenarlos usando menos espacio. Esta compresión se basa, a grandes rasgos, en buscar patrones o datos repetidos para luego poder hacer referencia a esas repeticiones sin la necesidad de volver a almacenarlas completamente en cada aparición.

Siendo entonces los conceptos principales la redundancia y la entropía, los algoritmos de compresión no solo son útiles para ocupar menos espacio de almacenamiento, sino también para obtener una idea de cómo están formadas estas cadenas. Dada una cadena, si al comprimirla obtenemos una cadena mucho menor, podemos suponer que su redundancia es alta, mientras que si al comprimirla su espacio no se redujo, toda información es relevante y poco es lo que se puede reemplazar.

# Problema

El problema a resolver es que dado un conjunto de receptores de células T (cada célular formada por una cadena _alpha_ y una _beta_), queremos poder predecir con qué grupo de pMHC interactúan. Es un problema de clusterización de machine learning. Sin embargo, para poder utilizar algún método como _k-means clustering_, es necesario saber de antemano cuántos grupos distintos estamos esperando.

Ahí es donde entra en juego la compresión de datos que nos puede dar un estimado de cuántos grupos distintos tenemos en nuestro set de datos. 

# compresión de Datos para Estimación de Grupos

La idea de la estimación está dada de la siguiente forma. Dado un set de receptores de células T (un listado de elementos de la forma <_alpha_,_beta_>), concaternarlos a todos y aplicar una función de compresión. La longitud de la cadena comprimida debería tener alguna correlación con la cantidad de grupos que hay en dicho set, ya que consideramos que si los elementos pertenecen al mismo grupo, su estructura será similar y por lo tanto, el algoritmo de compresión los _achicaría_.

## Algoritmo de compresión

Para comprimir las cadenas, usamos _zlib_, la librería por defecto para este tipo de tareas en _Python_. El algoritmo que utiliza _zlib_ para comprimir es una variante del algoritmo _LZ77_ llamado _deflate_. El algoritmo de _deflate_ es una combinación del algoritmo _LZ77_ junto a la Codificación de Huffman.

### Codificación de Huffman

La codificación de Huffman consiste en la construcción de un árbol binario que, basado en la frecuencia de aparición de cada símbolo del lenguaje (en este caso letras), le asignará una código de codificación, en donde los símbolos con mayor ocurrencia tendrán una longitud más corta mientras los de menor ocurra una longitud más larga. Para saber qué código corresponde a cada símbolo, basta con atravesar el árbol hasta llegar a la hoja de dicho símbolo e ir construyendo el código con las etiquetas de cada nodo atravesado.

### LZ77

LZ77 consiste en buscar segmentos de datos repetidos. Para eso, utiliza la técnica de ventana deslizante, en el sentido que el algoritmo va avanzando en la cadena de datos, y para cada posición, tiene memoria de qué caracteres estaban presente antes (hasta cierto límite). Cuando encuentra una cadena de caracteres próxima que se encuentra dentro de la ventana deslizante, esta cadena es reemplazada por dos números: la distancia hacia atrás donde comienza esta cadena, y la longitud de la misma. 

El algoritmo es lo suficientemente complejo como para detectar subcadenas que se repiten y siempre tomar la de longitud más larga.

### Combinación

_zlib_ combina la codificación de Huffman y _LZ77_, codificando primero la cadena de datos con _LZ77_ y luego convirtiendo todo a los árboles basados en frecuencia con el algoritmo de Huffman. Sin embargo, introduce una mejora. Los árboles utilizados son parte de la propia especificación de _zlib_, por lo que no se necesita espacio extra adicional para guardar información de la estructura de estos árboles.

