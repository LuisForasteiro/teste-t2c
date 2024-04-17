$exclude = @("venv", "test_t2c.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "test_t2c.zip" -Force