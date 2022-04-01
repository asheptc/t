1. Create an infrastructure diagram for the given requirements.

https://github.com/asheptc/t/blob/main/infrastructure_diagram.drawio (File could be open via https://www.draw.io/)

============================================================================================================================

3. Create a flowchart to monitor 4-key metrics

https://github.com/asheptc/t/blob/main/flowchart_to_monitor.drawio (File could be open via https://www.draw.io/)

===============================================================================================

4. Create a custom validation webhook for kubernetes for the given requirements


Genetare cert for DNS name webhook.default.svc

```bash
openssl req -x509 -sha256 -newkey rsa:2048 -keyout webhook.key -out webhook.crt -days 1024 -nodes -addext "subjectAltName = DNS.1:webhook.default.svc"

docker build -t webhook:validation -f Dockerfile .

cat webhook.key | base64 | tr -d '\n' 

cat webhook.crt | base64 | tr -d '\n'
```

Add webhook.key and webhook.crt in to base64 to 'Secret'

```bash
kubectl apply -f webhook-secret.yaml
 
kubectl apply -f webhook-configmap.yaml

kubectl apply -f webhook-service.yaml

kubectl apply -f webhook-deploy.yaml
```

Add webhook.crt in base64 in to 'admission-config'

```bash
kubectl apply -f webhook-admission-config.yaml
```
=================================================================

Check result

Success:

```bash
kubectl apply -f create_deploy_with_cpu.yaml

create_deploy_with_cpu.yaml
```

Failed:

```bash
kubectl apply -f create_deploy_without_cpu.yaml

Error from server: error when creating "create_deploy_without_cpu.yaml": admission webhook "webhook.default.svc" denied the request: Container resources limits cpu did not set
```