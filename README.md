package com.its.issue.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.its.issue.model.Issue;
import com.its.issue.service.IssueService;

import jakarta.validation.Valid;

@CrossOrigin(origins = "http://localhost:4300")
@RestController
@RequestMapping("/api/issues")
public class IssueController {

    private final IssueService issueService;

    public IssueController(IssueService issueService) {
        this.issueService = issueService;
    }

    @PostMapping
    public ResponseEntity<Issue> createIssue(
            @Valid @RequestBody Issue issue) {

        Issue savedIssue = issueService.createIssue(issue);

        return new ResponseEntity<>(
                savedIssue,
                HttpStatus.CREATED
        );
    }

    @GetMapping
    public ResponseEntity<List<Issue>> getAllIssues() {

        return new ResponseEntity<>(
                issueService.getAllIssues(),
                HttpStatus.OK
        );
    }

    @GetMapping("/{issueId}")
    public ResponseEntity<Issue> getIssueById(
            @PathVariable Long issueId) {

        return new ResponseEntity<>(
                issueService.getIssueById(issueId),
                HttpStatus.OK
        );
    }

    @PutMapping("/{issueId}")
    public ResponseEntity<Issue> updateIssue(
            @PathVariable Long issueId,
            @Valid @RequestBody Issue issue) {

        return new ResponseEntity<>(
                issueService.updateIssue(issueId, issue),
                HttpStatus.OK
        );
    }

    @DeleteMapping("/{issueId}")
    public ResponseEntity<Void> deleteIssue(
            @PathVariable Long issueId) {

        issueService.deleteIssue(issueId);

        return new ResponseEntity<>(
                HttpStatus.NO_CONTENT
        );
    }

    @GetMapping("/project/{projectId}")
    public ResponseEntity<List<Issue>> getIssuesByProject(
            @PathVariable Long projectId) {

        return new ResponseEntity<>(
                issueService.getIssuesByProject(projectId),
                HttpStatus.OK
        );
    }

    @GetMapping("/owner/{ownerId}")
    public ResponseEntity<List<Issue>> getIssuesByOwner(
            @PathVariable Long ownerId) {

        return new ResponseEntity<>(
                issueService.getIssuesByOwner(ownerId),
                HttpStatus.OK
        );
    }

    @GetMapping("/assignee/{assigneeId}")
    public ResponseEntity<List<Issue>> getIssuesByAssignee(
            @PathVariable Long assigneeId) {

        return new ResponseEntity<>(
                issueService.getIssuesByAssignee(assigneeId),
                HttpStatus.OK
        );
    }

    @PutMapping("/{issueId}/status")
    public ResponseEntity<Issue> updateIssueStatus(
            @PathVariable Long issueId,
            @RequestBody Map<String, String> request) {

        String status = request.get("status");

        Issue updatedIssue =
                issueService.updateIssueStatus(issueId, status);

        return new ResponseEntity<>(
                updatedIssue,
                HttpStatus.OK
        );
    }

    @PutMapping("/{issueId}/priority")
    public ResponseEntity<Issue> updateIssuePriority(
            @PathVariable Long issueId,
            @RequestBody Map<String, String> request) {

        String priority = request.get("priority");

        Issue updatedIssue =
                issueService.updateIssuePriority(issueId, priority);

        return new ResponseEntity<>(
                updatedIssue,
                HttpStatus.OK
        );
    }

    @PutMapping("/{issueId}/assignee/{assigneeId}")
    public ResponseEntity<Issue> updateIssueAssignee(
            @PathVariable Long issueId,
            @PathVariable Long assigneeId) {

        Issue updatedIssue =
                issueService.updateIssueAssignee(issueId, assigneeId);

        return new ResponseEntity<>(
                updatedIssue,
                HttpStatus.OK
        );
    }
}

package com.its.issue.service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.its.issue.client.ProjectClient;
import com.its.issue.exception.IssueNotFoundException;
import com.its.issue.model.Issue;
import com.its.issue.model.Project;
import com.its.issue.repository.IssueRepository;

@Service
public class IssueServiceImpl implements IssueService {

    private final IssueRepository issueRepository;
    private final ProjectClient projectClient;

    public IssueServiceImpl(
            IssueRepository issueRepository,
            ProjectClient projectClient) {

        this.issueRepository = issueRepository;
        this.projectClient = projectClient;
    }

