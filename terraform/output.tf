# DynamoDB
output "dynamodb" {
  description = "DynamoDB table arn, id and stream arn"
  value = {
    table_arn  = aws_dynamodb_table.covid.arn
    table_id   = aws_dynamodb_table.covid.id
    stream_arn = aws_dynamodb_table.covid.stream_arn
  }
}

output "redash_user" {
  value = {
    access_key         = aws_iam_access_key.redash_key.id,
    encrypted_secret   = aws_iam_access_key.redash_key.encrypted_secret,
    encrypted_password = aws_iam_user_login_profile.redash_profile.encrypted_password,
  }
}