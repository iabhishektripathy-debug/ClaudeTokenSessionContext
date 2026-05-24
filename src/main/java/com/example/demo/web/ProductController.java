package com.example.demo.web;

import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.cache.RedisHandler;

@RestController
public class ProductController {

    private final RedisHandler redisHandler;

    public ProductController(RedisHandler redisHandler) {
        this.redisHandler = redisHandler;
    }

    /**
     * Loads all product JSON files from resources into the Redis cache.
     *
     * @return a summary with the number of products loaded
     */
    @PutMapping("/productID")
    public Map<String, Object> loadProducts() {
        int loaded = redisHandler.load();
        return Map.of(
                "status", "loaded",
                "count", loaded
        );
    }

    /**
     * Returns the product JSON body cached in Redis for the given id.
     *
     * @return the JSON body, or 404 if the product is not in the cache
     */
    @GetMapping("/productID/{id}")
    public ResponseEntity<String> getProduct(@PathVariable String id) {
        String json = redisHandler.get(id);
        if (json == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .body(json);
    }
}
