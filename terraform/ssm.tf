resource "aws_ssm_parameter" "dynamodb_table_arn" {
  name  = "/projects/cgc-etl/dynamodb/table_arn"
  type  = "String"
  value = aws_dynamodb_table.covid.arn
}

resource "aws_ssm_parameter" "dynamodb_stream_arn" {
  name  = "/projects/cgc-etl/dynamodb/stream_arn"
  type  = "String"
  value = aws_dynamodb_table.covid.stream_arn
}

resource "aws_ssm_parameter" "dynamodb_table_id" {
  name  = "/projects/cgc-etl/dynamodb/table_id"
  type  = "String"
  value = aws_dynamodb_table.covid.id
}

# This will be created by serverless framework deploying lambdas
data "aws_ssm_parameter" "main_arn" {
  name       = "/projects/cgc-etl/lambda/main_arn"
  depends_on = [null_resource.sls_deploy]
}
