wget "https://www.antlr.org/download/antlr-4.10.1-complete.jar" -outfile "antlr4.jar"
$env:CLASSPATH = ".;$pwd\antlr4.jar;"+ $env:CLASSPATH
echo $env:CLASSPATH
java org.antlr.v4.Tool D:\Haizu\robotics_ws\cogni_ws\rei_ws\rei\framework\cognitive\speclanguage\src\main\antlr4\CogniLang.g4 -Dlanguage=Python3 -visitor -o cognilang