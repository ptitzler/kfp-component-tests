### Overview

`src/add_numbers.py` defines a Python function. `src/test-add-numbers.py` creates a KFP component factory for that function, creates a two-node pipeline, and runs it.

### Create and run pipeline

```
$ python src/test-add-numbers.py http://.../pipeline [<namespace>] [<kf-uid> <kf-password>]
```

### References

- [Kubeflow documentation: Building Python function-based components](https://www.kubeflow.org/docs/components/pipelines/sdk/python-function-components/)