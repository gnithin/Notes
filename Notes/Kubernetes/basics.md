# Kubernetes basics

Following along to [this tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-interactive/).

## Module 1 
- Link - https://kubernetes.io/docs/tutorials/kubernetes-basics
- Kubernetes a way to manage containers, in a deterministic way
- Maybe this is what others mean by orchestration, although it seems to be a lot more loaded than that

## Questions 
- What exactly is a master? Is it a container?
- Should the master run on a totally isolated machine? (The docs seem to imply that)
- What does a node signify? Is it a machine?
- Is pod a container? Can I have multiple pods in a node?


- Turns out that you can interact with Kubernetes via UI as well (I wonder what tools provide that?)

### Minikube
- Minikube or Microk8s are basically programs that'll allow you to run container instances locally
- More importantly, they seem to stress that it's a one-node VM
- If all it does is spawn containers inside it, how does it matter how many nodes there are? Creating multiple instances of a container is not a problem :/ 
- Both Minikube and microk8s have something called add-ons
	- I think these are programs that are not default opt-in since not everyone needs them.
	- Stuff like load-balancing and other features are not required for full-fledged local testing

- [QUESTION] After running `minikube start`, why does it say - "Done! kubectl is now configured to use "minikube""
	- What is it exactly doing to kubectl command? Is it monkey-patching it or something?

- When anyone talks about a Kubernetes cluster, they seem to talk about all the masters, and just not one master and a bunch of followers. Apparently production requires atleast 2 masters 

- [QUESTION] `kubectl get nodes` seems to list out the single k8s cluster as a whole. Was it not supposed to just print out the master. I thought master and nodes are different things. 
- [QUESTION] In the previous output, `master` was said to be a role. Are all machines nodes, and each pod in them have roles? That doesn't sound right at all.

****

## Module 2 
- Link - https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/
- Deployment is a configuration
- Whenever we create and apply a deployment configuration, the master node pulls that up, schedules it and is responsible for it's creation and update
- A deployments controller basically monitors the health of each deployment that is run, and is responsible for maintaining a particular number of deployments in the cluster
- This deployments controller is something that lives inside the master node
- A standard format of a kubectl command is `kubectl action resource`
	- Action here is a verb to do something
	- Resource is the endpoint/thing to do the action on
	- [QUESTION] Is the resource optional?
- Within the same Kubernetes cluster, every pod is visible
- But outside the k8s cluster, it is not. 
- [QUESTION] What is the difference between a pod and a service 
- One way to communicate with the pods is that kubectl can provide a proxy, which'll forward all the commands into the cluster. So it's as if we are running the commands inside the cluster.
	- [QUESTION] Are we then inside a node? Inside a container? Inside master?
- Each pod will be assigned a different endpoint through the proxy
	- [QUESTION] what are those endpoints exactly?
- In order for the internal pods to communicate with the outside world, we use a service (This seems analogous to the services directory being used to connect to db or any other external persistent storage tooling).

****

## Module - 3
- Link - https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/
- "A Pod is a Kubernetes abstraction that represents a group of one or more application containers (such as Docker), and some shared resources for those containers."
	- This basically shatters most of my previous understanding of what it actually means
- The resources for those containers are - 
	- Shared storage, called volumes
	- Networking - A bunch of ip address that the pod can use
	- Container metadata - Image details (I guess this should just be a file?)
- A pod can have multiple containers running inside it
	- The nature of this idea is pretty intriguing
	- [QUESTION] What is the scenario under which I will have to share 2 containers within the same pod? Why can't I have different pods altogether? They seem to be sharing the same IP and port address space, what's the advantage there? I am not able to map this to a real-world entity
		- One scenario is probabyl when they need to share disk?
- Each pod is tied to a node (I think it is being referred here as a physical machine or a server)

- A node is a physical or a virtual machine (finally!)
- A node has multiple pods
- It's controlled by the master (which I assume is also a node?)
- A kuubelet is a process inside the node, that is responsible to maintain communication between a node and a master
- There is a messed up endpoint that we'd end-up hitting if we need to access the pod
- Anything that's being printed out in the pod is basically logged (That's pretty awesome and feels like a bit too overkill)



## Commands list
- `minikube start` - To start a VM running a Kubernetes instance (It'll have docker installed in it apparently)
- `kubectl version` - Returns the version of the kubectl client, as well as the Kubernetes version number in the master
- `kubectl cluster-info` - Returns the cluster details
- `kubectl get nodes` - Gets all the nodes 
- `kubectl create deployment <deployment-name> --image=<image-link>` - Creates a new deployment from the given link
- `kubectl get deployments` - Gets all the deployments that are done under the current cluster
- `kubectl proxy` - Creates a communication link between the cluster and the terminal process. This will create an endpoint that'll allow us to communicate with the k8s server. This will run a server that'll keep running until it's time to turn it off again
- `kubectl get pods` - Lists all the pods in all the nodes (Hmm, that's weird, there should be a way to filter this down node by node)
- `kubectl describe pods` - Describe a pod in detail
- `kubectl logs <pod-name>` - Get the logs of a pod
- `kubectl exec <pod-name> <command>` - Run a particular command inside a pod
	- Use `kubectl exec -it <pod-name> bash` to run a terminal


## References 







