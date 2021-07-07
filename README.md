# IIC2173 - Entrega 2 - Grupo 1

Los docs (diagramas y documentación api) están en Docs/E2.pdf. 

Backend corriendo en https://www.iluovobackend.ml/
Frontend corriendo en https://www.iluovo.ml/


# Documentación Encriptación

Para la encriptación se utilizó Django Fernet. Según recomendaciones del curso, se utilizó una arquitectura Frontend -> Servidor -> Encriptación: cuando un usuario envía un mensaje a través del frontend, este llega a través de websockets WSS al backend, quien encripta de inmediato los contenidos del mensaje de ser éste privado utilizando F.encrypt según una llave de encriptación creada para este propósito. El mensaje original se envía sin encriptación solo a los miembros autorizados e ingresados en la room privada que corresponde. 

# Documentación CI / CD

## Continuous Integration

* Se creo un workflow con Github Actions
  * ``.github/workflows/django.yml``
  * Se activa al hacer push y pull requests en ``master`` y ``development``
  * Se instalan los requerimientos
  * Se extraen las variables de entorno de la sección ``env`` utilizando Github Secrets
  * Se corren 4 tests (para ello, se genera una base de datos de prueba)
  * Luego se destruye la base de datos de prueba

## Continuous Deployment
* Con el mismo workflow de Github Actions:
  * Sólo si se pasan todos los tests en la sección de CI
  * Además sólo si se trata de la rama master (el resto solo tests), usando ``github.ref``
    * Se instala AWS CLI 2
    * Se configuran las credenciales de AWS con Github Secrets
    * Se carga la aplicación a un bucket S3
    * Se gatilla el Deploy utilizando CodeDeploy
* Se utilizó una AMI:
  * con CodeDeployAgent instalado
  * con el archivo ``.env`` en la ruta correspondiente
* CodeDeploy:
  * Application integrada con el Auto Scalling Group y Load Balancer
  * Integrada con S3 Bucket
  * Todo autorizado con un Rol que da acceso a todo lo necesario




# IIC2173 - Entrega 1 - Grupo 1



## Consideraciones generales

Para acceder al servidor en el cual se encuentra montada la aplicación y del cual se sacan las imagenes (AMI) para el Auto Scaling Group, se debe acceder mediante:  

ssh -i "iluovo_key.pem" ubuntu@ec2-3-95-109-129.compute-1.amazonaws.com

Para acceder a la aplicación de chat, se debe acceder a:
newchat.iluovo.com

Como se detalla más abajo, para hacer uso de la aplicación, se debe acceder mediante HTTP.

Las documentaciones se encuentran el final de este README.


## Requisitos
A continuación se indica el detalle de los requisitos implementadas, medios implementados y no implementados.

---

## Parte mínima

### Sección mínima (50%) (30p)

#### **Backend**
* **RF1: (3p)** **:heavy_check_mark: Logrado.** 
  Se debe poder enviar mensajes y se debe registrar su timestamp. Estos mensajes deben aparecer en otro usuario, ya sea en tiempo real o refrescando la página. **El no cumplir este requisito completamente limita la nota a 3.9**
  

* **RF2: (5p)** **:heavy_check_mark: Logrado** 
    Se deben exponer endpoints HTTP que realicen el procesamiento y cómputo del chat para permitir desacoplar la aplicación. **El no cumplir este requisito completamente limita la nota a 3.9**  
    Para probar esto, se puede acceder directamente a la API desde:  
    http://3.95.109.129:8000/

* **RF3: (7p)** **:heavy_minus_sign: Medio Logrado** 

   Esta implemenado el AutoScalingGroup con una AMI de una instancia en la cual trabajamos. Este cuenta con un ElasticLoadBalancer que balancea los requests entre las instancias que contiene el ASG. Se dejó como minimo 3 instancias en el ASG.
    * **(4p)** **:heavy_check_mark: Logrado** 
    Debe estar implementado el Load Balancer
    * **(3p)** **:x: No Logrado** 
  Se debe añadir al header del request información sobre cuál instancia fue utilizada para manejar el request. Se debe señalar en el Readme cuál fue el header agregado.  
