resource "aws_lambda_permission" "cloudwatch_etl_main" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "CGC-python-etl-dev-main"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_8pm.arn
}