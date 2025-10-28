# Kubernetes Interview Cheat Sheet

## Core Concepts

**Pod**: Smallest deployable unit, one or more containers
**Node**: Worker machine (VM or physical) that runs pods
**Cluster**: Set of nodes managed by Kubernetes
**Control Plane**: Manages cluster (API server, scheduler, controller manager)
**Service**: Stable network endpoint for accessing pods
**Deployment**: Manages ReplicaSets and pod updates
**Namespace**: Virtual cluster for resource isolation

## kubectl Commands

### Cluster Info
```bash
kubectl cluster-info
kubectl version
kubectl get nodes
kubectl describe node node-name
kubectl top nodes                      # Resource usage
```

### Pod Operations
```bash
# List pods
kubectl get pods
kubectl get pods -n namespace
kubectl get pods -o wide               # More details
kubectl get pods --all-namespaces      # All namespaces
kubectl get pods -w                    # Watch mode

# Create pod
kubectl run nginx --image=nginx
kubectl run nginx --image=nginx --port=80

# Describe pod
kubectl describe pod pod-name

# Get pod logs
kubectl logs pod-name
kubectl logs pod-name -f               # Follow
kubectl logs pod-name -c container     # Specific container
kubectl logs pod-name --previous       # Previous instance

# Execute command
kubectl exec pod-name -- ls /app
kubectl exec -it pod-name -- bash

# Delete pod
kubectl delete pod pod-name
kubectl delete pod pod-name --force --grace-period=0

# Port forwarding
kubectl port-forward pod-name 8080:80

# Copy files
kubectl cp file.txt pod-name:/path
kubectl cp pod-name:/path/file.txt ./
```

### Deployments
```bash
# Create deployment
kubectl create deployment nginx --image=nginx
kubectl create deployment nginx --image=nginx --replicas=3

# List deployments
kubectl get deployments
kubectl get deploy

# Scale deployment
kubectl scale deployment nginx --replicas=5

# Update image
kubectl set image deployment/nginx nginx=nginx:1.19

# Rollout status
kubectl rollout status deployment/nginx
kubectl rollout history deployment/nginx
kubectl rollout undo deployment/nginx

# Edit deployment
kubectl edit deployment nginx

# Delete deployment
kubectl delete deployment nginx
```

### Services
```bash
# Create service
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl create service clusterip nginx --tcp=80:80

# List services
kubectl get services
kubectl get svc

# Describe service
kubectl describe service nginx

# Delete service
kubectl delete service nginx
```

### Namespaces
```bash
# List namespaces
kubectl get namespaces
kubectl get ns

# Create namespace
kubectl create namespace dev

# Set default namespace
kubectl config set-context --current --namespace=dev

# Delete namespace
kubectl delete namespace dev
```

### ConfigMaps & Secrets
```bash
# Create ConfigMap
kubectl create configmap app-config --from-file=config.properties
kubectl create configmap app-config --from-literal=key=value

# List ConfigMaps
kubectl get configmaps

# Describe ConfigMap
kubectl describe configmap app-config

# Create Secret
kubectl create secret generic db-secret --from-literal=password=mypass
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass

# List secrets
kubectl get secrets

# Decode secret
kubectl get secret db-secret -o jsonpath='{.data.password}' | base64 -d
```

### Apply & Manage Resources
```bash
# Apply configuration
kubectl apply -f deployment.yaml
kubectl apply -f directory/

# Create from file
kubectl create -f deployment.yaml

# Delete from file
kubectl delete -f deployment.yaml

# Get resource YAML
kubectl get pod pod-name -o yaml
kubectl get deployment nginx -o json

# Dry run
kubectl apply -f deployment.yaml --dry-run=client
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml

# Replace resource
kubectl replace -f deployment.yaml
```

## YAML Manifests

### Pod Definition
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.19
    ports:
    - containerPort: 80
    env:
    - name: ENV_VAR
      value: "production"
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### Deployment Definition
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service Definition
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```

### ConfigMap Definition
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgres://db:5432/mydb"
  log_level: "info"
  config.properties: |
    property1=value1
    property2=value2
```

