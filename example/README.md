
## 1. 准备

下载 tong 客户端

```shell
wget 

```




## 2. 验证

### 2.1 方式一：使用 tong 客户端 （推荐）
```shell
tong validate

```

### 2.2 方式二：使用 docker（可选）


```shell
ImageName="$(basename $(pwd))"
docker build -f Dockerfile -t $ImageName .
docker run -it  --rm $ImageName  python -c "from infer import Infer, Inputs; Infer().run_inference(Inputs())"

```

## 3. 上传模型
```
tong push
```
