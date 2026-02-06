package com.example.researchbot.dto;

public class ResearchResponse {
    private String finalReport;

    public ResearchResponse() {
    }

    public ResearchResponse(String finalReport) {
        this.finalReport = finalReport;
    }

    public String getFinalReport() {
        return finalReport;
    }

    public void setFinalReport(String finalReport) {
        this.finalReport = finalReport;
    }
}
