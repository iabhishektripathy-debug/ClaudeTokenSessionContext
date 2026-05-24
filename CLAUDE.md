# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Spring Boot REST service that serves architectural-lighting product data (modeled on Acuity Brands / Luminis luminaires). Product documents live as `<productId>.json` files under `src/main/resources`; they are bulk-loaded into a Redis cache and served by `productId`.

- **Java 21** (build target), built/run on the locally installed JDK (currently Java 25 — see "Gotchas").
- **Spring Boot 3.4.2**, Maven (no Gradle). Use the bundled Maven wrapper `./mvnw`.
- Dependencies: `spring-boot-starter-web`, `-actuator`, `-data-redis`.

## Commands

```bash
./mvnw test                                  # full test suite
./mvnw test -Dtest=HelloControllerTest       # single test class
./mvnw test -Dtest=HelloControllerTest#rootReturnsServiceInfo   # single test method
./mvnw clean compile                         # clean build (see stale-resources gotcha below)
./mvnw spring-boot:run                        # run on http://localhost:8080
python3 scripts/gen_products.py              # regenerate the 100 sample product JSON files
```

Redis must be running for the app to serve product data (it is NOT auto-started):

```bash
redis-server --daemonize yes --save "" --appendonly no   # start (no persistence)
redis-cli ping                                            # PONG == up
redis-cli shutdown nosave                                 # stop
```

## Request flow (the core of the app)

The product feature spans three files and is only understandable read together:

1. **`web/ProductController`** — `PUT /productID` triggers a cache load; `GET /productID/{id}` reads the cached JSON. The GET returns the **raw JSON string** from Redis as `ResponseEntity<String>` with `Content-Type: application/json`, or **404** when the key is absent. It does NOT deserialize into a model.
2. **`cache/RedisHandler`** — `load()` reads every `*.json` from the `src/main/resources` directory (path is `product.json-dir`, default `src/main/resources`), parses each to extract the `productId` field, and stores it in Redis as `key=productId, value=raw JSON body` via `StringRedisTemplate`. `get(productId)` returns that raw body. Returns the count loaded.
3. **`src/main/resources/*.json`** — 101 product documents named `<productId>.json`. The filename equals the `productId` inside the body, and `ordering.sku` / the `datasheetUrl` path also echo it.

Operational sequence: **start Redis → run app → `PUT /productID` once to populate → `GET /productID/{id}`**. On a fresh/flushed Redis, GETs return 404 until the PUT runs.

## Data model

`web/ProductDetails` is a Java `record` (with nested records: `Photometrics`, `Electrical`, `Optics`, `Physical`/`Dimensions`, `Compliance`, `Ordering`) that documents the schema every product JSON conforms to. It is currently **not referenced by the controller** (the GET passes raw JSON through) — keep it in sync with the JSON shape, or wire the controller back to it if typed responses/validation are needed. `2726523.json` is the canonical hand-built sample; the other 100 are generated.

`web/HelloController` (`GET /`) and Actuator (`/actuator/health`, `/actuator/info`) are unrelated scaffolding.

## Gotchas (discovered the hard way)

- **`load()` reads the filesystem, not the classpath.** It resolves `src/main/resources` relative to the working directory, so it works under `./mvnw spring-boot:run` (run from repo root) but **not from a packaged jar**. An earlier classpath-glob implementation read `target/classes`, which had drifted from source (see next point). If you package this as a jar, switch to classpath resource resolution and re-test the count.
- **Stale `target/classes` resources.** Maven copies resources into `target/classes` and does NOT delete files removed from `src/main/resources` without `clean`. If the loaded count ever exceeds the source file count, run `./mvnw clean`.
- **Port 8080 lingers after `spring-boot:run`.** `mvn spring-boot:run` forks a child JVM; killing the backgrounded mvn PID does NOT kill it, leaving a stale app on 8080 (causes confusing 404s for newly added endpoints). Free the port before re-running: `lsof -ti tcp:8080 -sTCP:LISTEN | xargs -r kill -9`.
- **Sample data is synthetic.** Acuity's site returns HTTP 403 to automated fetches, so product spec values are representative, not real. `scripts/gen_products.py` is seeded (`random.seed(2726523)`) → deterministic regeneration; it reserves `2726523` and writes by `productId`.
