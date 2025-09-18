terraform {
  backend "gcs" {
    bucket = "qwiklabs-gcp-02-c5bbec007868-terraform-state"
    prefix = "agentic-era-hack/dev"
  }
}
