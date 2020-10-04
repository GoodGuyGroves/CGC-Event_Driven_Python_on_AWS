resource "aws_dynamodb_table" "covid" {
  name           = "covid-stats"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "date"
  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Name = "cloudguruchallenge"
  }
}