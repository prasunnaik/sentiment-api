package com.insurewise.policy.controller;

import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.policy.dto.response.ApplicationDocumentResponse;
import com.insurewise.policy.service.ApplicationDocumentService;
import java.util.List;
import java.util.UUID;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/applications/{id}/documents")
@PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
public class ApplicationDocumentController {

    private final ApplicationDocumentService service;

    public ApplicationDocumentController(
            ApplicationDocumentService service) {
        this.service = service;
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ApplicationDocumentResponse upload(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id,
            @RequestPart("file") MultipartFile file) {

        return service.uploadDocument(
                principal,
                id,
                file);
    }

    @GetMapping
    public List<ApplicationDocumentResponse> list(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {

        return service.listDocuments(
                principal,
                id);
    }

    @DeleteMapping("/{documentId}")
    public void delete(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id,
            @PathVariable UUID documentId) {

        service.deleteDocument(
                principal,
                id,
                documentId);
    }
}
