{{/*
Expand the name of the chart.
*/}}
{{- define "setup-rh-operator-amq-streams.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "setup-rh-operator-amq-streams.fullname" -}}
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
{{- define "setup-rh-operator-amq-streams.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "setup-rh-operator-amq-streams.labels" -}}
helm.sh/chart: {{ include "setup-rh-operator-amq-streams.chart" . }}
{{ include "setup-rh-operator-amq-streams.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: kafka-operator
app.kubernetes.io/part-of: demojam-platform
{{- end }}

{{/*
Selector labels
*/}}
{{- define "setup-rh-operator-amq-streams.selectorLabels" -}}
app.kubernetes.io/name: {{ include "setup-rh-operator-amq-streams.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the namespace to use
*/}}
{{- define "setup-rh-operator-amq-streams.namespace" -}}
{{- default .Release.Namespace .Values.namespace.name }}
{{- end }}