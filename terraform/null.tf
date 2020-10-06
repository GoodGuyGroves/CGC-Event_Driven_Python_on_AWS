resource "null_resource" "sls_deploy_all" {
  triggers = {
    id = "${uuid()}"
  }
  provisioner "local-exec" {
    working_dir = "../"
    command     = <<EOF
sls package
sls deploy
EOF
  }
}