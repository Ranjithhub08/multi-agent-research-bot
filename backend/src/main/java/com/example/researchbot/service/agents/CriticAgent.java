package com.example.researchbot.service.agents;

import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CriticAgent {

    private final ChatClient chatClient;

    public CriticAgent(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String critique(String researchContent) {
        SystemMessage systemMessage = new SystemMessage("You are a Critic Agent. specific task: Review the provided research content for logical fallacies, missing information, and potential biases. Provide a constructive critique to improve the quality.");
        UserMessage userMessage = new UserMessage("Research Content:\n" + researchContent);
        
        return chatClient.call(new Prompt(List.of(systemMessage, userMessage))).getResult().getOutput().getContent();
    }
}
