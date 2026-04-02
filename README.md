# Projet 2025 — Microservices avec Docker & Kubernetes

Projet utilisant des microservices (REST / gRPC), Docker et Kubernetes.

__Auteures__ : Marine GIMENEZ, Hanna SYSOIEVA

---

## Table des matières

1. [Commencer par un seul service en local](#1-commencer-par-un-seul-service-en-local)
2. [Ajouter une gateway en local](#2-ajouter-une-gateway-en-local)
3. [Ajouter un deuxième service en local](#3-ajouter-un-deuxième-service-en-local)
4. [Ajouter une base de données en local](#4-ajouter-une-base-de-données-en-local)
5. [Sécuriser le cluster (RBAC)](#5-sécuriser-le-cluster-rbac)

---

## 1. Commencer par un seul service en local

> Coder une mini application, créer et publier une image Docker, puis déployer sur Kubernetes.

```bash
# Build de l'image Docker
docker build -t heart:v1 .

# Lancement du conteneur
docker run -d -p 4444:5000 heart:v1

# Tag et push vers Docker Hub
docker tag heart:v1 gimenezm/heart:v1
docker login
docker push gimenezm/heart:v1

# Démarrage de Minikube
minikube start
kubectl get nodes

# Déploiement Kubernetes
kubectl apply -f heart-deployment.yml
kubectl apply -f heart-service-clusterip.yml
```

---

## 2. Ajouter une gateway en local

> Mise en place d'un Ingress pour router le trafic vers les services.

```bash
# Activation de l'addon Ingress
minikube addons enable ingress
kubectl get pods -n ingress-nginx

# Application de la configuration Ingress
kubectl apply -f ingress.yml
kubectl get ingress

# Configuration DNS locale (Windows)
# Éditer le fichier : C:\Windows\System32\drivers\etc\hosts
# Ajouter la ligne suivante :
# 127.0.0.1 prog-dist.info

# Activation du DNS Ingress et tunnel
minikube addons enable ingress-dns
minikube tunnel
```

> Accès à l'application : http://prog-dist.info

---

## 3. Ajouter un deuxième service en local

> Ajout d'un second microservice et liaison des services entre eux.

```bash
# Build de l'image Docker du second service
docker build -t titre:v1 .

# Lancement du conteneur
docker run -d -p 4445:5000 titre:v1

# Tag et push vers Docker Hub
docker tag titre:v1 gimenezm/titre:v1
docker login
docker push gimenezm/titre:v1

# Démarrage de Minikube
minikube start
kubectl get nodes

# Déploiement Kubernetes
kubectl apply -f titre-deployment.yml
kubectl apply -f titre-service-clusterip.yml
```

---

## 4. Ajouter une base de données en local

> Déploiement de MySQL avec gestion des secrets, volumes persistants et configmaps.

```bash
# Application des ressources Kubernetes MySQL
kubectl apply -f mysql-secret.yaml
kubectl apply -f mysql-storage.yaml
kubectl apply -f mysql-configmap.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-serviceNodePort.yaml

# Vérification des ressources
kubectl get secrets
kubectl get PersistentVolumes
kubectl get PersistentVolumeClaims
kubectl get deployments
kubectl get services
kubectl get pods

# Connexion au pod MySQL
kubectl exec --stdin --tty mysql-8f5d78b77-5rjrz -- mysql -ptest1234

# Montage d'un volume local
minikube mount .:/mnt/data
```

---

## 5. Sécuriser le cluster (RBAC)

> Mise en place du contrôle d'accès basé sur les rôles (Role-Based Access Control).

```bash
# Application des ressources RBAC
kubectl apply -f serviceaccount.yaml
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml

# Vérification des ressources créées
kubectl get serviceaccount
kubectl get role
kubectl get rolebinding

# Tests des permissions du service account
kubectl auth can-i get pods --as=system:serviceaccount:default:heart-user
kubectl auth can-i list services --as=system:serviceaccount:default:heart-user
kubectl auth can-i delete pods --as=system:serviceaccount:default:heart-user
kubectl auth can-i create deployments --as=system:serviceaccount:default:heart-user
```

---

## Références

- [kubernetes-minikube](https://github.com/charroux/kubernetes-minikube)
- [CodingWithKubernetes](https://github.com/charroux/CodingWithKubernetes)
- [gRPCSpring](https://github.com/charroux/gRPCSpring)
- [noops/mysql](https://github.com/charroux/noops/tree/main/mysql)
- [kubernetes-volumes](https://github.com/charroux/kubernetes-volumes)
- [RBAC Kubernetes](https://kubernetes.io/fr/docs/reference/access-authn-authz/rbac/)
