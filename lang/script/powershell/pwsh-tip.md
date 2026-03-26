# PowerShell TIp

## diff

```pwsh
PS C:\> Compare-Object -ReferenceObject (Get-Content file1.txt) -DifferenceObject (Get-Content file2.txt)
PS C:\> diff (gc file1.txt) (gc file2.txt)
```
