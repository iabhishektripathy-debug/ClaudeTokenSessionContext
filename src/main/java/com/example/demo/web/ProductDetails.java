package com.example.demo.web;

import java.util.List;

/**
 * Data model for an architectural lighting product (luminaire).
 *
 * <p>Modeled on the Luminis "Clermont CT111 Catenary" family (e.g. model CT161),
 * an O12 catenary-mount pendant. Field set is derived from standard architectural
 * lighting specification sheets; populate with values from the product datasheet.
 *
 * @param productId       echoed back from the request path
 * @param productOverview short marketing/summary description of the product
 */
public record ProductDetails(
        String productId,
        String productOverview,
        String modelNumber,
        String name,
        String family,
        String brand,
        String manufacturer,
        String category,
        String mountingType,
        String application,
        Photometrics photometrics,
        Electrical electrical,
        Optics optics,
        Physical physical,
        Compliance compliance,
        String warranty,
        Ordering ordering,
        String datasheetUrl
) {

    /** Light output and color characteristics. */
    public record Photometrics(
            int maxDeliveredLumens,
            List<Integer> availableCctKelvin,
            int minCri,
            Double efficacyLumensPerWatt,
            String distribution
    ) {
    }

    /** Power and driver characteristics. */
    public record Electrical(
            Double wattage,
            String inputVoltageRange,
            String frequencyHz,
            List<String> dimmingProtocols,
            String driverType
    ) {
    }

    /** Optical system. */
    public record Optics(
            String type,
            String beamDistribution,
            String shielding
    ) {
    }

    /** Physical construction and dimensions. */
    public record Physical(
            Dimensions dimensions,
            Double weightKg,
            String housingMaterial,
            List<String> finishOptions,
            String ingressProtection
    ) {
    }

    /** Overall envelope dimensions in millimeters. */
    public record Dimensions(
            Double diameterMm,
            Double heightMm,
            Double lengthMm
    ) {
    }

    /** Ratings, listings and environmental compliance. */
    public record Compliance(
            List<String> listings,
            String ikRating,
            String operatingTempRange,
            boolean darkSkyCompliant
    ) {
    }

    /** Catalog / ordering identifiers. */
    public record Ordering(
            String catalogNumber,
            String sku,
            String exampleOrderCode
    ) {
    }
}
