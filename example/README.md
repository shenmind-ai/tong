
## 准备

下载 tong 客户端

```
wget 

```




## 验证

### 1. 使用 tong 客户端
```
tong validate

```

### 2. 使用 docker


```
ImageName="$(basename $(pwd))"
docker build -f Dockerfile -t $ImageName .
docker run -it  --rm $ImageName  python -c "from infer import Infer, Inputs; Infer().run_inference(Inputs())"

```

## 上传模型
```
tong push
```
