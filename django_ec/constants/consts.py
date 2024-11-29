from enum import Enum

class Menu(Enum):
    LIST = (1,'商品一覧','admin_list')
    PURCHACE_LIST = (2,'購入明細','admin_purchace_list')
    # CREATE = (2,'商品作成','admin_create')
    # EDIT = (3,'商品編集','admin_edit')
    # DELETE = (4,'商品削除','admin_delete')

    def __init__(self, id, label, path):
        self.id = id
        self.label = label
        self.path = path