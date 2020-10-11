# Create IAM user for redash
resource "aws_iam_group" "challenge_temp" {
  name = "ChallengeTempGroup"
  path = "/groups/"
}

resource "aws_iam_policy" "challenge_dynamodb_policy" {
  name        = "ChallengeDynamoDBPolicy"
  description = "Gives access to DynamoDB specifically for the #CloudGuruChallenge ETL Challenge"
  policy      = file("policies/challenge_dynamodb_policy.json")
}

resource "aws_iam_group_policy_attachment" "challenge_policy_attach" {
  group      = aws_iam_group.challenge_temp.name
  policy_arn = aws_iam_policy.challenge_dynamodb_policy.arn
}

resource "aws_iam_user" "redash" {
  name = "redash"
}

data "local_file" "redash_pgp_key" {
  filename = "./keys/redash_base64_encoded.gpg"
}

resource "aws_iam_access_key" "redash_key" {
  user    = aws_iam_user.redash.name
  pgp_key = data.local_file.redash_pgp_key.content_base64
}

resource "aws_iam_user_login_profile" "redash_profile" {
  user                    = aws_iam_user.redash.name
  pgp_key                 = aws_iam_access_key.redash_key.pgp_key
  password_reset_required = true
}

resource "aws_iam_user_group_membership" "challenge_temp" {
  user   = aws_iam_user.redash.name
  groups = [aws_iam_group.challenge_temp.name]
}