from corelib.platdb import (Application, 
                            CDN, 
                            Compute,
                            Deployment, 
                            EgressController, 
                            Insights, 
                            Repo,
                            Resource, 
                            TrafficController)

neo4j_db_fixtures = [
    (Application, {"name": "app1"}, {"name": "new_app1"}),
    (CDN, {"name": "cdn1"}, {"name": "new_cdn1"}),
    (Compute, {
        "platform": "ec2",
        "address": "1.2.3.4",
        "protocol": "TCP",
        "protocol_multiplexor": "80"
    }, {
        "name": "new_compute1",
        "platform": "k8s",
        "address": "pod-1234nv",
        "protocol": "HTTP",
        "protocol_multiplexor": "80"
    }),
    (Deployment, {
        "deployment_type": "auto_scaling_group",
        "address": "1.2.3.4",
        "protocol": "TCP",
        "protocol_multiplexor": "80"
    }, {
        "deployment_type": "target_group",
        "address": "5.6.7.8",
        "protocol": "HTTP",
        "protocol_multiplexor": "443"
    }),
    (EgressController, {"name": "egress1"}, {"name": "new_egress1"}),
    (Insights, {
        "attribute_name": "attr1",
        "recommendation": "recommendation1",
        "starting_state": "state1",
        "upgraded_state": "state2"
    }, {
        "attribute_name": "new_attr1",
        "recommendation": "new_recommendation1",
        "starting_state": "new_state1",
        "upgraded_state": "new_state2"
    }),
    (Repo, {"name": "repo1"}, {"name": "new_repo1"}),
    (Resource, {
        "name": "resource1",
        "address": "1.2.3.4",
        "protocol": "TCP",
        "protocol_multiplexor": "80"
    }, {
        "name": "new_resource1",
        "address": "5.6.7.8",
        "protocol": "HTTP",
        "protocol_multiplexor": "443"
    }),
    (TrafficController, {
        "access_names": "access1",
        "address": "1.2.3.4",
        "protocol": "TCP",
        "protocol_multiplexor": "80"
    }, {
        "access_names": "new_access1",
        "address": "5.6.7.8",
        "protocol": "HTTP",
        "protocol_multiplexor": "443"
    })
]
