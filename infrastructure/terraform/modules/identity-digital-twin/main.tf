# Terraform module — identity-digital-twin (ADR-209)
#
# Prefer shared messaging/database/cache modules. This module only expresses
# twin-specific topic ACLs / Redis key prefix / optional capacity knobs.
# Cloud provider is selected by the environment root, never by twin domain code.

terraform {
  required_version = ">= 1.5.0"
}

variable "environment" {
  type = string
}

variable "topic_prefix" {
  type    = string
  default = "marpich.twin"
}

variable "enable_edge_cache" {
  type    = bool
  default = false
}

output "twin_topic_names" {
  value = [
    "${var.topic_prefix}.lifecycle.v1",
    "${var.topic_prefix}.sync.v1",
    "${var.topic_prefix}.intelligence.v1",
    "${var.topic_prefix}.security.v1",
    "${var.topic_prefix}.graph.v1",
    "${var.topic_prefix}.compliance.v1",
    "${var.topic_prefix}.dlq.v1",
  ]
}

output "notes" {
  value = "Wire topics via shared messaging module; this module is a contract list for GitOps/SRE."
}
