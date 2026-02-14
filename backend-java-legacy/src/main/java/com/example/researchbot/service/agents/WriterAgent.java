package com.example.researchbot.service.agents;

import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class WriterAgent {

    private final ChatClient chatClient;

    public WriterAgent(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String write(String refinedContent) {
        SystemMessage systemMessage = new SystemMessage("You are a Writer Agent. Your goal is to write a final, polished research report based on the refined content. Format it professionally with headers, bullet points, and a clear structure. Use Markdown.");
        UserMessage userMessage = new UserMessage("Refined Content:\n" + refinedContent);
        
        return chatClient.call(new Prompt(List.of(systemMessage, userMessage))).getResult().getOutput().getContent();
    }
}
