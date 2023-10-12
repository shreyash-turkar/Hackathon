
$date = Get-Date
$weekLess = $date.AddDays(-7)
echo $date
echo $weekLess
$files = Get-ChildItem "C:\Windows\System32\winevt\Logs" -Recurse -Filter *.evtx | Where-Object { $_.LastWriteTime -gt $weekLess }

foreach ($f in $files){
    $outfile = "C:\Users\Administrator\Desktop\out\" +  $f.BaseName + ".csv"

    try {
        $out = Get-WinEvent -Path $f.FullName -ErrorAction Stop
        $out | Export-CSV $outfile
    }
    catch [Exception] {
        if ($_.Exception -match " No events were found that match the specified selection criteria.") {
            Write-Host "No events found for" + $f.FullName;
        }
    }

}
