Genetare cert for DNS name webhook.default.svc

openssl req -x509 -sha256 -newkey rsa:2048 -keyout webhook.key -out webhook.crt -days 1024 -nodes -addext "subjectAltName = DNS.1:webhook.default.svc"

docker build -t webhook:validation -f Dockerfile .

cat webhook.key | base64 | tr -d '\n' 

cat webhook.crt | base64 | tr -d '\n'

Add webhook.key and webhook.crt in base64 to 'Secret'

kubectl apply -f webhook-secret.yaml
 
kubectl apply -f webhook-configmap.yaml

kubectl apply -f webhook-service.yaml

kubectl apply -f webhook-deploy.yaml

Add webhook.crt in base64 to 'admission-config'

kubectl apply -f webhook-admission-config.yaml

=================================================================

Check result

Success:

kubectl apply -f create_deploy_with_cpu.yaml

create_deploy_with_cpu.yaml

Failed:

kubectl apply -f create_deploy_without_cpu.yaml
