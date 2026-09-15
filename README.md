Get-ChildItem "$env:USERPROFILE\.m2\repository\com\amazonaws" -Recurse -Filter "aws-java-sdk-core*.jar" -ErrorAction SilentlyContinue | Select-Object FullName
