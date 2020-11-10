# iDrac

1. default account and password

root/calvin


2. iDRAC 7 show "Network connection has dropped"

because tls algorithms

```bash
rhel:~ # cat $JAVA_HOME/jre/lib/security/java.security
...
jdk.tls.disabledAlgorithms=SSLv3, RC4, MD5withRSA, DH keySize < 1024, \
 EC keySize < 224, DES40_CBC, RC4_40, 3DES_EDE_CBC 
```

->

```bash
rhel:~ # cat $JAVA_HOME/jre/lib/security/java.security
...
jdk.tls.disabledAlgorithms=SSLv3, RC4, DES, DH keySize < 1024, \
 EC keySize < 224, anon, NULL
```

or

->

```bash
rhel:~ # cat $JAVA_HOME/jre/lib/security/java.security
...
#jdk.tls.disabledAlgorithms=SSLv3, RC4, MD5withRSA, DH keySize < 1024, \
# EC keySize < 224, DES40_CBC, RC4_40, 3DES_EDE_CBC 
```
