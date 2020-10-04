#!/usr/bin/env bash

read terraform_output

access_key=$(echo "${terraform_output}" | jq -r '.access_key')
decrypted_password=$(echo "${terraform_output}" | jq -r '.encrypted_password' | base64 --decode | gpg --decrypt 2> /dev/null)
decrypted_secret=$(echo "${terraform_output}" | jq -r '.encrypted_secret' | base64 --decode | gpg --decrypt 2> /dev/null)

printf "Access key: %s\n" "${access_key}"
printf "Password: %s\n" "${decrypted_password}"
printf "Secret: %s\n" "${decrypted_secret}"
printf "\n"