* **RF4: (2p)** **:heavy_check_mark: Logrado**
   El servidor debe tener un nombre de dominio de primer nivel (tech, me, tk, ml, ga, com, cl, etc).

* **RF4: (3p)** **:heavy_minus_sign: Medio Logrado**  

  El dominio se encuentra asegurado con SSL. Sin embargo, si se accede a la aplicación mediante HTTPS, está no logra conectarse con el backend ya que este no cuenta con HTTPS, y por lo tanto no se puede acceder a las salas de chat. Por esta misma razon, no dejamos que se redirijiera de HTTP a HTTPS.
    * **(2p)** Debe tener SSL. 
    * **(1p)** Debe redirigir HTTP a HTTPS.

#### **Frontend**
* **RF5: (3p)** **:heavy_check_mark: Logrado** 
  Utilizar un CDN para exponer los *assets* de su frontend. (ej. archivos estáticos, el mismo *frontend*, etc.). Para esto recomendamos fuertemente usar cloudfront en combinacion con S3.
* **RF6: (7p)** **:heavy_check_mark: Logrado** 
  Realizar una aplicación para el *frontend* que permita ejecutar llamados a los endpoints HTTP del *backend*.
    * **(3p)** Debe hacer llamados al servidor correctamente.
    * Elegir **$1$** de los siguientes. No debe ser una aplicación compleja en diseño. No pueden usar una aplicacion que haga rendering via template de los sitios web. Debe ser una app que funcione via endpoints REST
        * **(4p)** Hacer una aplicación móvil (ej. Flutter, ReactNative)
        * **(4p)** Hacer una aplicación web (ej. ReactJS, Vue, Svelte)

---

## Sección variable

Deben completar al menos 2 de los 3 requisitos

### Caché (25%) (15p) **:heavy_minus_sign: Medio Implementado**
Para esta sección variable la idea es implementar una capa de Caché para almacenar información y reducir la carga en el sistema. Para almacenar información para la aplicación recomendamos el uso de **Redis**, así como recomendamos Memcached para fragmentos de HTML o respuestas de cara al cliente. 

En esta sección, se implementó la infraestructura de caché en AWS ElastiCache pero no se conectó con la apliación. En la sección de documentación se indica en datalle la implementación hecha.

* **RF1: (4p)** **:heavy_minus_sign: Medio Logrado** 
  Levantar la infraestructura necesaria de caché. Se puede montar en otra máquina o usando el servicios administrado por AWS. Se debe indicar como funciona en local y en producción. 
* **RF2: (6p)** **:x: No Logrado** 
  Utilizar la herramienta seleccionada de caché para almacenar las información para al menos 2 casos de uso. Por ejemplo las salas y sus últimos mensajes o credenciales de acceso (login). 
    * **Restricción** Por cada caso de uso debe utilizar alguna configuración distinta (reglas de entrada FIFO/LIFO, estructura de datos o bien el uso de reglas de expiración)
* **RF3: (5p)** **:heavy_minus_sign: Medio Logrado** 
  Documentar y explicar la selección de la tecnología y su implementación en el sistema. Responder a preguntas como: "¿por qué se usó el FIFO/LRU o almacenar un hash/list/array?" para cada caso de uso implementado. 


### Trabajo delegado (25%) (15p) **:x: No implementado**
Para esta sección de delegación de trabajo recomendamos el uso de "Functions as a Service" como el servicio administrado de AWS, _Lambda Functions_, o bien el uso de más herramientas como AWS SQS y AWS SNS. 

Se pide implementar al menos **3 casos de uso con distinto tipo de integración**.


1.- Mediante una llamada web (AWS API Gateway)
2.- Mediante código incluyendo la librería (sdk)
3.- Como evento a partir de una regla del AutoScalingGroup
4.- Mediante Eventbridge para eventos externos (NewRelic, Auth0 u otro)
5.- Cuando se esté haciendo un despliegue mediante CodeCommit 
6.- Cuando se cree/modifique un documento a S3

