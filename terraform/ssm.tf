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