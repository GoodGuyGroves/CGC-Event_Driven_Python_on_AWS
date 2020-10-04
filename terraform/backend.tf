terraform {
  backend "s3" {
    bucket = "terraform-russellgroves"
    key    = "state/projects/cgc-etl/terraform.tfstate"
    region = "af-south-1"
  }
}