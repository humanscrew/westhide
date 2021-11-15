from myapi.extensions import db
from sqlalchemy.sql.expression import and_, or_, func


class ClosureTable:

    def __init__(self,
                 TreeModel, NodeModel, ClosureTableModel,
                 NodeSchema, ClosureTableSchema,
                 ancestorKey="name", descendantKey="children"
                 ):
        self.TreeModel = TreeModel
        self.NodeModel = NodeModel
        self.ClosureTableModel = ClosureTableModel
        self.NodeSchema = NodeSchema
        self.ClosureTableSchema = ClosureTableSchema
        self.ancestorKey = ancestorKey
        self.descendantKey = descendantKey

    def addLink(self, treeId, ancestorId, descendantId, distance, depth):
        # ancestorId = self.NodeModel.query.with_entities(self.NodeModel.id).filter_by(name=ancestor).one().id
        # descendantId = self.NodeModel.query.with_entities(self.NodeModel.id).filter_by(name=descendant).one().id
        closureTable = self.ClosureTableModel(
            tree_id=treeId, ancestor_id=ancestorId, descendant_id=descendantId, distance=distance, depth=depth
        )
        db.session.add(closureTable)
        db.session.commit()

    def createTree(self, treeList, ancestorKey=None, descendantKey=None):

        nodeSchema = self.NodeSchema(many=True)
        nodes = self.NodeModel.query.with_entities(self.NodeModel.id, self.NodeModel.name).all()
        nodes = nodeSchema.dump(nodes)

        def getNodeId(nodeName):
            for item in nodes:
                if item["name"] == nodeName:
                    return item["id"]

        def handleTree(treeList, ancestorKey, descendantKey, ancestorList=[], treeId=None):
            for tree in treeList:
                nodeName = tree.get(ancestorKey)
                if not nodeName:
                    return

                depth = len(ancestorList)
                if not depth:
                    maxTreeId = db.session.query(func.max(self.TreeModel.id)).scalar()
                    treeId = maxTreeId + 1 if maxTreeId else 1
                    treeRoot = self.TreeModel(id=treeId, name=nodeName)
                    db.session.add(treeRoot)
                    db.session.commit()

                nodeId = getNodeId(nodeName)
                for index, ancestor in enumerate(ancestorList):
                    distance = depth-index
                    ancestorId = getNodeId(ancestor)
                    self.addLink(treeId, ancestorId, nodeId, distance, depth)

                self.addLink(treeId, nodeId, nodeId, 0, depth)

                descendantList = tree.get(descendantKey)
                if descendantList:
                    ancestorList.append(nodeName)
                    handleTree(descendantList, ancestorKey, descendantKey, ancestorList, treeId)
                    ancestorList.pop()

        # tableName = self.ClosureTableModel.__tablename__
        # db.session.execute(f"TRUNCATE TABLE {tableName}")
        ancestorKey = ancestorKey if ancestorKey else self.ancestorKey
        descendantKey = descendantKey if descendantKey else self.descendantKey
        handleTree(treeList, ancestorKey, descendantKey)

    def getTreeList(self, nodes, treeIds):

        nodeIdList = [item.get("id") for item in nodes]
        for index in range(0, len(nodes)):
            del nodes[index]["id"]

        def getNode(nodeId):
            index = nodeIdList.index(nodeId)
            node = nodes[index]
            return node

        closureTable = self.ClosureTableModel.query.filter(
            and_(
                self.ClosureTableModel.tree_id.in_(treeIds),
                self.ClosureTableModel.ancestor_id.in_(nodeIdList),
                self.ClosureTableModel.descendant_id.in_(nodeIdList),
                or_(self.ClosureTableModel.distance == 1, self.ClosureTableModel.depth == 0)
            )
        ).all()
        closureTableSchema = self.ClosureTableSchema(many=True)
        closureTable = closureTableSchema.dump(closureTable)

        treeIds = []
        linkGroup = {}
        for link in closureTable:
            treeId = link["treeId"]
            if not treeId in treeIds:
                treeIds.append(treeId)
                linkGroup[treeId] = []
            linkGroup[treeId].append(link)

        treeList = []
        for groupKey in linkGroup:
            linkList = linkGroup[groupKey]
            depthList = [item["depth"] for item in linkList]
            if 0 in depthList:
                rootNodeId = linkList[depthList.index(0)]["ancestorId"]
            else:
                break

            ancestorList = [rootNodeId]
            map = {}
            map.update(**getNode(rootNodeId), children=[])

            def handleMap(ancestorList, tree):
                depth = len(ancestorList)
                for link in linkList:
                    ancestorId = link["ancestorId"]
                    if link["depth"] == depth and ancestorId == ancestorList[depth-1]:
                        descendantId = link["descendantId"]
                        treeItem = {}
                        treeItem.update(**getNode(descendantId), children=[])
                        treeItemIndex = len(tree)
                        tree.append(treeItem)
                        ancestorList.append(descendantId)
                        handleMap(ancestorList, tree[treeItemIndex]["children"])
                        ancestorList.pop()

            handleMap(ancestorList, map["children"])
            treeList.append(map)
        return treeList
