Remove-Item -Recurse -Force "$env:USERPROFILE\.m2\repository\com\amazonaws\aws-java-sdk-core\1.12.400"


mvn dependency:get -Dartifact=com.amazonaws:aws-java-sdk-core:1.12.400

Test-Path "$env:USERPROFILE\.m2\repository\com\amazonaws\aws-java-sdk-core\1.12.400\aws-java-sdk-core-1.12.400.jar"


jar tf "$env:USERPROFILE\.m2\repository\com\amazonaws\aws-java-sdk-core\1.12.400\aws-java-sdk-core-1.12.400.jar" | Select-String "AWSCredentials.class"
