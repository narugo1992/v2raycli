def get_generic_routing(no_proxy_on_private: bool = True, no_proxy_on_cn: bool = False,
                        direct_tag: str = 'direct') -> dict:
    rules = []
    if no_proxy_on_private:
        rules.append({
            "type": "field",
            "outboundTag": direct_tag,
            "ip": ["geoip:private"],
        })
    if no_proxy_on_cn:
        rules.append({
            "type": "field",
            "outboundTag": direct_tag,
            "domain": ["geosite:cn"],
        })
        rules.append({
            "type": "field",
            "outboundTag": direct_tag,
            "ip": ["geoip:cn"],
        })

    return {
        "domainStrategy": "IPOnDemand",
        "rules": rules,
    }
