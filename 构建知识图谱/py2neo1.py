# 编写时间:2023/7/18 22:20
from py2neo import Graph, Node, Relationship

# Neo4j数据库连接配置
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

# 导入节点数据
def import_nodes_from_csv():
    with open('nodes.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        property = lines[0].strip().split(',')[2:]
        # property = ['brand','code','engName','goods_id','id','image','max','min','name','price','size','sub_name','typeName']
        for line in lines[1:]:
            row = line.strip().split(',')
            print(row)
            _id = int(row[0])
            labels = row[1].split(':')[1]
            print(labels)
            properties = {key: value for key, value in zip(property, row[2:]) if value and key}
            if not row[10]:
                properties['name'] = row[13]
            node = Node(labels, _id=_id, **properties)
            graph.create(node)

# 导入关系数据
def import_relationships_from_csv():
    with open('rel.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines[1:]:
            row = line.strip().split(',')
            start_id = int(row[0])
            end_id = int(row[1])
            rel_type = row[2]

            start_node = graph.nodes.match(_id=start_id).first()
            end_node = graph.nodes.match(_id=end_id).first()

            if start_node and end_node:
                relationship = Relationship(start_node, rel_type, end_node)
                graph.create(relationship)

# 调用函数导入节点和关系数据
import_nodes_from_csv()
import_relationships_from_csv()
