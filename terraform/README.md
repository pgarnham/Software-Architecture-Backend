# IaaC con Terraform

Para aplicar ``IaaC`` a iluovo se utilizó [Terraform](https://www.terraform.io/ "Link a Terraform"), quien provee un formato y una manera de conectar a ``AWS`` y crear allí la infraestructura especificada de manera automática.

## Configuración
Para crear la infraestructura es necesario:

* Instalar Terraform
  * Descargarlo desde la [página oficial](https://www.terraform.io/downloads.html "Link a Terraform Downloads").
  * Agregarlo al Path de Windows, tal como se indica en [este artículo](https://stackoverflow.com/questions/1618280/where-can-i-set-path-to-make-exe-on-windows "Cómo agregar al PATH de Windows").
* Instalar [AWS CLI](https://docs.aws.amazon.com/es_es/cli/latest/userguide/cli-chap-install.html "Link para instalar AWS CLI")
* Crear una [AWS Access Key](https://console.aws.amazon.com/iam/home?#/security_credentials "Link para crear Access Key").
* Configurar AWS CLI:
  ~~~
  aws configure
  ~~~
  * Ingresar el ``Access Key ID``
  * Ingresar el ``Secret Access Key``
  * Ingresar ``Default region name`` que en este caso es ``us-east-1``
* Ingresar a la carpeta ``terraform`` presente en este repositorio
* Editar el archivo ``variables.tf`` rellenando con la información correspondiente a la base de datos, la imagen usada pr el Launch Configuration, y el vpc usado en la infraestructura.
  * Es necesario crear el componente ``vpc`` manualmente en la consola de AWS, para luego agregarlo a este archivo. 
* Inicializamos el ambiente de Terraform:
  ~~~
  terraform init
  ~~~
* Chequeamos que la configuración no tenga errores:

  ~~~
  terraform plan
  ~~~
* Creamos la infraestructura en nuestra cuenta de AWS
  ~~~
  terraform apply
  ~~~
* En caso de querer borrar los cambios hechos mediante Terraform:
  ~~~
  terraform destroy
  ~~~

## Documentación
En el archivo ``main.tf`` se definieron los componentes a crear en la nueva infraestructura:

### Security Group ``aws_security_group``
* Configurado con los puertos abiertos necesarios para que el Load Balancer funcione correctamente.
* Nombre en AWS: ``web-elb-sg-cd-3``
### Launch Configuration ``aws_launch_configuration``
* Asociado a la llave ``iluovo_key.pem`` creada para entregas anteriores.
* Define el uso de instancias ``t2.micro``
* Asociada a la ami definida en ``variables.tf``
* Nombre en AWS: ``config-env-3``
### Auto Scalling Group ``aws_autoscaling_group``
* Capacidad deseada fijada en 2 instancias
* Capacidad máxima fijada en 2 instancias
* Capacidad mínima fijada en 1 instancia
* Asociada al Launch Configuration antes mencionado
* Asociado a los subnets:
  * ``subnet-2489f269``
  * ``subnet-d41fa9f5``
* Nombre en AWS: ``asg-cd-3``
### Application Load Balancer ``aws_alb``
* Asociado al Security Group antes mencionado
* Asociado a los subnets:
  * ``subnet-2489f269``
  * ``subnet-d41fa9f5``
* Nombre en AWS: ``redirect-load-balancer-3``
### Target Group ``aws_alb_target_group``
* Puerto: ``8000``
* Protocolo: ``HTTP``
* vpc se agrega a través de las variables del archivo ``variables.tf``
* Health Check:
  * path: ``/``
  * Puerto: ``8000``
* Nombre en AWS: ``target-group-3``
### Relación Auto Scalling Group  - Target Group ``aws_autoscaling_attachment``
* Se relaciona el Auto Scalling Group ya mencionado, que crea las instancias, al Target Group al que se asignan.
### ALB Listeners ``aws_alb_listener``
#### Port 443
  * Utiliza el protocolo HTTPS
  * Utiliza el ``ssl_policy`` correspondiente a ``ELBSecurityPolicy-2016-08``
  * Utiliza el certificado creado con anterioridad para la url [www.iluovobackend.ml](https://www.iluovobackend.ml "Ruta para el Backend de iluovo"), enlazado mediante su ``arn``
  * Redirige el trafico desde el puerto 443 del Load Balancer hacia el Target Group antes documentado.
  * Para utilizar este puerto, se requiere configurar manualmente un ``DNS Record`` que asocie el Load Balancer al dominio correspondiente.
#### Port 80
  * Utiliza el protocolo HTTP
  * Redirige el trafico desde el puerto 80 del Load Balancer hacia el Target Group antes documentado.
### Base de Datos RDS ``aws_db_instance``
* Se utiliza el motor ``postgres``, versión ``12.3``
* La zona de disponibilidad es ``us-east-1a``
* Se utiliza el Security Group mencionado anteriormente
* Se utiliza el archivo ``variables.tf`` para definr:
  * name
  * usermane
  * password
  * puerto
### Bucket S3 ``aws_s3_bucket``
* Se crea el bucket definido para los Assets de la pagina [iluovo.ml](https://www.iluovo.ml "Pagina Principal de iluovo").
* Se define como privado
* Para finalizar la configuración, se requiere crear manualmente el componente CloudFront que distribuye los assets desde la Consola de AWS.

---

## Extra
Para facilitar la generación de el archivo ``main.tf`` y algunos de sus componentes, se utilizó la herramienta [Terraforming](https://github.com/dtan4/terraforming "Link al repositorio de Github").
Esta hace ingeniería inversa, de manera que entregue los componentes ya existentes en la cuenta de AWS en formato ``terraform``.

## Mejoras
* Para mejorar el actual IaaC, se podrían generar dos bases de datos, una para ``staging`` y otra para ``producción``. Esto con la adición de los correspondientes parámetros en la sección variables, posiblemente separando las variables de ambos ambientes en dos archivos diferentes. Además, se podrían agregar los parámetros de capacidad, motor y tipo de instancia al mismo archivo, de manera de hacer más personalizable la infraestructura.
* Por otro lado, se podría también personalizar el ``Auto Scalling Group`` y ``Launch Configuration`` añadiendo también las variables de tipo de instancia, capacidad deseada, capacidad mínima y capacidad máxima, así como también el tipo de instancia a generar.
* Además, se puede generar el componente ``vpc`` a través de terraform, sacándolo de la sección de variables. De esta manera no sería necesario configurarla de antemano en la Consola de AWS.
* Por otro lado, se puede agregar también el componente de CloudFront, y asociarlo al bucket S3 destinado a los assets de la página de iluovo. De esta manera seguimos reduciendo las configuraciones que se deben hacer manualmente en la Consola de AWS.
* Finalmente, se puede utilizar el parámetro ``count`` y las ``CONDITIONS`` de terraform para definir si el componente se creará o no.
  ~~~
    count = <CONDITION> ? <TRUE_VAL> : <FALSE_VAL>
  ~~~
  * De esta manera, podríamos agregar una variable en la sección variables, y utilizar las herramientas antes mencionadas para separar el ambiente ``staging`` del de ``producción``. Por ejemplo, al setear la variable ``production = true``, creará los componentes correspondientes a este ambiente, y los de staging en caso contrario.
