resource "aws_cloudwatch_event_rule" "daily_8pm" {
  name                = "daily-8pm"
  description         = "Runs once a day at 8pm"
  schedule_expression = "cron(0 20 * * ? *)"
  is_enabled          = true
}

resource "aws_cloudwatch_event_target" "check_main_etl_daily_8pm" {
  rule      = aws_cloudwatch_event_rule.daily_8pm.name
  target_id = "lambda"
  arn       = data.aws_ssm_parameter.main_arn.value
}
