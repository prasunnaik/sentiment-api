package com.insurewise.policy.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CategoryRequest(

        @NotBlank(message = "Category name is required")
        @Size(max = 80, message = "Category name cannot exceed 80 characters")
        String name,

        @NotBlank(message = "Category description is required")
        @Size(max = 500, message = "Category description cannot exceed 500 characters")
        String description,

        @NotBlank(message = "Category status is required")
        String status
) {
}



package com.insurewise.policy.dto;

import com.insurewise.policy.entity.Category;

import java.time.LocalDateTime;
import java.util.UUID;

public record CategoryResponse(
        UUID id,
        String name,
        String description,
        String status,
        LocalDateTime createdAt
) {

    public static CategoryResponse from(Category category) {

        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getDescription(),
                category.getStatus(),
                category.getCreatedAt()
        );
    }
}



package com.insurewise.policy.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "categories")
@Getter
@Setter
@NoArgsConstructor
public class Category {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(
            nullable = false,
            length = 80
    )
    private String name;

    @Column(
            nullable = false,
            length = 500
    )
    private String description;

    @Column(
            nullable = false,
            length = 20
    )
    private String status;

    @Column(
            name = "created_at",
            nullable = false
    )
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {

        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }

        if (status == null || status.isBlank()) {
            status = "ACTIVE";
        }
    }
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface CategoryRepository
        extends JpaRepository<Category, UUID> {

    boolean existsByNameIgnoreCase(String name);

    boolean existsByNameIgnoreCaseAndIdNot(
            String name,
            UUID id
    );
}





package com.insurewise.policy.service;

import com.insurewise.policy.dto.CategoryRequest;
import com.insurewise.policy.dto.CategoryResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.repository.CategoryRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@Transactional
public class CategoryService {

    private final CategoryRepository categoryRepository;

    public CategoryService(
            CategoryRepository categoryRepository
    ) {
        this.categoryRepository = categoryRepository;
    }

    @Transactional(readOnly = true)
    public List<CategoryResponse> getAll() {

        return categoryRepository.findAll()
                .stream()
                .map(CategoryResponse::from)
                .toList();
    }

    public CategoryResponse create(
            CategoryRequest request
    ) {

        String name = request.name().trim();

        if (categoryRepository.existsByNameIgnoreCase(name)) {
            throw new IllegalArgumentException(
                    "A category with this name already exists"
            );
        }

        Category category = new Category();

        category.setName(name);

        category.setDescription(
                request.description().trim()
        );

        String status =
                request.status()
                        .trim()
                        .toUpperCase();

        validateStatus(status);

        category.setStatus(status);

        return CategoryResponse.from(
                categoryRepository.save(category)
        );
    }

    public CategoryResponse update(
            UUID id,
            CategoryRequest request
    ) {

        Category category =
                categoryRepository.findById(id)
                        .orElseThrow(() ->
                                new IllegalArgumentException(
                                        "Category not found"
                                )
                        );

        String name = request.name().trim();

        if (categoryRepository
                .existsByNameIgnoreCaseAndIdNot(
                        name,
                        id
                )) {

            throw new IllegalArgumentException(
                    "A category with this name already exists"
            );
        }

        category.setName(name);

        category.setDescription(
                request.description().trim()
        );

        String status =
                request.status()
                        .trim()
                        .toUpperCase();

        validateStatus(status);

        category.setStatus(status);

        return CategoryResponse.from(
                categoryRepository.save(category)
        );
    }

    private void validateStatus(String status) {

        if (!"ACTIVE".equals(status)
                && !"INACTIVE".equals(status)) {

            throw new IllegalArgumentException(
                    "Category status must be ACTIVE or INACTIVE"
            );
        }
    }
}




package com.insurewise.policy.controller;

import com.insurewise.policy.dto.CategoryRequest;
import com.insurewise.policy.dto.CategoryResponse;
import com.insurewise.policy.service.CategoryService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(
            CategoryService categoryService
    ) {
        this.categoryService = categoryService;
    }

    @GetMapping
    public List<CategoryResponse> getAllCategories() {

        return categoryService.getAll();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CategoryResponse createCategory(
            @Valid @RequestBody CategoryRequest request
    ) {

        return categoryService.create(request);
    }

    @PutMapping("/{id}")
    public CategoryResponse updateCategory(
            @PathVariable UUID id,
            @Valid @RequestBody CategoryRequest request
    ) {

        return categoryService.update(id, request);
    }
}



