# swagger


## swagger-codegen-cli


### build

```bash
linux:~ # wget https://github.com/swagger-api/swagger-codegen/archive/v2.4.7.zip
linux:~ # unzip -qq swagger-codegen-2.4.7.zip
linux:~ # cd swagger-codegen-2.4.7
linux:~ # mvn clean package
linux:~ # cp ./modules/swagger-codegen-cli/target/swagger-codegen-cli.jar .
```


---

### binary

```bash
linux:~ # wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.7/swagger-codegen-cli-2.4.7.jar
```


---

### usage

```bash
linux:~ # java -jar swagger-codegen-cli.jar version
linux:~ # java -jar swagger-codegen-cli.jar help
linux:~ # java -jar swagger-codegen-cli.jar langs

linux:~ # java -jar swagger-codegen-cli.jar help generate
linux:~ # java -jar swagger-codegen-cli.jar generate -i <json_file> -o <output_dir> -l python
```
