jar tf "$env:USERPROFILE\.m2\repository\com\amazonaws\aws-java-sdk-core\1.12.400\aws-java-sdk-core-1.12.400.jar" | Select-String "AWSCredentials.class"
