import os

import shutil



async def delete_files(

    *paths

):

    for path in paths:

        try:

            if not path:

                continue


            # File Delete

            if os.path.isfile(path):

                os.remove(path)


            # Folder Delete

            elif os.path.isdir(path):

                shutil.rmtree(

                    path,

                    ignore_errors=True

                )

        except:

            pass
