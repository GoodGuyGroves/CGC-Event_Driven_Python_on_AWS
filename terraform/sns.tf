resource "aws_sns_topic" "dynamodb_alert" {
  name         = "dynamodb-activity"
  display_name = "DynamoDB Activity"
  tags = {
    "creator" = "terraform"
  }
}