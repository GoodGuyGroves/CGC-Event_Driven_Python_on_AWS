resource "null_resource" "sls_deploy" {
  triggers = {
    id = "${uuid()}"
  }
  provisioner "local-exec" {
    working_dir = "../"
    command     = "sls deploy -v"
  }
}