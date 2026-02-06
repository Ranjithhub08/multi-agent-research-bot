package com.example.researchbot.service.agents;

import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ResearcherAgent {

    private final ChatClient chatClient;

    public ResearcherAgent(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String research(String topic) {
        SystemMessage systemMessage = new SystemMessage("You are a Researcher Agent. Your goal is to provide a comprehensive, detailed, and factual research summary on the given topic. Include key facts, recent developments, and statistical data where relevant.");
        UserMessage userMessage = new UserMessage("Research Topic: " + topic);
        
        return chatClient.call(new Prompt(List.of(systemMessage, userMessage))).getResult().getOutput().getContent();
    }
}
