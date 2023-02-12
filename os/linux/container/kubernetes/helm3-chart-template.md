# helm 3.x chart template

## getting started

```bash
[linux:~ ] $ helm create mychart
[linux:~ ] $ rm -rf mychart/templates/*

# demo example
[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-configmap
data:
  myvalue: "Hello World"
EOF
[linux:~ ] $ helm install full-coral ./mychart
[linux:~ ] $ helm get manifest full-coral
[linux:~ ] $ kubectl get configmap mychart-configmap -o yaml

# update example
[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
EOF

[linux:~ ] $ helm install --debug --dry-run --generate-name ./mychart
```

{{ <var> }}: inject variable

---

## built-in object

```
Release
  Release.Name
  Release.Namespace
  Release.IsUpgrade
  Release.IsInstall
  Release.Revision

Values    # -> values.yaml

Chart     # -> Chart.yaml
{{ .Chart.Name }}-{{ .Chart.Version }}

Files
  Files.Get
  (.Files.Get config.ini)

Capabilities

Template
```

---

## values file

```bash
[linux:~ ] $ cat << EOF > mychart/values.yaml
favoriteDrink: coffee
EOF

[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favoriteDrink }}
EOF

[linux:~ ] $ helm install --generate-name --dry-run --debug [--set favoriteDrink=slurm] ./mychart
```

```bash
[linux:~ ] $ cat << EOF > mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
EOF

[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink }}
  food: {{ .Values.favorite.food }}
EOF

[linux:~ ] $ helm install --generate-name --dry-run --debug [--set favorite.drink=slurm] [--set favorite.food=steak] ./mychart
```

---

## template function and pipeline

```bash
[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | repeat 5 | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  snack: {{ .Values.favorite.snack | default "tea" | quote }}
EOF
```

---

## flow control

### if/else

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | default "tea" | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  {{ if eq .Values.favorite.drink "coffee" }}mug: "true"{{ end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643099479-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  mug: "true"

```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | default "tea" | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  {{ if eq .Values.favorite.drink "coffee" }}
    mug: "true"
  {{ end }}
---
# helm install --generate-name --dry-run ./mychart
YAML parse error
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | default "tea" | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  {{ if eq .Values.favorite.drink "coffee" }}
  mug: "true"
  {{ end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643099612-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"

  mug: "true"

```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | default "tea" | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  {{- if eq .Values.favorite.drink "coffee" }}
  mug: "true"
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643099647-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  mug: "true"
---
# helm install --generate-name --dry-run --set favorite.drink=coka ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643100666-configmap
data:
  myvalue: "Hello World"
  drink: "coka"
  food: "PIZZA"
```

{{- 刪掉左邊的 space

-}} 刪掉右邊的 space

### with

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- with .Values.favorite }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643100537-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
---
# helm install --generate-name --dry-run --set favorite=null ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643100488-configmap
data:
  myvalue: "Hello World"
```

### range

```bash
[linux:~ ] $ cat << EOF > mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
pizzaToppings:
  - mushrooms
  - cheese
  - peppers
  - onions
EOF

[linux:~ ] $ cat << EOF > mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- with .Values.favorite }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  {{- end }}
  toppings: |-
    {{- range .Values.pizzaToppings }}
    - {{ . | title | quote }}
    {{- end }}
EOF

[linux:~ ] $ helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643122062-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  toppings: |-
    - "Mushrooms"
    - "Cheese"
    - "Peppers"
    - "Onions"
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- with .Values.favorite }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  toppings: |-
    {{- range $.Values.pizzaToppings }}
    - {{ . | title | quote }}
    {{- end }}
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643122250-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  toppings: |-
    - "Mushrooms"
    - "Cheese"
    - "Peppers"
    - "Onions"

---
# helm install --generate-name --dry-run --set pizzaToppings="{beef,cheese}" ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643122599-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  toppings: |-
    - "Beef"
    - "Cheese"

```

---

## variable

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- with .Values.favorite }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  release: {{ .Release.Name }}
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
nil pointer
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- $relname := .Release.Name -}}
  {{- with .Values.favorite }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  release: {{ $relname }}
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643123319-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "PIZZA"
  release: mychart-1643123319

```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  {{- range $key, $val := .Values.favorite }}
  {{ $key }}: {{ $val | quote }}
  {{- end }}
---
# helm install --generate-name --dry-run ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643123886-configmap
data:
  myvalue: "Hello World"
  drink: "coffee"
  food: "pizza"

---
# helm install --generate-name --dry-run \
#   --set favorite.fruit="apple" \
#   --set favorite.drink="tea" \
#   --set favorite.food=null \
#   ./mychart
apiVersion: v1
kind: ConfigMap
metadata:
  name: mychart-1643126211-configmap
data:
  myvalue: "Hello World"
  drink: "tea"
  fruit: "apple"

```

---

## ref

[helm docs](https://helm.sh/docs)