    @Override
    public Issue createIssue(Issue issue) {

        issue.setCreatedDate(LocalDateTime.now());
        issue.setLastUpdatedDate(LocalDateTime.now());

        return issueRepository.save(issue);
    }

    @Override
    public List<Issue> getAllIssues() {

        return issueRepository.findAll();
    }

    @Override
    public Issue getIssueById(Long issueId) {

        return issueRepository.findById(issueId)
                .orElseThrow(() ->
                    new IssueNotFoundException(
                        "Issue not found with id: " + issueId
                    )
                );
    }

    @Override
    public Issue updateIssue(Long issueId, Issue issue) {

        Issue existingIssue = issueRepository.findById(issueId)
                .orElseThrow(() ->
                    new IssueNotFoundException(
                        "Issue not found with id: " + issueId
                    )
                );

        existingIssue.setSummary(issue.getSummary());
        existingIssue.setDescription(issue.getDescription());
        existingIssue.setPriority(issue.getPriority());
        existingIssue.setAssigneeId(issue.getAssigneeId());
        existingIssue.setStatus(issue.getStatus());
        existingIssue.setProjectId(issue.getProjectId());
        existingIssue.setSprint(issue.getSprint());
        existingIssue.setStoryPoint(issue.getStoryPoint());
        existingIssue.setTags(issue.getTags());
        existingIssue.setType(issue.getType());

        existingIssue.setLastUpdatedDate(LocalDateTime.now());

        return issueRepository.save(existingIssue);
    }

    @Override
    public void deleteIssue(Long issueId) {

        Issue existingIssue = issueRepository.findById(issueId)
                .orElseThrow(() ->
                    new IssueNotFoundException(
                        "Issue not found with id: " + issueId
                    )
                );

        issueRepository.delete(existingIssue);
    }

    @Override
    public List<Issue> getIssuesByProject(Long projectId) {

        return issueRepository.findByProjectId(projectId);
    }

    @Override
    public List<Issue> getIssuesByOwner(Long ownerId) {

        List<Project> projects =
                projectClient.getProjectsByOwner(ownerId);

        List<Issue> issues = new ArrayList<>();

        for (Project project : projects) {

            List<Issue> projectIssues =
                    issueRepository.findByProjectId(project.getId());

            issues.addAll(projectIssues);
        }

        return issues;
    }

    @Override
    public List<Issue> getIssuesByAssignee(Long assigneeId) {

        return issueRepository.findByAssigneeId(assigneeId);
    }

    public Issue updateIssueStatus(Long issueId, String status) {

    Issue issue = issueRepository.findById(issueId)
            .orElseThrow(() ->
                    new RuntimeException("Issue not found: " + issueId));

    issue.setStatus(status);

    return issueRepository.save(issue);
}

@Override
public Issue updateIssuePriority(Long issueId, String priority) {

    Issue issue = issueRepository.findById(issueId)
            .orElseThrow(() ->
                    new RuntimeException("Issue not found: " + issueId));

    issue.setPriority(priority);

    return issueRepository.save(issue);
}

@Override
public Issue updateIssueAssignee(Long issueId, Long assigneeId) {

    Issue issue = issueRepository.findById(issueId)
            .orElseThrow(() ->
                    new RuntimeException("Issue not found: " + issueId));

    issue.setAssigneeId(assigneeId);

    return issueRepository.save(issue);
}

}
package com.its.issue.model;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "issues")
public class Issue {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Summary is required")
    private String summary;

    private String description;

    @NotBlank(message = "Priority is required")
    private String priority;

    @NotNull(message = "Assignee ID is required")
    private Long assigneeId;

    @NotBlank(message = "Status is required")
    private String status;

    private LocalDateTime createdDate;

    private LocalDateTime lastUpdatedDate;

    @NotNull(message = "Project ID is required")
    private Long projectId;

    private String sprint;

    private Integer storyPoint;

    private String tags;

    @NotBlank(message = "Type is required")
    private String type;

