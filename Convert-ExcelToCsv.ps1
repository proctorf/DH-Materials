# PowerShell script to convert Excel file to CSV using Excel COM objects
# This requires Microsoft Excel to be installed

param(
    [string]$ExcelFile = "MarriagePaticipantsTable_Messy.xlsx",
    [string]$CsvFile = ""
)

# Set default CSV filename if not provided
if ($CsvFile -eq "") {
    $CsvFile = [System.IO.Path]::ChangeExtension($ExcelFile, ".csv")
}

# Get full paths
$ExcelPath = Resolve-Path $ExcelFile -ErrorAction SilentlyContinue
if (-not $ExcelPath) {
    Write-Error "Excel file '$ExcelFile' not found!"
    exit 1
}

$CsvPath = Join-Path (Get-Location) $CsvFile

Write-Host "Converting Excel file to CSV..." -ForegroundColor Green
Write-Host "Source: $ExcelPath" -ForegroundColor Cyan
Write-Host "Target: $CsvPath" -ForegroundColor Cyan

try {
    # Create Excel application object
    $Excel = New-Object -ComObject Excel.Application
    $Excel.Visible = $false
    $Excel.DisplayAlerts = $false
    
    # Open the workbook
    $Workbook = $Excel.Workbooks.Open($ExcelPath.Path)
    
    # Get the first worksheet
    $Worksheet = $Workbook.Worksheets.Item(1)
    
    # Save as CSV (file format 6 = CSV)
    $Worksheet.SaveAs($CsvPath, 6)
    
    # Close and cleanup
    $Workbook.Close($false)
    $Excel.Quit()
    
    # Release COM objects
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($Worksheet) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($Workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($Excel) | Out-Null
    
    Write-Host "✅ Successfully converted to CSV: $CsvFile" -ForegroundColor Green
    
    # Show file info
    $CsvInfo = Get-Item $CsvPath
    Write-Host "📁 File size: $($CsvInfo.Length) bytes" -ForegroundColor Yellow
    Write-Host "📅 Created: $($CsvInfo.CreationTime)" -ForegroundColor Yellow
    
} catch {
    Write-Error "Failed to convert Excel file: $($_.Exception.Message)"
    
    # Cleanup in case of error
    if ($Excel) {
        try {
            $Excel.Quit()
            [System.Runtime.Interopservices.Marshal]::ReleaseComObject($Excel) | Out-Null
        } catch {}
    }
    exit 1
}
