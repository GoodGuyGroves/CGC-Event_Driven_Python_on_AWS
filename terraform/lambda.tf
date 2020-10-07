resource "aws_lambda_permission" "cloudwatch_etl_main" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "CGC-python-etl-dev-main"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_8pm.arn
}

data "aws_lambda_function" "etl_alert" {
  function_name = "CGC-python-etl-dev-alert"
}

resource "aws_lambda_event_source_mapping" "dynamodb_alert" {
  event_source_arn  = aws_dynamodb_table.covid.stream_arn
  function_name     = data.aws_lambda_function.etl_alert.arn
  starting_position = "LATEST"
  batch_size = 100
  maximum_batching_window_in_seconds = 10
  enabled = true
}