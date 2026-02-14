package com.example.researchbot.controller;

import com.example.researchbot.dto.ResearchRequest;
import com.example.researchbot.dto.ResearchResponse;
import com.example.researchbot.service.OrchestratorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/research")
@CrossOrigin(origins = "*") // Allow all for development
public class ResearchController {

    private final OrchestratorService orchestratorService;

    public ResearchController(OrchestratorService orchestratorService) {
        this.orchestratorService = orchestratorService;
    }

    @PostMapping
    public ResponseEntity<ResearchResponse> conductResearch(@RequestBody ResearchRequest request) {
        String finalReport = orchestratorService.orchestrateResearch(request.getTopic());
        return ResponseEntity.ok(new ResearchResponse(finalReport));
    }
}