    public Issue() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }

    public Long getAssigneeId() {
        return assigneeId;
    }

    public void setAssigneeId(Long assigneeId) {
        this.assigneeId = assigneeId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }

    public LocalDateTime getLastUpdatedDate() {
        return lastUpdatedDate;
    }

    public void setLastUpdatedDate(LocalDateTime lastUpdatedDate) {
        this.lastUpdatedDate = lastUpdatedDate;
    }

    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    public String getSprint() {
        return sprint;
    }

    public void setSprint(String sprint) {
        this.sprint = sprint;
    }

    public Integer getStoryPoint() {
        return storyPoint;
    }

    public void setStoryPoint(Integer storyPoint) {
        this.storyPoint = storyPoint;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}

package com.its.issue.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.its.issue.model.Issue;

public interface IssueRepository extends JpaRepository<Issue, Long> {

    List<Issue> findByProjectId(Long projectId);

    List<Issue> findByAssigneeId(Long assigneeId);
}
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>4.1.0</version>
        <relativePath/>
    </parent>

    <groupId>com.its</groupId>
    <artifactId>issue-service</artifactId>
    <version>0.0.1-SNAPSHOT</version>

    <name>issue-service</name>
    <description>Issue MicroServices for ITS</description>

    <properties>
        <java.version>17</java.version>
        <spring-cloud.version>2025.1.2</spring-cloud.version>
    </properties>

    <!-- Spring Cloud dependency management -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>

        <!-- OpenFeign -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>

        <!-- Eureka Client -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Spring Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webmvc</artifactId>
        </dependency>

        <!-- MySQL -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Swagger -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.8.9</version>
        </dependency>

        <!-- Tests -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webmvc-test</artifactId>
            <scope>test</scope>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
        <finalName>issue</finalName>
    </build>

</project>
spring.application.name=issue-service

server.port=8083

spring.datasource.url=jdbc:mysql://its.cinei2gc4el7.us-east-1.rds.amazonaws.com:3306/issue_db
spring.datasource.username=root
spring.datasource.password=password

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

eureka.client.service-url.defaultZone=http://localhost:8761/eureka
eureka.client.register-with-eureka=true
eureka.client.fetch-registry=true

eureka.instance.prefer-ip-address=true
eureka.instance.ip-address=127.0.0.1

package com.its.issue.client;

import java.util.List;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import com.its.issue.model.Project;

@FeignClient(name = "project-service")
public interface ProjectClient {

    @GetMapping("/api/projects/owner/{ownerId}")
    List<Project> getProjectsByOwner(
            @PathVariable("ownerId") Long ownerId);
}
package com.its.issue.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {

        registry.addMapping("/**")
                .allowedOrigins("http://localhost:4300")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }
}
package com.its.issue.exception;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(IssueNotFoundException.class)
    public ResponseEntity<String> handleIssueNotFound(
            IssueNotFoundException exception) {

        return new ResponseEntity<>(
                exception.getMessage(),
                HttpStatus.NOT_FOUND
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidationErrors(
            MethodArgumentNotValidException exception) {

        Map<String, String> errors = new HashMap<>();

        exception.getBindingResult()
                .getFieldErrors()
                .forEach(error ->
                        errors.put(
                                error.getField(),
                                error.getDefaultMessage()
                        )
                );

        return new ResponseEntity<>(
                errors,
                HttpStatus.BAD_REQUEST
        );
    }
}
package com.its.issue.exception;

public class IssueNotFoundException extends RuntimeException {

    public IssueNotFoundException(String message) {
        super(message);
    }
}

package com.its.issue.model;

public class Project {

    private Long id;
    private String projectName;
    private Long productOwnerId;

    public Project() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getProjectName() {
        return projectName;
    }

    public void setProjectName(String projectName) {
        this.projectName = projectName;
    }

    public Long getProductOwnerId() {
        return productOwnerId;
    }

    public void setProductOwnerId(Long productOwnerId) {
        this.productOwnerId = productOwnerId;
    }
}
package com.its.issue.service;

import java.util.List;

import com.its.issue.model.Issue;

public interface IssueService {

    Issue createIssue(Issue issue);

    List<Issue> getAllIssues();

    Issue getIssueById(Long issueId);

    Issue updateIssue(Long issueId, Issue issue);

    Issue updateIssueStatus(Long issueId, String status);

    void deleteIssue(Long issueId);

    List<Issue> getIssuesByProject(Long projectId);

    List<Issue> getIssuesByOwner(Long ownerId);

    List<Issue> getIssuesByAssignee(Long assigneeId);

    Issue updateIssuePriority(Long issueId, String priority);

    Issue updateIssueAssignee(Long issueId, Long assigneeId);
}