Alternativamente pueden integrar más servicios para realizar tareas más lentas de la siguiente forma: 
1.- Al crear un mensaje se registra en una cola (SQS) que llama a una función en lambda (directamente o a través de SNS)
2.- En Lambda se analiza ciertos criterios (si es positivo o negativo, si tiene "garabatos" o palabras prohibidas en el chat) y con este resultado se "taggea" el comentario. 
Si se crean en "tópics" distintos se consideran como 2 casos de uso (por el uso de distintas herramientas). 

Seguir el siguiente tutorial cuenta como 3 (https://read.acloud.guru/perform-sentiment-analysis-with-amazon-comprehend-triggered-by-aws-lambda-7363db23651f o https://medium.com/@manojf/sentiment-analysis-with-aws-comprehend-ai-ml-series-454c80a6114). No es necesaro que entiendan a cabalidad como funciona el código de estas funciones, pero sí que comprendan el flujo de la información y cómo es que se ejecuta.

Se deben documentar las decisiones tomadas. 

* **RF: (5p)** Por cada uno de los 3 tipos de integración.
    * **(3p)** Por la implementación.
    * **(2p)** Por la documentación.

### Mensajes en tiempo real (25%) (15p) **:heavy_check_mark: Implementado** 
El objetivo de esta sección es implementar la capacidad de enviar actualizaciones hacia otros servicios. Servicios recomendados a utilizar: SNS, Sockets (front), AWS Pinpoint entre otras. 

* **RF1: (5p)** **:heavy_check_mark: Logrado**  
  Cuando se escriben mensajes en un chat/sala que el usuario está viendo, se debe reflejar dicha acción sin que éste deba refrescar su aplicación. 
* **RF2: (5p)** **:heavy_check_mark: Logrado** 
  Independientemente si el usuario está conectado o no, si es nombrado con @ o # se le debe enviar una notificación (al menos crear un servicio que diga que lo hace, servicio que imprime "se está enviando un correo")
* **RF3: (5p)** **:heavy_check_mark: Logrado** 
  Debe documentar los mecanismos utilizados para cada uno de los puntos anteriores indicando sus limitaciones/restricciones. 


## Documentación

**Cache:**
En cuanto al caché, se implementó del lado de aws un cluster con redis en AWS ElastiCache. Para que las instancias de EC2 puedan acceder al cluster para almacenar y obtener información, se debe habilitar el puerto 6379 en sus security groups. Con esto configurado y con la dirección de endpoint del cluster que se obtiene de la consola, ya se pueden ejecutar comandos de redis para utilizar caché.

**Mensajes en tiempo real:**

Para el funcionamiento de los mensajes en tiempo real se usaron websockets, el frontend se conecta al backend a través de un websocket, los cuales se usan en backend con django channels. Al recibir un mensaje en backend se postea hacia la base de datos y luego se hace un group send para enviar el mensaje a todos los sockets que están conectados a la pieza desde donde se envió el mensaje original. 
En el caso de la API, al hacer POST via http también se le envía el mensaje creado a todos los usuarios  que estén conectados a la habitación del mensaje. Esto se logró creando un cliente temporal que se conecta a la habitación señalada con websockets para hacer el group send y desconectarse.
Luego para cuando un mensaje viene con un @ se revisa el string siguiente y se hace un get a la base de datos por un User que tenga el username, siendo este el string que viene después del @ antes de un espacio. Si este usuario existe se le envía una notificación y se avisa al chat que ese usuario está siendo notificado.

**Elastic Load Balancer:**

Se generó un Application Load Balancer, y un Target Group, que luego se enlazó un Auto Scaling Group, con su respectivo Launch Template.
Para facilitar el desarrollo y testeo, se fue utilizando el mismo template, pero generando nuevas versiones de este, con una nueva imagen incorporando los cambios deseados.
Se creó un Scaling Policies, que inicia una nueva instancia si se llega al 70% del procesamiento.


