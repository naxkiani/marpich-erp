{{- define "marpich-iam.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "marpich-iam.fullname" -}}
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

{{- define "marpich-iam.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "marpich-iam.labels" -}}
helm.sh/chart: {{ include "marpich-iam.chart" . }}
{{ include "marpich-iam.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: marpich-identity-platform
{{- end }}

{{- define "marpich-iam.selectorLabels" -}}
app.kubernetes.io/name: {{ include "marpich-iam.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "marpich-iam.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "marpich-iam.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
