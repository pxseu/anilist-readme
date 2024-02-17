

Write-Output "[TEST_SCRIPT]: Starting the project"
Write-Output ""

venv/Scripts/python.exe -m unittest

$env:DEV = $true
$env:INPUT_USER_ID = "889921"
$env:INPUT_GH_TOKEN = "test"
$env:INPUT_PREFERRED_LANGUAGE = "english"
$env:INPUT_TIMEZONE = "UTC"
venv/Scripts/python.exe .

Write-Output ""
Write-Output "[TEST_SCRIPT]: Done"
