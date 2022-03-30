from flask import Flask, request, jsonify
from os import environ
import logging
# from kubernetes import client, config

webhook = Flask(__name__)

webhook.config['K8S_NAMESPACE'] = environ.get('K8S_NAMESPACE')

webhook.logger.setLevel(logging.INFO)

if "K8S_NAMESPACE" not in environ:    
    webhook.logger.error("Container environment did not set")
    exit(1)

@webhook.route('/webhook', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")

    # webhook.logger.info(f'request_info {request_info}')

    # webhook.logger.info(f"===============================================================\n")
    
    # webhook.logger.info(f'container ==================== {request_info["request"]["object"]["spec"]["template"]["spec"]["containers"]}')

    # webhook.logger.info(f"===============================================================\n")

    # webhook.logger.info(f'container ==================== {request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][0]["resources"].get("limits")}')

    # webhook.logger.info(f"===============================================================\n")

    if  (webhook.config['K8S_NAMESPACE'] != request_info["request"]["object"]["metadata"].get("namespace")):
        webhook.logger.info("No block for this namespace")
        return admission_response(True, uid, f"No block for this namespace")

    elif  (webhook.config['K8S_NAMESPACE'] == request_info["request"]["object"]["metadata"].get("namespace")) \
        and (request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][0]["resources"].get("limits") == None or \
         request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"].get("cpu") == None):
        webhook.logger.error("Container resources limits cpu did not set")
        return admission_response(False, uid, f"Container resources limits cpu did not set")

    elif (webhook.config['K8S_NAMESPACE'] == request_info["request"]["object"]["metadata"].get("namespace")) \
        and int(request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"].get("cpu")) < 2:        
        webhook.logger.info(f'Create K8S object')
        return admission_response(True, uid, f"Create K8S object")
    else:
        webhook.logger.error(f'Disallowed create K8S object')
        return admission_response(False, uid, f"Disallowed create K8S object")


def admission_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response":
                        {"allowed": allowed,
                         "uid": uid,
                         "status": {"message": message}
                         }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0',
                port=5000)
