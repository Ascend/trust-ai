module aiguard-plugin

go 1.16

require (
        github.com/fsnotify/fsnotify v1.4.9
        go.uber.org/atomic v1.7.0
        golang.org/x/net v0.0.0-20210405180319-a5a99cb37ef4
        golang.org/x/text v0.3.7 // indirect
        google.golang.org/grpc v1.41.0
        k8s.io/kubelet v0.19.4
)

replace (
        go.uber.org/atomic => go.uber.org/atomic v1.6.0
        golang.org/x/net v0.0.0-20210405180319-a5a99cb17ef4 => golang.org/x/net v0.0.0-20210226172049-e18ecbb05110
        k8s.io/api => k8s.io/api v0.19.4
        k8s.io/apiextensions-apiserver => k8s.io/apiextensions-apiserver v0.19.4
        k8s.io/apimachinery => k8s.io/apimachinery v0.19.4
        k8s.io/component-base => k8s.io/component-base v0.19.4
)
