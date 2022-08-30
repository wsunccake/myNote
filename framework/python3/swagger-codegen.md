# swagger-codegen

## download

```bash
linux:~ $ curl -L -O https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/2.2.1/swagger-codegen-cli-2.2.1.jar
linux:~ $ mv swagger-codegen-cli-2.2.1.jar /usr/local/lib
```


---

## code gen

```bash
linux:~ $ alias swagger-codegen="java -jar /usr/local/lib/swagger-codegen-cli-2.2.1.jar"

linux:~ $ swagger-codegen
linux:~ $ swagger-codegen help
linux:~ $ swagger-codegen help <command>
linux:~ $ swagger-codegen help generate
linux:~ $ swagger-codegen help langs
linux:~ $ swagger-codegen config-help -l <lang>

linux:~ $ swagger-codegen generate -i <input file> -l <lang>
```


---

## example

```bash
linux:~ $ git clone https://github.com/OAI/OpenAPI-Specification.git
linux:~ $ cd OpenAPI-Specification/examples/v2.0/json

linux:~/OpenAPI-Specification/examples/v2.0/json $ swagger-codegen generate -i api-with-examples.json -l python-flask
linux:~/OpenAPI-Specification/examples/v2.0/json $ python3 -m venv venv
linux:~/OpenAPI-Specification/examples/v2.0/json $ source venv/bin/activate
linux:~/OpenAPI-Specification/examples/v2.0/json $ pip3 install -r requirements.txt
linux:~/OpenAPI-Specification/examples/v2.0/json $ python3 -m swagger_server

linux:~ $ curl -L http://127.0.0.1:8080/ui
```

ps: 2.x 只支援 v2, 3.x 才支援 v3


---

## ref

[swagger-codegen](https://github.com/swagger-api/swagger-codegen)