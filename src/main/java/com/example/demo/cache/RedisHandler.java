package com.example.demo.cache;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Loads product JSON documents into Redis and reads them back.
 *
 * <p>Keys are the {@code productId} and values are the raw JSON body.
 */
@Component
public class RedisHandler {

    private final StringRedisTemplate redisTemplate;
    private final ObjectMapper objectMapper;
    private final Path jsonDir;

    public RedisHandler(StringRedisTemplate redisTemplate,
                        ObjectMapper objectMapper,
                        @Value("${product.json-dir:src/main/resources}") String jsonDir) {
        this.redisTemplate = redisTemplate;
        this.objectMapper = objectMapper;
        this.jsonDir = Paths.get(jsonDir);
    }

    /**
     * Reads every {@code *.json} file from the {@code src/main/resources} folder and stores
     * each one in Redis, keyed by its {@code productId} with the raw JSON body as the value.
     *
     * @return the number of documents loaded
     */
    public int load() {
        int loaded = 0;
        try (DirectoryStream<Path> jsonFiles = Files.newDirectoryStream(jsonDir, "*.json")) {
            for (Path file : jsonFiles) {
                String json = Files.readString(file, StandardCharsets.UTF_8);
                JsonNode node = objectMapper.readTree(json);
                JsonNode productId = node.get("productId");
                if (productId == null || productId.asText().isBlank()) {
                    // Not a product document; skip it.
                    continue;
                }
                redisTemplate.opsForValue().set(productId.asText(), json);
                loaded++;
            }
        } catch (IOException e) {
            throw new IllegalStateException("Failed to load product JSON files from " + jsonDir, e);
        }
        return loaded;
    }

    /**
     * Returns the JSON body stored for the given product id, or {@code null} if absent.
     *
     * @param productId the Redis key
     * @return the JSON body, or {@code null} if no entry exists
     */
    public String get(String productId) {
        return redisTemplate.opsForValue().get(productId);
    }
}