### Secret Definition
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=        # base64 encoded
  password: cGFzc3dvcmQ=    # base64 encoded
```

### Persistent Volume & Claim
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### Using ConfigMap & Secret in Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:1.0
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: config-volume
    configMap:
      name: app-config
  - name: secret-volume
    secret:
      secretName: db-secret
```

## Service Types

### ClusterIP (Default)
```yaml
# Internal cluster IP, accessible only within cluster
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
```

### NodePort
```yaml
# Exposes service on each node's IP at a static port
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080    # 30000-32767 range
```

### LoadBalancer
```yaml
# Cloud provider load balancer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
```

### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

## Advanced Concepts

### DaemonSet
```yaml
# Runs one pod per node
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: logging-agent
spec:
  selector:
    matchLabels:
      app: logging
  template:
    metadata:
      labels:
        app: logging
    spec:
      containers:
      - name: fluentd
        image: fluentd:latest
```

### StatefulSet
```yaml
# For stateful applications (databases)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

### Job
```yaml
# Run to completion
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-calculation
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

### CronJob
```yaml
# Scheduled jobs
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"    # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["/bin/backup.sh"]
          restartPolicy: OnFailure
```

## Resource Management

### Resource Requests & Limits
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"           # 250 millicores = 0.25 CPU
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### Horizontal Pod Autoscaler
```bash
kubectl autoscale deployment nginx --cpu-percent=50 --min=1 --max=10
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

## Health Checks

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Readiness Probe
```yaml
readinessProbe:
  tcpSocket:
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Startup Probe
```yaml
startupProbe:
  exec:
    command:
    - /bin/check-startup.sh
  initialDelaySeconds: 0
  periodSeconds: 10
  failureThreshold: 30
```

## Common Interview Questions

**Q: What is a Pod?**
- Smallest deployable unit in Kubernetes
- Can contain one or more containers
- Shares network namespace and storage volumes
- Ephemeral by nature

**Q: Difference between Deployment and ReplicaSet?**
- ReplicaSet ensures specified number of pod replicas running
- Deployment manages ReplicaSets and provides declarative updates
- Deployment supports rollback, rolling updates
- Use Deployment, not ReplicaSet directly

**Q: What is a Service and why needed?**
- Stable network endpoint for pods
- Pods are ephemeral, IPs change
- Service provides load balancing
- Types: ClusterIP, NodePort, LoadBalancer

**Q: Explain Namespace**
- Virtual clusters within physical cluster
- Resource isolation and organization
- Resource quotas per namespace
- RBAC policies per namespace

**Q: What are ConfigMaps and Secrets?**
- ConfigMap: Non-sensitive configuration data
- Secret: Sensitive data (base64 encoded)
- Both decouple config from container images
- Can be mounted as volumes or env variables

**Q: Difference between StatefulSet and Deployment?**
- StatefulSet: For stateful apps (databases)
- Stable network identity and persistent storage
- Ordered deployment and scaling
- Deployment: For stateless apps

**Q: What is an Ingress?**
- Manages external HTTP/HTTPS access to services
- Provides load balancing, SSL termination
- Name-based virtual hosting
- Requires Ingress Controller (nginx, traefik)

**Q: Explain Rolling Update**
- Gradual replacement of old pods with new
- Zero downtime deployment
- Controlled by maxSurge and maxUnavailable
- Can rollback if issues occur

**Q: What is kubectl?**
- Command-line tool for Kubernetes
- Communicates with API server
- Manages cluster resources
- Configuration in ~/.kube/config

**Q: How does Kubernetes scheduling work?**
- Scheduler watches for unscheduled pods
- Finds suitable node based on resources, constraints
- Considers: resource requests, node selectors, affinity rules
- Binds pod to node

**Q: What are Labels and Selectors?**
- Labels: Key-value pairs attached to objects
- Selectors: Query labels to identify resources
- Used for grouping and selecting objects
- Foundation of loose coupling in K8s
