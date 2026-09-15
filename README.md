} catch (IOException | RuntimeException exception) {

    System.err.println("========== S3 UPLOAD FAILED ==========");
    System.err.println("Exception class: " + exception.getClass().getName());
    System.err.println("Exception message: " + exception.getMessage());
    exception.printStackTrace(System.err);
    System.err.println("======================================");

    throw new S3FileStorageException(
            "Unable to upload file to S3",
            exception);
}



amazonS3.putObject(
        new PutObjectRequest(
                properties.bucketName(),
                key,
                file.getInputStream(),
                metadata));





System.err.println("========== S3 UPLOAD START ==========");
System.err.println("Bucket: " + properties.bucketName());
System.err.println("Key: " + key);
System.err.println("File: " + file.getOriginalFilename());
System.err.println("====================================");





