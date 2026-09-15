2026-09-15T12:05:42.888+05:30  INFO 34192 --- [insurewise-service] [           main] com.insurewise.InsurewiseApplication     : Starting InsurewiseApplication using Java 21.0.12 with PID 34192 (C:\Users\psumans\CAP-Code\insurewise-cap-angular-be\insurewise-service\target\classes started by psumans in C:\Users\psumans\CAP-Code)
2026-09-15T12:05:42.891+05:30  INFO 34192 --- [insurewise-service] [           main] com.insurewise.InsurewiseApplication     : No active profile set, falling back to 1 default profile: "default"
2026-09-15T12:05:44.422+05:30  WARN 34192 --- [insurewise-service] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanDefinitionStoreException: Failed to read candidate component class: file [C:\Users\psumans\CAP-Code\insurewise-cap-angular-be\insurewise-service\target\classes\com\insurewise\auth\config\AuthBeansConfig.class]
2026-09-15T12:05:44.437+05:30  INFO 34192 --- [insurewise-service] [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2026-09-15T12:05:44.476+05:30 ERROR 34192 --- [insurewise-service] [           main] o.s.boot.SpringApplication               : Application run failed

org.springframework.beans.factory.BeanDefinitionStoreException: Failed to read candidate component class: file [C:\Users\psumans\CAP-Code\insurewise-cap-angular-be\insurewise-service\target\classes\com\insurewise\auth\config\AuthBeansConfig.class]
	at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.scanCandidateComponents(ClassPathScanningCandidateComponentProvider.java:510) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.findCandidateComponents(ClassPathScanningCandidateComponentProvider.java:351) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.boot.context.properties.ConfigurationPropertiesScanRegistrar.scan(ConfigurationPropertiesScanRegistrar.java:85) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.context.properties.ConfigurationPropertiesScanRegistrar.registerBeanDefinitions(ConfigurationPropertiesScanRegistrar.java:62) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.context.annotation.ImportBeanDefinitionRegistrar.registerBeanDefinitions(ImportBeanDefinitionRegistrar.java:86) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.lambda$loadBeanDefinitionsFromRegistrars$1(ConfigurationClassBeanDefinitionReader.java:376) ~[spring-context-6.1.6.jar:6.1.6]
	at java.base/java.util.LinkedHashMap.forEach(LinkedHashMap.java:986) ~[na:na]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitionsFromRegistrars(ConfigurationClassBeanDefinitionReader.java:375) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitionsForConfigurationClass(ConfigurationClassBeanDefinitionReader.java:148) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ConfigurationClassBeanDefinitionReader.loadBeanDefinitions(ConfigurationClassBeanDefinitionReader.java:120) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.processConfigBeanDefinitions(ConfigurationClassPostProcessor.java:428) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry(ConfigurationClassPostProcessor.java:289) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanDefinitionRegistryPostProcessors(PostProcessorRegistrationDelegate.java:349) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(PostProcessorRegistrationDelegate.java:118) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.support.AbstractApplicationContext.invokeBeanFactoryPostProcessors(AbstractApplicationContext.java:788) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:606) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:146) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:754) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:456) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:334) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1354) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1343) ~[spring-boot-3.2.5.jar:3.2.5]
	at com.insurewise.InsurewiseApplication.main(InsurewiseApplication.java:13) ~[classes/:na]
Caused by: java.lang.IllegalStateException: Failed to introspect Class [com.insurewise.framework.s3.config.S3AutoConfiguration] from ClassLoader [jdk.internal.loader.ClassLoaders$AppClassLoader@76ed5528]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:483) ~[spring-core-6.1.6.jar:6.1.6]
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:360) ~[spring-core-6.1.6.jar:6.1.6]
	at org.springframework.util.ReflectionUtils.getUniqueDeclaredMethods(ReflectionUtils.java:417) ~[spring-core-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.lambda$getTypeForFactoryMethod$1(AbstractAutowireCapableBeanFactory.java:750) ~[spring-beans-6.1.6.jar:6.1.6]
	at java.base/java.util.concurrent.ConcurrentHashMap.computeIfAbsent(ConcurrentHashMap.java:1708) ~[na:na]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.getTypeForFactoryMethod(AbstractAutowireCapableBeanFactory.java:749) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.determineTargetType(AbstractAutowireCapableBeanFactory.java:682) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.predictBeanType(AbstractAutowireCapableBeanFactory.java:653) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.AbstractBeanFactory.isFactoryBean(AbstractBeanFactory.java:1676) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doGetBeanNamesForType(DefaultListableBeanFactory.java:562) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeanNamesForType(DefaultListableBeanFactory.java:534) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeansOfType(DefaultListableBeanFactory.java:661) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBeansOfType(DefaultListableBeanFactory.java:653) ~[spring-beans-6.1.6.jar:6.1.6]
	at org.springframework.boot.context.TypeExcludeFilter.getDelegates(TypeExcludeFilter.java:77) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.boot.context.TypeExcludeFilter.match(TypeExcludeFilter.java:65) ~[spring-boot-3.2.5.jar:3.2.5]
	at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.isCandidateComponent(ClassPathScanningCandidateComponentProvider.java:541) ~[spring-context-6.1.6.jar:6.1.6]
	at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.scanCandidateComponents(ClassPathScanningCandidateComponentProvider.java:471) ~[spring-context-6.1.6.jar:6.1.6]
	... 22 common frames omitted
Caused by: java.lang.NoClassDefFoundError: com/amazonaws/auth/AWSCredentials
	at java.base/java.lang.Class.getDeclaredMethods0(Native Method) ~[na:na]
	at java.base/java.lang.Class.privateGetDeclaredMethods(Class.java:3580) ~[na:na]
	at java.base/java.lang.Class.getDeclaredMethods(Class.java:2678) ~[na:na]
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:465) ~[spring-core-6.1.6.jar:6.1.6]
	... 38 common frames omitted
Caused by: java.lang.ClassNotFoundException: com.amazonaws.auth.AWSCredentials
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641) ~[na:na]
	at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188) ~[na:na]
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:526) ~[na:na]
	... 42 common frames omitted


Process finished with exit code 1
