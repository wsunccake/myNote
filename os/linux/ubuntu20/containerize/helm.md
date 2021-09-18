# helm 3.x

## install

```bash
[ubuntu:~ ] # curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
[ubuntu:~ ] # apt-get install apt-transport-https --yes
[ubuntu:~ ] # echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
[ubuntu:~ ] # apt-get update
[ubuntu:~ ] # apt-get install helm
```


---

## hello

```bash
[ubuntu:~ ] # mkdir hello
[ubuntu:~ ] # mkdir -p hello/templates

[ubuntu:~ ] # cat << EOF > hello/Chart.yaml
apiVersion: v2
name: hello
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "0.1.0"
EOF

[ubuntu:~ ] # cat << EOF > hello/values.yaml
my:
  message: "hello wolrd"
EOF

[ubuntu:~ ] # cat << EOF > hello/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: {{ .Values.my.message }}
EOF

[ubuntu:~ ] # helm install [--dry-run] [--set my.message="hello helm"] demo hello
[ubuntu:~ ] # helm list
[ubuntu:~ ] # kubectl get cm
[ubuntu:~ ] # kubectl describe cm demo-configmap
```


---

## deploy to chart

```yaml
alpine.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpine
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alpine
  template:
    metadata:
      labels:
        app: alpine
    spec:
      containers:
      - name: alpine
        image: alpine:3.13
        stdin: true
        tty: true
```


### from tempalte

```bash
[ubuntu:~ ] # helm create alpine
[ubuntu:~ ] # tree alpine
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml


[ubuntu:~ ] # grep -Ev '^$|^\s+?#' alpine/Chart.yaml
apiVersion: v2
name: bbb
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"

[ubuntu:~ ] # vi alpine/Chart.yaml
appVersion: "1.16.0" -> appVersion: "3.13"


[ubuntu:~ ] # grep -Ev '^$|^\s+?#' alpine/Chart.yaml
replicaCount: 1
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""
imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""
serviceAccount:
  create: true
  annotations: {}
  name: ""
podAnnotations: {}
podSecurityContext: {}
securityContext: {}
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
resources: {}
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
nodeSelector: {}
tolerations: []
affinity: {}
[ubuntu:~ ] # vi alpine/values.yaml
   repository: nginx ->    repository: alpine

[ubuntu:~ ] # grep -Ev '^$|^\s+?#' alpine/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "bbb.fullname" . }}
  labels:
    {{- include "bbb.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "bbb.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "bbb.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "bbb.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
[ubuntu:~ ] # vi alpine/templates/deployment.yaml
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          stdin: true
          tty: true
#          livenessProbe:
#            httpGet:
#              path: /
#              port: http
#          readinessProbe:
#            httpGet:
#              path: /
#              port: http
```


### simple

```bash
[ubuntu:~ ] # tree chart/
chart/
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   └── _helpers.tpl
└── values.yaml

[ubuntu:~ ] # grep -Ev '^$|^\s+?#' chart/Chart.yaml 
apiVersion: v2
name: chart
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "0.1.0"

[ubuntu:~ ] # grep -Ev '^$|^\s+?#' chart/values.yaml 
alpine:
  replicas: 1
image:
  alpine:
    repository: alpine
    tag: "3.13"

[ubuntu:~ ] # grep -Ev '^$|^\s+?#' chart/templates/deployment.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "chart.fullname" . }}-alpine
  labels:
  {{- include "chart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.alpine.replicas }}
  selector:
    matchLabels:
      app: alpine
    {{- include "chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        app: alpine
      {{- include "chart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - image: {{ .Values.image.alpine.repository }}:{{ .Values.image.alpine.tag | default
          .Chart.AppVersion }}
        name: alpine
        resources: {}
        stdin: true
        tty: true
```
