package com.example.demo.web;

import java.time.Instant;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/")
    public Map<String, Object> hello() {
        return Map.of(
                "service", "demo-service",
                "message", "Hello from Spring Boot",
                "timestamp", Instant.now().toString()
        );
    }
}
