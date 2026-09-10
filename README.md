package com.insurewise.claims.service;

import com.insurewise.claims.dto.request.ClaimDependentRequest;
import com.insurewise.claims.dto.response.ClaimDependentResponse;
import com.insurewise.claims.entity.Claim;
import com.insurewise.claims.entity.ClaimDependent;
import com.insurewise.claims.repository.ClaimDependentRepository;
import com.insurewise.claims.repository.ClaimRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.claims.exception.ClaimNotFoundException;


@Service
@Transactional
public class ClaimDependentService {
    private final ClaimRepository claimRepository;
    private final ClaimDependentRepository dependentRepository;

    public ClaimDependentService(
            ClaimRepository claimRepository,
            ClaimDependentRepository dependentRepository) {
        this.claimRepository = claimRepository;
        this.dependentRepository = dependentRepository;
    }

    public ClaimDependentResponse addDependent(
            UUID customerId,
            UUID claimId,
            ClaimDependentRequest request) {

        try {
            Claim claim = requireOwnedClaim(customerId, claimId);

            ClaimDependent dependent = dependentRepository.save(
                    new ClaimDependent(
                            claim,
                            request.fullName(),
                            request.relationship(),
                            request.dateOfBirth(),
                            request.gender()));

            return toResponse(dependent);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimDependentService.addDependent: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<ClaimDependentResponse> listDependents(
            UUID customerId,
            UUID claimId) {

        try {
            requireOwnedClaim(customerId, claimId);

            return dependentRepository.findByClaimId(claimId)
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimDependentService.listDependents: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private Claim requireOwnedClaim(UUID customerId, UUID claimId) {
        return claimRepository.findById(claimId)
                .filter(claim -> claim.isOwnedBy(customerId))
                .orElseThrow(ClaimNotFoundException::new);
    }

    private ClaimDependentResponse toResponse(
            ClaimDependent dependent) {
        return new ClaimDependentResponse(
                dependent.getId(),
                dependent.getClaim().getId(),
                dependent.getFullName(),
                dependent.getRelationship(),
                dependent.getDateOfBirth(),
                dependent.getGender());
    }
}




package com.insurewise.claims.service;

import com.insurewise.claims.dto.response.ClaimDocumentResponse;
import com.insurewise.claims.entity.Claim;
import com.insurewise.claims.entity.ClaimDocument;
import com.insurewise.claims.repository.ClaimDocumentRepository;
import com.insurewise.claims.repository.ClaimRepository;
import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.service.S3StorageService;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import com.insurewise.claims.exception.ClaimDocumentNotFoundException;
import com.insurewise.common.exception.InvalidFileException;
import com.insurewise.claims.exception.ClaimNotFoundException;


@Service
@Transactional
public class ClaimDocumentService {
    private final ClaimRepository claimRepository;
    private final ClaimDocumentRepository documentRepository;
    private final S3StorageService storageService;

    public ClaimDocumentService(
            ClaimRepository claimRepository,
            ClaimDocumentRepository documentRepository,
            S3StorageService storageService) {
        this.claimRepository = claimRepository;
        this.documentRepository = documentRepository;
        this.storageService = storageService;
    }

    public ClaimDocumentResponse uploadDocument(
            UUID customerId,
            UUID claimId,
            MultipartFile file) {

        try {
            Claim claim = requireOwnedClaim(customerId, claimId);

            if (file == null || file.isEmpty()) {
                throw new InvalidFileException(
                        "A non-empty file is required");
            }

            String s3Key = storageService.upload(
                    file,
                    "claim-documents",
                    customerId);

            String fileName = file.getOriginalFilename() == null
                    ? "unnamed-file"
                    : file.getOriginalFilename();

            ClaimDocument document = documentRepository.save(
                    new ClaimDocument(
                            claim,
                            fileName,
                            file.getContentType(),
                            s3Key,
                            customerId));

            return toResponse(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimDocumentService.uploadDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<ClaimDocumentResponse> listDocuments(
            UUID customerId,
            UUID claimId) {

        try {
            requireOwnedClaim(customerId, claimId);

            return documentRepository.findByClaimId(claimId)
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimDocumentService.listDocuments: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void deleteDocument(
            UUID customerId,
            UUID claimId,
            UUID documentId) {

        try {
            requireOwnedClaim(customerId, claimId);

            ClaimDocument document =
                    documentRepository.findById(documentId)
                            .filter(item -> item.getClaim().getId()
                                    .equals(claimId))
                            .orElseThrow(
                                    () -> new ClaimDocumentNotFoundException(
                                            documentId));

            storageService.delete(document.getS3Key());
            documentRepository.delete(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimDocumentService.deleteDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private Claim requireOwnedClaim(
            UUID customerId,
            UUID claimId) {

        return claimRepository.findById(claimId)
                .filter(claim -> claim.isOwnedBy(customerId))
                .orElseThrow(ClaimNotFoundException::new);
    }

    private ClaimDocumentResponse toResponse(
            ClaimDocument document) {

        PresignedUrlResponse download =
                storageService.getPresignedDownloadUrl(
                        document.getS3Key());

        return new ClaimDocumentResponse(
                document.getId(),
                document.getClaim().getId(),
                document.getFileName(),
                document.getContentType(),
                download,
                document.getUploadedBy(),
                document.getCreatedAt());
    }
}




package com.insurewise.claims.service;

import com.insurewise.claims.client.PolicyApplicationLookupClient;
import com.insurewise.claims.client.PolicyApplicationSnapshot;
import com.insurewise.claims.dto.request.ClaimCreateRequest;
import com.insurewise.claims.dto.response.ClaimResponse;
import com.insurewise.claims.entity.Claim;
import com.insurewise.claims.repository.ClaimRepository;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.common.exception.IdempotencyKeyConflictException;
import com.insurewise.claims.exception.ClaimNotFoundException;


@Service
@Transactional
public class ClaimService {
    private final ClaimRepository claimRepository;
    private final PolicyApplicationLookupClient applicationClient;

    public ClaimService(
            ClaimRepository claimRepository,
            PolicyApplicationLookupClient applicationClient) {
        this.claimRepository = claimRepository;
        this.applicationClient = applicationClient;
    }

    public ClaimResponse fileClaim(
            UUID customerId,
            ClaimCreateRequest request) {

        try {
            var existing = claimRepository.findByIdempotencyKey(
                    request.idempotencyKey());

            if (existing.isPresent()) {
                Claim claim = existing.get();

                if (!claim.isOwnedBy(customerId)) {
                    throw new IdempotencyKeyConflictException(
                            "Idempotency key belongs to another customer");
                }

                return toResponse(claim);
            }

            PolicyApplicationSnapshot application =
                    applicationClient.getActiveApplicationForCustomer(
                            request.policyApplicationId(),
                            customerId);

            Long sequence = claimRepository.nextClaimCodeSequence();
            String claimCode = "CLM-" + sequence;

            Claim claim = new Claim(
                    claimCode,
                    request.idempotencyKey(),
                    customerId,
                    application.applicationId(),
                    application.policyName(),
                    request.incidentType(),
                    request.incidentDate(),
                    request.amount(),
                    request.description(),
                    request.documentRef());

            return toResponse(claimRepository.save(claim));

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimService.fileClaim: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public ClaimResponse approveClaim(
            UUID staffUserId,
            UUID claimId) {

        try {
            Claim claim = getClaimEntity(claimId);
            claim.approve(staffUserId);
            return toResponse(claim);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimService.approveClaim: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public ClaimResponse rejectClaim(
            UUID staffUserId,
            UUID claimId) {

        try {
            Claim claim = getClaimEntity(claimId);
            claim.reject(staffUserId);
            return toResponse(claim);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimService.rejectClaim: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public ClaimResponse getClaimForCustomer(
            UUID customerId,
            UUID claimId) {

        try {
            Claim claim = getClaimEntity(claimId);

            if (!claim.isOwnedBy(customerId)) {
                throw new ClaimNotFoundException();
            }

            return toResponse(claim);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimService.getClaimForCustomer: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public ClaimResponse getClaimForStaff(UUID claimId) {

        try {
            return toResponse(getClaimEntity(claimId));

        } catch (Exception exception) {
            System.err.println(
                    "Error in ClaimService.getClaimForStaff: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private Claim getClaimEntity(UUID claimId) {
        return claimRepository.findById(claimId)
                .orElseThrow(() -> new ClaimNotFoundException(claimId));
    }

    private ClaimResponse toResponse(Claim claim) {
        return new ClaimResponse(
                claim.getId(),
                claim.getClaimCode(),
                claim.getCustomerId(),
                claim.getPolicyApplicationId(),
                claim.getPolicyNameSnapshot(),
                claim.getIncidentType(),
                claim.getIncidentDate(),
                claim.getAmount(),
                claim.getDescription(),
                claim.getDocumentRef(),
                claim.getStatus(),
                claim.getProcessedBy(),
                claim.getProcessedAt(),
                claim.getCreatedAt());
    }
}
