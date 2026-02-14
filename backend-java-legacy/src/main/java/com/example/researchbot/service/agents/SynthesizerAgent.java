package com.example.researchbot.service.agents;

import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SynthesizerAgent {

    private final ChatClient chatClient;

    public SynthesizerAgent(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String synthesize(String researchContent, String critique) {
        SystemMessage systemMessage = new SystemMessage("You are a Synthesizer Agent. Your goal is to improve the provided research content based on the critique. Incorporate the feedback, fix errors, and improve clarity/flow.");
        UserMessage userMessage = new UserMessage("Original Research:\n" + researchContent + "\n\nCritique:\n" + critique);
        
        return chatClient.call(new Prompt(List.of(systemMessage, userMessage))).getResult().getOutput().getContent();
    }
}
