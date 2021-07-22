### Overview

`src/split_file.py` defines a Python function. `src/test-split-file.py` creates a KFP component factory for that function, creates a one node pipeline, and runs it.

### Create and run pipeline

```
$ python src/test-split-file.py http://.../pipeline [<namespace>] [<kf-uid> <kf-password>]
```

### References

- [Kubeflow documentation: Building Python function-based components](https://www.kubeflow.org/docs/components/pipelines/sdk/python-function-components/)