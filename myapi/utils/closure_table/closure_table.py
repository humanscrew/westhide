from myapi.extensions import db
from sqlalchemy.sql.expression import and_, or_, func


class ClosureTable:
    def __init__(
        self,
        tree_model,
        node_model,
        closure_table_model,
        node_schema,
        closure_table_schema,
        ancestor_key="name",
        descendant_key="children",
    ):
        self.tree_model = tree_model
        self.node_model = node_model
        self.closure_table_model = closure_table_model
        self.node_schema = node_schema
        self.closure_table_schema = closure_table_schema
        self.ancestor_key = ancestor_key
        self.descendant_key = descendant_key
        self.nodes = []

    def get_node(self, value, field="name"):
        for node in self.nodes:
            if node[field] == value:
                return node
        node = self.node_model.query.filter(
            getattr(self.node_model, field) == value
        ).first()
        node = self.node_schema().dump(node)
        self.nodes.extend(node)
        return node

    def add_link(self, tree_id, ancestor_id, descendant_id, distance, depth):
        # ancestor_id = self.node_model.query.with_entities(self.node_model.id).filter_by(name=ancestor).one().id
        # descendant_id = self.node_model.query.with_entities(self.node_model.id).filter_by(name=descendant).one().id
        closure_table = self.closure_table_model(
            tree_id=tree_id,
            ancestor_id=ancestor_id,
            descendant_id=descendant_id,
            distance=distance,
            depth=depth,
        )
        db.session.add(closure_table)
        db.session.commit()

    def handle_create_tree(
        self, tree_list, ancestor_key, descendant_key, ancestor_list=None, tree_id=None
    ):
        for tree in tree_list:
            node_name = tree.get(ancestor_key)
            if not node_name:
                return

            depth = isinstance(ancestor_list, list) and len(ancestor_list)
            if not depth:
                max_tree_id = db.session.query(func.max(self.tree_model.id)).scalar()
                tree_id = max_tree_id + 1 if max_tree_id else 1
                tree_root = self.tree_model(id=tree_id, name=node_name)
                db.session.add(tree_root)
                db.session.commit()

            node_id = self.get_node(node_name).get("id")
            for index, ancestor in enumerate(ancestor_list):
                distance = depth - index
                ancestor_id = self.get_node(ancestor).get("id")
                self.add_link(tree_id, ancestor_id, node_id, distance, depth)

            self.add_link(tree_id, node_id, node_id, 0, depth)

            descendant_list = tree.get(descendant_key)
            if isinstance(descendant_list, list):
                ancestor_list.append(node_name)
                self.handle_create_tree(
                    descendant_list,
                    ancestor_key,
                    descendant_key,
                    ancestor_list,
                    tree_id,
                )
                ancestor_list.pop()

    def create_tree(self, tree_list, ancestor_key=None, descendant_key=None):
        # tableName = self.closure_table_model.__tablename__
        # db.session.execute(f"TRUNCATE TABLE {tableName}")
        ancestor_key = ancestor_key or self.ancestor_key
        descendant_key = descendant_key or self.descendant_key
        self.handle_create_tree(tree_list, ancestor_key, descendant_key)

    def handle_get_tree(self, ancestor_list, descendant_list, link_list):
        depth = ancestor_list and len(ancestor_list)
        for link in link_list:
            ancestor_id = link["ancestorId"]
            if link["depth"] == depth and ancestor_id == ancestor_list[depth - 1]:
                descendant_id = link["descendantId"]
                node = dict(**self.get_node(descendant_id, "id"), children=[])
                index = len(descendant_list)
                descendant_list.append(node)
                ancestor_list.append(descendant_id)
                self.handle_get_tree(
                    ancestor_list, descendant_list[index]["children"], link_list
                )
                ancestor_list.pop()

    def get_tree_list(self, nodes, tree_ids):
        self.nodes = nodes

        node_id_list = [node.get("id") for node in nodes]
        # for index in range(0, len(nodes)):
        #     del nodes[index]["id"]

        closure_table = self.closure_table_model.query.filter(
            and_(
                self.closure_table_model.tree_id.in_(tree_ids),
                self.closure_table_model.ancestor_id.in_(node_id_list),
                self.closure_table_model.descendant_id.in_(node_id_list),
                or_(
                    self.closure_table_model.distance == 1,
                    self.closure_table_model.depth == 0,
                ),
            )
        ).all()
        closure_table_schema = self.closure_table_schema(many=True)
        closure_table = closure_table_schema.dump(closure_table)

        closure_tree_ids = []
        link_group = {}
        for link in closure_table:
            tree_id = link["treeId"]
            if tree_id not in closure_tree_ids:
                closure_tree_ids.append(tree_id)
                link_group[tree_id] = []
            link_group[tree_id].append(link)

        tree_list = []
        for tree_id in link_group:
            link_list = link_group[tree_id]
            depth_list = [item["depth"] for item in link_list]
            if 0 in depth_list:
                root_node_id = link_list[depth_list.index(0)]["ancestorId"]
            else:
                continue

            ancestor_list = [root_node_id]
            tree = dict(**self.get_node(root_node_id, "id"), children=[])

            self.handle_get_tree(ancestor_list, tree["children"], link_list)

            tree_list.append(tree)
        return tree_list
