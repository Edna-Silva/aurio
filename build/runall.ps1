Set-Location "c:\Users\yamme\Downloads\AURIO\build"
$procs = @()
foreach ($i in 0..9) { $procs += Start-Process python -ArgumentList "toon.py antonio parts\p$i.mp4 $i" -WindowStyle Hidden -PassThru -RedirectStandardError "parts\err$i.log" }
$procs | Wait-Process
"done" | Out-File parts\DONE.txt
