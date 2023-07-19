# 启动步骤
**ps.本项目只能在服务器上面启动,以下所有步骤基于服务器完成**

https://github.com/5KG-UCAS/CosmeticsKG (后端)
https://github.com/5KG-UCAS/CosmeticsKG-Web (前端)

[百度云项目资料](https://pan.baidu.com/s/1MLivu-yKH7h0PVKsJBs2cw?pwd=fbx1)

服务器安装docker，宝塔面板，本地电脑安装FinalShell（安装步骤自行上网查询）

## 1.安装neo4j
由于作者开发版本时间，neo4j版本使用的是**3.5.22-community**，其他版本未测试，不保证兼容性。
![1.png](https://images.xcnv.com/2023/07/18/64b56e5987754.png)

1.docker安装neo4j
```
docker pull neo4j:3.5.22-community
```
2.创建neo4j目录
进入服务器opt目录，新建neo4j目录，在neo4j目录下新建data、logs、conf、import、plugins目录
```
cd /opt
mkdir neo4j
cd neo4j
mkdir data logs conf import plugins
```
3.创建neo4j容器

-d 后台运行 --name 容器名称 -p 端口映射 -v 挂载目录

xxxx:xxxx,前为主机端口，可自行修改，后为容器端口，不可修改
```
docker run -d --name neo4j \
-p 7474:7474 -p 7687:7687 \
-v /opt/neo4j/data:/data \
-v /opt/neo4j/logs:/logs \
-v /opt/neo4j/conf:/var/lib/neo4j/conf \
-v /opt/neo4j/import:/var/lib/neo4j/import \
-v /opt/neo4j/plugins:/plugins \
neo4j:3.5.22-community
```
4.修改neo4j配置文件
docker创建初级使用一般不需要修改
```
dbms.connector.bolt.listen_address=0.0.0.0:7687

dbms.connector.https.listen_address=0.0.0.0:7473

dbms.connectors.default_listen_address=0.0.0.0

dbms.memory.pagecache.size=512M

dbms.connector.http.listen_address=0.0.0.0:7474

wrapper.java.additional=-Dneo4j.ext.udc.source=docker
dbms.tx_log.rotation.retention_policy=100M size
dbms.directories.logs=/logs
HOME=/var/lib/neo4j
EDITION=community
```
5.重启neo4j容器
```
docker restart neo4j
```
6.访问neo4j
浏览器输入服务器ip:7474，出现如下界面，说明neo4j安装成功
默认用户名neo4j，密码neo4j，之后会让你修改密码，修改完密码后，记得保存，后面会用到
![2.png](https://images.xcnv.com/2023/07/18/64b56e578ca50.png)

---

## 2.安装Tomcat
由于使用宝塔面板安装，所以不需要自己安装，直接在宝塔面板安装即可，主打的就是便利，哈哈
![3.png](https://images.xcnv.com/2023/07/18/64b56e590b22e.png)
后续需要进入宝塔的目录可以直接点击上图的**小黄色文件夹图标**，进入目录
---

## 3.项目调试部署
### 修改项目配置文件
进入下载的代码，进入src/main/resources目录，修改application.properties文件
根据自己部署的服务器ip和密码修改

```
neo4j.uri=bolt://ip:7687
neo4j.username=neo4j
neo4j.password=123456
```
找到SessionCreater.java文件，修改neo4j的用户名和密码
![4.png](https://images.xcnv.com/2023/07/18/64b56e59edd9f.png)

### 打包项目
我的idea是我自己专门设置的，所以不一定和你的一样，但是打包的步骤是一样的，自行百度

可以使用命令行打包，也可以使用idea打包，打包后会在target目录下生成一个war包，war包就是我们需要的部署包
![5.png](https://images.xcnv.com/2023/07/18/64b56e5896159.png)
打包时一定要跳过测试，不然会自动生成脏数据.成功如下图所示
![6.png](https://images.xcnv.com/2023/07/18/64b56e580c5c2.png)

### 部署项目

| 文件名/文件夹名       | 描述                                                       |
|----------------|----------------------------------------------------------|
| CosmeticsKG    | 系统后端（智能问答模块）源码，仓库：https://github.com/5KG-UCAS/CosmeticsKG |
| CosmeticsKG-Web | 系统Web前端源码，仓库：https://github.com/5KG-UCAS/CosmeticsKG-Web |
| graph.db.tar   |图数据库数据文件|
| graphserver.war |InteractiveGraph-neo4j中间件，仓库：https://github.com/grapheco/InteractiveGraph-neo4j|
|conf1.properties|中间件配置文件|
|CosmeticsKG.war|系统后端war包|
|HanLP语言包|http://nlp.hankcs.com/download.php?file=data|


#### 3.1安装环境
安装依赖环境中的环境。
以下步骤使用$Neo4j代替Neo4j安装路径根目录；使用$Tomcat代替Tomcat安装路径根

如果安装上述使用宝塔安装tomcat，目录为：/www/server/tomcat

#### 3.2导入数据
1. 将graph.db.tar复制到 /opt/neo4j/data/databases
2. 解压得到graph.db的文件夹，若不是请重命名为该名称
   1 tar ‐xvf graph.db.tar
3. 重启neo4j容器
  ```
  docker restart neo4j
  ```

#### 3.3部署war包
![1689611991069.png](https://images.xcnv.com/2023/07/18/64b56ede816d5.png)
1. 拷贝graphserver.war 到 $Tomcat/webapps
2. 拷贝CosmeticsKG.war 到 $Tomcat/webapps
3. 拷贝CosmeticsKG-Web文件夹到$Tomcat/webapps

### 3.4修改配置文件(可以自行修改默认访问端口，百度)
1. 拷贝conf1.properties到 $Tomcat/webapps/graphserver/WEB-INF，并修
   改配置文件中以下几行：
```
   #你的Neo4j地址和端口号
   neo4j.boltUrl=bolt://localhost:768
   #Neo4j登录用户名
   neo4j.boltUser=neo4j
   #Neo4j登录密码
   neo4j.boltPassword=1
   ```
6. 进入$Tomcat/webapps/CosmeticsKG/WEB-INF/classes，修改neo4j文
   件：
```
   #你的Neo4j地址和端口号
   bolt://localhost:768
   #Neo4j登录用户名
   neo4j
   #Neo4j登录密码
   1
   ```
7. 重启Tomcat服务器
```
   cd $Tomcat/bin
   ./shutdown.sh
   ./startup.sh
```
##### 3.5配置HanLP语言包
   进入$Tomcat/webapps/CosmeticsKG/WEB-INF/classes，修改hanlp.properties文
   件：
```
   #修改为HanLP语言包解压后的路径（路径可以自己在服务器上创建一个文件夹，放入下载的data包）
   root=~/HanLP/
```
### 3.6 完成
   浏览器打开：
   1 http://ip:port/CosmeticsKG‐Web/
   浏览器输入网址时会将-转义，导致404，可以进入上传后的文件，修改前端的目录名为CosmeticsKGWeb，即可访问