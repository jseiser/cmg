# CMG 

Python Web App which accepts POSTS requests to `/process` endpoint.  The format of the text file must be correct.
### Tech

* [python](https://www.python.org/)
* [flask](https://flask.palletsprojects.com/en/2.0.x/)
* [helm](https://helm.sh/)

### Pre-Req

Kubernetes Cluster
Helm Chart

Ideally, some sort of ingress but port-forward will work for POC

### Usage

```
cd chart/cmg
helm install cmg ./cmg-0.1.0.tgz
kubectl --namespace default port-forward service/cmg 8080:80

curl -X POST -F file=@data.txt http://localhost:8080/process
```

#### Results
```
{"hum-1":"Keep","hum-2":"Discard","temp-1":"Precise","temp-2":"Ultra Precise"}
```

Running Multiple Pods
```
❯ kubectl get pods
NAME                   READY   STATUS    RESTARTS   AGE
cmg-7f5d76ddb9-ml6cv   1/1     Running   0          19s
cmg-7f5d76ddb9-pmdq2   1/1     Running   0          19s
```

## Things I wish I could change

1. Input file format is less than ideal.
2. Currently adding additinal devices/rules requires editing the source code.  Would be preferable if data ingestion could be seperate from business rules.
3. Slight CI is in place, but no chance to do proper CD
4. Helm Chart is not published.
5. No error handling in the code.

## Adding additional Devices/Rules


Extend this function
```
# Each Devices needs a rule to return its status
def rule_validation(device_type, name, metrics, ref_temp, ref_humidity):
    """Determine Rules for Device types"""
    metrics = list(map(float, metrics))
    if device_type == "thermometer":
        return check_thermometer(metrics, ref_temp)
        
    elif device_type == "humidity":
        return check_humidity(metrics, ref_humidity)
```

Then add a custom validation function for that device type.

```
def check_something(metrics, ref_temp):
    return "Pass"
```