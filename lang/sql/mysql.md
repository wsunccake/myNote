# MySQL


## run

```bash
linux:~ # cat run.sh
#!/bin/sh

HOST="node-1.domain.tld"

mysql -u root << EOF
USE nova;
SELECT id, created_at, updated_at, hypervisor_hostname FROM compute_nodes;
-- SELECT id, created_at, updated_at, host FROM services;
SELECT id, created_at, updated_at, host FROM services WHERE host = "$HOST";
EOF

linux:~ # ./run.sh
```
