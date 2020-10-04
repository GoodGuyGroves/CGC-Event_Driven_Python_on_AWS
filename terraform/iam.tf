# Create IAM user for redash
resource "aws_iam_group" "challenge_temp" {
    name = "ChallengeTempGroup"
    path = "/groups/"
}

resource "aws_iam_policy" "challenge_dynamodb_policy" {
    name = "ChallengeDynamoDBPolicy"
    description = "Gives access to DynamoDB specifically for the #CloudGuruChallenge ETL Challenge"
    policy = file("policies/challenge_dynamodb_policy.json")
}

resource "aws_iam_group_policy_attachment" "challenge_policy_attach" {
    group = aws_iam_group.challenge_temp.name
    policy_arn = aws_iam_policy.challenge_dynamodb_policy.arn
}

resource "aws_iam_user" "redash" {
    name = "redash"
}

resource "aws_iam_access_key" "redash_key" {
    user = aws_iam_user.redash.name
    pgp_key = "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"
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