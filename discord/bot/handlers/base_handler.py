from chains.chain_manager import ChainManager

class BaseHandler:
    def __init__(self, chain_manager: ChainManager):
        self.chain_manager = chain_manager
