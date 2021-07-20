resource "time_sleep" "wait_for_main_lambda" {
  depends_on = [null_resource.sls_deploy_all]

  create_duration = "10s"
}