resource "null_resource" "build_python_deps" {
  # triggers = {
  #   id = "${uuid()}"
  # }
  provisioner "local-exec" {
    working_dir = "../layers/pandas"
    command     = <<EOF
./build_layer.sh
EOF
  }
}

resource "null_resource" "sls_deploy_all" {
  # triggers = {
  #   id = "${uuid()}"
  # }
  provisioner "local-exec" {
    working_dir = "../"
    command     = <<EOF
sls package
sls deploy -v
EOF
  }

  provisioner "local-exec" {
    working_dir = "../"
    when        = destroy
    command     = "sls remove"
  }
  depends_on = [null_resource.build_python_deps, aws_ssm_parameter.dynamodb_table_arn,
  aws_ssm_parameter.sns_dynamodb_alert_topic, aws_ssm_parameter.dynamodb_stream_arn]
}