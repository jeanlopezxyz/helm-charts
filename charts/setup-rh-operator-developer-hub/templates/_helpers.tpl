{{/*
Expand the name of the chart.
*/}}
{{- define "setup-rh-operator-developer-hub.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "setup-rh-operator-developer-hub.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "setup-rh-operator-developer-hub.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "setup-rh-operator-developer-hub.labels" -}}
helm.sh/chart: {{ include "setup-rh-operator-developer-hub.chart" . }}
{{ include "setup-rh-operator-developer-hub.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: rhdh-setup
app.kubernetes.io/part-of: demojam-platform
{{- end }}

{{/*
Selector labels
*/}}
{{- define "setup-rh-operator-developer-hub.selectorLabels" -}}
app.kubernetes.io/name: {{ include "setup-rh-operator-developer-hub.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Generate a secure backend secret
*/}}
{{- define "setup-rh-operator-developer-hub.backendSecret" -}}
{{- if .Values.backstage.secrets.backendSecret }}
{{- .Values.backstage.secrets.backendSecret | b64enc }}
{{- else }}
{{- randAlphaNum 32 | b64enc }}
{{- end }}
{{- end }}