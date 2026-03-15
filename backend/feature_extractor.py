def extract_features(log):
    # Extracts the Shadow Feature Vector
    return {
        "failed_connection_ratio": float(log.failed_connection_ratio),
        "new_dest_ip_attempts": float(log.new_dest_ip_attempts),
        "port_diversity": float(log.port_diversity),
        "short_session_frequency": float(log.short_session_frequency),
        "suspicious_dns_queries": float(log.suspicious_dns_queries)
    }
