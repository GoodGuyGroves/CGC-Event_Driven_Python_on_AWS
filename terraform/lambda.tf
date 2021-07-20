resource "aws_lambda_permission" "cloudwatch_etl_main" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "CGC-python-etl-dev-main"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_8pm.arn
  depends_on    = [time_sleep.wait_for_main_lambda]
}

data "aws_lambda_function" "etl_main" {
  function_name = "CGC-python-etl-dev-main"
}

data "aws_lambda_function" "etl_alert" {
  function_name = "CGC-python-etl-dev-alert"
  depends_on    = [null_resource.sls_deploy_all]
}

resource "aws_lambda_event_source_mapping" "dynamodb_alert" {
  event_source_arn                   = aws_dynamodb_table.covid.stream_arn
  function_name                      = data.aws_lambda_function.etl_alert.arn
  starting_position                  = "LATEST"
  batch_size                         = 100
  maximum_batching_window_in_seconds = 10
  enabled                            = true
}