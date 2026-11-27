# AWS IAM OIDC provider + deploy role for GitHub Actions.
# Validate: terraform init -backend=false && terraform validate
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

variable "github_repo" {
  description = "owner/repo allowed to assume the role"
  type        = string
  default     = "gvarun17/github-actions-gh200"
}

variable "environment" {
  description = "GitHub environment name bound in the sub claim"
  type        = string
  default     = "prod"
}

resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

data "aws_iam_policy_document" "trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:environment:${var.environment}"]
    }
  }
}

resource "aws_iam_role" "gh_deploy" {
  name                 = "gh-deploy-${var.environment}"
  assume_role_policy   = data.aws_iam_policy_document.trust.json
  max_session_duration = 3600
}

output "role_arn" {
  value = aws_iam_role.gh_deploy.arn
}
