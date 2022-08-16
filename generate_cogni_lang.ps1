if (-not(Test-Path -Path "antlr4.jar" -PathType Leaf)){
    wget "https://www.antlr.org/download/antlr-4.10.1-complete.jar" -outfile "antlr4.jar"
}
$env:CLASSPATH = ".;$pwd\antlr4.jar;"+ $env:CLASSPATH
# Generate python Python
Write-Host "Generating Cognilang language elements for Python"
java org.antlr.v4.Tool framework\cognitive\speclanguage\src\main\antlr4\CogniLang.g4 -Dlanguage=Python3 -visitor -Xexact-output-dir -o framework_python/rei/format/cognilang