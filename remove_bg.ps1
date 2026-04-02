Add-Type -AssemblyName System.Drawing

$inputPath = Join-Path $PSScriptRoot "images\download.jpg"
$outputPath = Join-Path $PSScriptRoot "images\logo_continental.png"

# Load original logo
$original = [System.Drawing.Image]::FromFile($inputPath)

# Create new image with padding
$padX = 20
$padY = 10
$newWidth = $original.Width + (2 * $padX)
$newHeight = $original.Height + (2 * $padY)

$bmp = New-Object System.Drawing.Bitmap($newWidth, $newHeight, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

# Fill background with dark navy (#0F172A)
$bgColor = [System.Drawing.Color]::FromArgb(255, 15, 23, 42)
$g.Clear($bgColor)

# Draw original logo on top
$g.DrawImage($original, $padX, $padY, $original.Width, $original.Height)
$g.Dispose()

# Now replace the light/white/checkered pixels with the dark background color
for ($x = 0; $x -lt $bmp.Width; $x++) {
    for ($y = 0; $y -lt $bmp.Height; $y++) {
        $pixel = $bmp.GetPixel($x, $y)
        $brightness = ($pixel.R * 0.299 + $pixel.G * 0.587 + $pixel.B * 0.114)
        # Replace light pixels (white/checkered background) with dark navy
        if ($brightness -gt 180) {
            $bmp.SetPixel($x, $y, $bgColor)
        }
        # Smooth transition zone
        elseif ($brightness -gt 140) {
            $ratio = ($brightness - 140) / 40.0
            $r = [int]($pixel.R * (1 - $ratio) + $bgColor.R * $ratio)
            $g2 = [int]($pixel.G * (1 - $ratio) + $bgColor.G * $ratio)
            $b = [int]($pixel.B * (1 - $ratio) + $bgColor.B * $ratio)
            $bmp.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(255, $r, $g2, $b))
        }
    }
}

$bmp.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$original.Dispose()
$bmp.Dispose()
Write-Host "Logo avec fond sombre cree : $outputPath"
