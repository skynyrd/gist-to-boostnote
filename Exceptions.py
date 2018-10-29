class CannotFindFolderKeyError(Exception):
    def __init__(self, config_path, folder_name):
        super(CannotFindFolderKeyError, self).__init__(f"Cannot find folder name <{folder_name}>"
                                                       f" in config file <{config_path}>")
